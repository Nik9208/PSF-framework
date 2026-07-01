import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import mutual_info_regression

def _estimate_mi(source, target):
    s = source.reshape(-1, 1)
    return float(mutual_info_regression(s, target)[0])

def _compute_residual(target, predictor):
    model = LinearRegression()
    model.fit(predictor.reshape(-1, 1), target)
    return target - model.predict(predictor.reshape(-1, 1))

def compute_causal_fingerprint(X, Y=None, Z=None):
    """
    Computes Transfer Entropy (TE+, TE-) and Conditional Mutual Information (CMI) proxies.
    If Y and Z are not provided, assumes auto-causality (delay embedding structure).
    """
    # For a univariate time series, we construct Y and Z from delays
    if Y is None:
        Y = np.roll(X, -1)
    if Z is None:
        Z = np.roll(X, -2)
        
    X_prev, X_curr = X[:-1], X[1:]
    Y_prev, Y_curr = Y[:-1], Y[1:]
    Z_prev = Z[:-1]
    
    # Truncate to match lengths
    min_len = min(len(X_curr), len(Y_curr), len(Z_prev))
    X_prev, X_curr = X_prev[:min_len], X_curr[:min_len]
    Y_prev, Y_curr = Y_prev[:min_len], Y_curr[:min_len]
    Z_prev = Z_prev[:min_len]

    # TE Proxies
    res_Y_given_Y = _compute_residual(Y_curr, Y_prev)
    TE_XY = _estimate_mi(X_prev, res_Y_given_Y)
    
    res_X_given_X = _compute_residual(X_curr, X_prev)
    TE_YX = _estimate_mi(Y_prev, res_X_given_X)
    
    # CMI Proxy
    res_X_given_Z = _compute_residual(X_curr, Z_prev)
    res_Y_given_Z = _compute_residual(Y_curr, Z_prev)
    CMI = _estimate_mi(res_X_given_Z, res_Y_given_Z)
    
    return float(TE_XY), float(TE_YX), float(CMI)
