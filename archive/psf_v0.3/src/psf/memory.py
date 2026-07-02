import numpy as np
from sklearn.feature_selection import mutual_info_regression

def estimate_mi(source, target, n_neighbors=5):
    """Estimate Mutual Information between source and target."""
    if len(source) < 2: return 0.0
    s = source.reshape(-1, 1)
    mi = mutual_info_regression(s, target, n_neighbors=n_neighbors)
    return float(mi[0])

def compute_memory_profile(X, max_k=10, n_neighbors=5):
    """
    Computes the predictive memory profile M(k) for a 1D time series.
    Returns the area under the M(k) curve as a scalar representation.
    """
    profile = []
    for k in range(1, max_k + 1):
        mi = estimate_mi(X[:-k], X[k:], n_neighbors=n_neighbors)
        profile.append(mi)
    return float(sum(profile))
