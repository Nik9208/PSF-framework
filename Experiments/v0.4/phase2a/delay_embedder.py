import numpy as np

def embed_signal(X, m, tau):
    """
    Takens' Delay Embedding.
    Returns an (N - (m-1)*tau) x m matrix.
    If m=1, returns X as a column vector.
    """
    X = np.asarray(X)
    n = len(X)
    if m == 1:
        return X.reshape(-1, 1)
        
    eff_length = n - (m - 1) * tau
    if eff_length <= 0:
        raise ValueError("Signal too short for given m and tau.")
        
    embedded = np.zeros((eff_length, m))
    for i in range(m):
        embedded[:, i] = X[i*tau : i*tau + eff_length]
    return embedded
