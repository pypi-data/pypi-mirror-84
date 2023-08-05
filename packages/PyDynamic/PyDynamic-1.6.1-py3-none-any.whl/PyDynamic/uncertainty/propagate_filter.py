# -*- coding: utf-8 -*-
"""
This module contains functions for the propagation of uncertainties through
the application of a digital filter using the GUM approach.

This modules contains the following functions:

* :func:`FIRuncFilter`: Uncertainty propagation for signal y and uncertain FIR
  filter theta
* :func:`IIRuncFilter`: Uncertainty propagation for the signal x and the uncertain
  IIR filter (b,a)

.. note:: The Elster-Link paper for FIR filters assumes that the autocovariance
          is known and that noise is stationary!

"""

import numpy as np
from scipy.linalg import toeplitz
from scipy.signal import lfilter, lfilter_zi, dimpulse
from ..misc.tools import trimOrPad

__all__ = ["FIRuncFilter", "IIRuncFilter"]


def FIRuncFilter(y, sigma_noise, theta, Utheta=None, shift=0, blow=None, kind="corr"):
    """Uncertainty propagation for signal y and uncertain FIR filter theta

    A preceding FIR low-pass filter with coefficients `blow` can be provided optionally.

    Parameters
    ----------
        y: np.ndarray
            filter input signal
        sigma_noise: float or np.ndarray
            float:    standard deviation of white noise in y
            1D-array: interpretation depends on kind
        theta: np.ndarray
            FIR filter coefficients
        Utheta: np.ndarray, optional
            covariance matrix associated with theta
            if the filter is fully certain, use `Utheta = None` (default) to make use of more efficient calculations. 
            see also the comparison given in <examples\Digital filtering\FIRuncFilter_runtime_comparison.py>
        shift: int, optional
            time delay of filter output signal (in samples) (defaults to 0)
        blow: np.ndarray, optional
            optional FIR low-pass filter
        kind: string
            only meaningful in combination with sigma_noise a 1D numpy array
            "diag": point-wise standard uncertainties of non-stationary white noise
            "corr": single sided autocovariance of stationary (colored/correlated)
            noise (default)

    Returns
    -------
        x: np.ndarray
            FIR filter output signal
        ux: np.ndarray
            point-wise standard uncertainties associated with x


    References
    ----------
        * Elster and Link 2008 [Elster2008]_

    .. seealso:: :mod:`PyDynamic.deconvolution.fit_filter`

    """

    Ntheta = len(theta)  # FIR filter size

    # check which case of sigma_noise is necessary
    if isinstance(sigma_noise, float):
        sigma2 = sigma_noise ** 2

    elif isinstance(sigma_noise, np.ndarray) and len(sigma_noise.shape) == 1:
        if kind == "diag":
            sigma2 = sigma_noise ** 2
        elif kind == "corr":
            sigma2 = sigma_noise
        else:
            raise ValueError("unknown kind of sigma_noise")

    else:
        raise ValueError(
            f"FIRuncFilter: Uncertainty sigma_noise associated "
            f"with input signal is expected to be either a float or a 1D array but "
            f"is of shape {sigma_noise.shape}. Please check documentation for input "
            f"parameters sigma_noise and kind for more information."
        )


    if isinstance(blow,np.ndarray):             # calculate low-pass filtered signal and propagate noise

        if isinstance(sigma2, float):
            Bcorr = np.correlate(blow, blow, 'full') # len(Bcorr) == 2*Ntheta - 1
            ycorr = sigma2 * Bcorr[len(blow)-1:]     # only the upper half of the correlation is needed

            # trim / pad to length Ntheta
            ycorr = trimOrPad(ycorr, Ntheta)
            Ulow = toeplitz(ycorr)

        elif isinstance(sigma2, np.ndarray):

            if kind == "diag":
                # [Leeuw1994](Covariance matrix of ARMA errors in closed form) can be used, to derive this formula
                # The given "blow" corresponds to a MA(q)-process.
                # Going through the calculations of Leeuw, but assuming
                # that E(vv^T) is a diagonal matrix with non-identical elements,
                # the covariance matrix V becomes (see Leeuw:corollary1)
                # V = N * SP * N^T + M * S * M^T
                # N, M are defined as in the paper
                # and SP is the covariance of input-noise prior to the observed time-interval
                # (SP needs be available len(blow)-timesteps into the past. Here it is
                # assumed, that SP is constant with the first value of sigma2)

                # V needs to be extended to cover Ntheta-1 timesteps more into the past
                sigma2_extended = np.append(sigma2[0] * np.ones((Ntheta - 1)), sigma2)

                N = toeplitz(blow[1:][::-1], np.zeros_like(sigma2_extended)).T
                M = toeplitz(trimOrPad(blow, len(sigma2_extended)), np.zeros_like(sigma2_extended))
                SP = np.diag(sigma2[0] * np.ones_like(blow[1:]))
                S = np.diag(sigma2_extended)

                # Ulow is to be sliced from V, see below
                V = N.dot(SP).dot(N.T) + M.dot(S).dot(M.T)

            elif kind == "corr":

                # adjust the lengths sigma2 to fit blow and theta
                # this either crops (unused) information or appends zero-information
                # note1: this is the reason, why Ulow will have dimension (Ntheta x Ntheta) without further ado

                # calculate Bcorr
                Bcorr = np.correlate(blow, blow, "full")

                # pad or crop length of sigma2, then reflect some part to the left and invert the order
                # [0 1 2 3 4 5 6 7] --> [0 0 0 7 6 5 4 3 2 1 0 1 2 3]
                sigma2 = trimOrPad(sigma2, len(blow) + Ntheta - 1)
                sigma2_reflect = np.pad(sigma2, (len(blow) - 1, 0), mode="reflect")

                ycorr = np.correlate(sigma2_reflect, Bcorr, mode="valid") # used convolve in a earlier version, should make no difference as Bcorr is symmetric
                Ulow = toeplitz(ycorr)

        xlow, _ = lfilter(blow, 1.0, y, zi=y[0] * lfilter_zi(blow, 1.0))

    else:  # if blow is not provided
        if isinstance(sigma2, float):
            Ulow = np.eye(Ntheta) * sigma2

        elif isinstance(sigma2, np.ndarray):

            if kind == "diag":
                # V needs to be extended to cover Ntheta timesteps more into the past
                sigma2_extended = np.append(sigma2[0] * np.ones((Ntheta - 1)), sigma2)

                # Ulow is to be sliced from V, see below
                V = np.diag(sigma2_extended) #  this is not Ulow, same thing as in the case of a provided blow (see above)

            elif kind == "corr":
                Ulow = toeplitz(trimOrPad(sigma2, Ntheta))

        xlow = y

    # apply FIR filter to calculate best estimate in accordance with GUM
    x, _ = lfilter(theta, 1.0, xlow, zi=xlow[0] * lfilter_zi(theta, 1.0))
    x = np.roll(x, -int(shift))

    # add dimension to theta, otherwise transpose won't work
    if len(theta.shape) == 1:
        theta = theta[:, np.newaxis]

    # NOTE: In the code below whereever `theta` or `Utheta` get used, they need to be flipped. 
    #       This is necessary to take the time-order of both variables into account. (Which is descending
    #       for `theta` and `Utheta` but ascending for `Ulow`.)
    #       
    #       Further details and illustrations showing the effect of not-flipping
    #       can be found at https://github.com/PTB-PSt1/PyDynamic/issues/183

    # handle diag-case, where Ulow needs to be sliced from V
    if kind == "diag":
        # UncCov needs to be calculated inside in its own for-loop
        # V has dimension (len(sigma2) + Ntheta) * (len(sigma2) + Ntheta) --> slice a fitting Ulow of dimension (Ntheta x Ntheta)
        UncCov = np.zeros((len(sigma2)))

        if isinstance(Utheta, np.ndarray):
            for k in range(len(sigma2)):
                Ulow = V[k:k+Ntheta,k:k+Ntheta]
                UncCov[k] = np.squeeze(np.flip(theta).T.dot(Ulow.dot(np.flip(theta))) + np.abs(np.trace(Ulow.dot(np.flip(Utheta)))))  # static part of uncertainty
        else:
            for k in range(len(sigma2)):
                Ulow = V[k:k+Ntheta,k:k+Ntheta]
                UncCov[k] = np.squeeze(np.flip(theta).T.dot(Ulow.dot(np.flip(theta))))  # static part of uncertainty

    else:
        if isinstance(Utheta, np.ndarray):
            UncCov = np.flip(theta).T.dot(Ulow.dot(np.flip(theta))) + np.abs(np.trace(Ulow.dot(np.flip(Utheta))))      # static part of uncertainty
        else:
            UncCov = np.flip(theta).T.dot(Ulow.dot(np.flip(theta)))     # static part of uncertainty

    if isinstance(Utheta, np.ndarray):
        unc = np.empty_like(y)

        # use extended signal to match assumption of stationary signal prior to first entry
        xlow_extended = np.append(np.full(Ntheta - 1, xlow[0]), xlow)
        
        for m in range(len(xlow)):
            # extract necessary part from input signal
            XL = xlow_extended[m : m + Ntheta, np.newaxis]
            unc[m] = XL.T.dot(np.flip(Utheta).dot(XL))  # apply formula from paper
    else:
        unc = np.zeros_like(y)
    
    ux = np.sqrt(np.abs(UncCov + unc))
    ux = np.roll(ux, -int(shift))  # correct for delay

    return x, ux.flatten()  # flatten in case that we still have 2D array


def IIRuncFilter(x, noise, b, a, Uab):
    """
    Uncertainty propagation for the signal x and the uncertain IIR filter (b,a)

    Parameters
    ----------
    x: np.ndarray
        filter input signal
    noise: float
        signal noise standard deviation
    b: np.ndarray
        filter numerator coefficients
    a: np.ndarray
        filter denominator coefficients
    Uab: np.ndarray
        covariance matrix for (a[1:],b)

    Returns
    -------
    y: np.ndarray
        filter output signal
    Uy: np.ndarray
        uncertainty associated with y

    References
    ----------
        * Link and Elster [Link2009]_

    """

    if not isinstance(noise, np.ndarray):
        noise = noise * np.ones_like(x)  # translate iid noise to vector

    p = len(a) - 1

    # Adjust dimension for later use.
    if not len(b) == len(a):
        b = np.hstack((b, np.zeros((len(a) - len(b),))))

    # From discrete-time transfer function to state space representation.
    [A, bs, c, b0] = tf2ss(b, a)

    A = np.matrix(A)
    bs = np.matrix(bs)
    c = np.matrix(c)

    phi = np.zeros((2 * p + 1, 1))
    dz = np.zeros((p, p))
    dz1 = np.zeros((p, p))
    z = np.zeros((p, 1))
    P = np.zeros((p, p))

    y = np.zeros((len(x),))
    Uy = np.zeros((len(x),))

    Aabl = np.zeros((p, p, p))
    for k in range(p):
        Aabl[0, k, k] = -1

    # implementation of the state-space formulas from the paper
    for n in range(len(y)):
        for k in range(p):  # derivative w.r.t. a_1,...,a_p
            dz1[:, k] = A * dz[:, k] + np.squeeze(Aabl[:, :, k]) * z
            phi[k] = c * dz[:, k] - b0 * z[k]
        phi[p + 1] = -np.matrix(a[1:]) * z + x[n]  # derivative w.r.t. b_0
        for k in range(p + 2, 2 * p + 1):  # derivative w.r.t. b_1,...,b_p
            phi[k] = z[k - (p + 1)]
        P = A * P * A.T + noise[n] ** 2 * (bs * bs.T)
        y[n] = c * z + b0 * x[n]
        Uy[n] = phi.T * Uab * phi + c * P * c.T + b[0] ** 2 * noise[n] ** 2
        z = A * z + bs * x[n]  # update of the state equations
        dz = dz1

    Uy = np.sqrt(np.abs(Uy))  # calculate point-wise standard uncertainties

    return y, Uy
