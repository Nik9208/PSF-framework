import numpy as np
from sklearn.neighbors import NearestNeighbors

def compute_local_dimension(X, k=10):
    """
    Maximum Likelihood Estimator of Intrinsic Dimensionality (Levina & Bickel, 2004).
    Resolves Representation Ambiguity.
    """
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)
        
    if len(X) <= k:
        return 0.0
    
    # We query k+1 neighbors because the first neighbor is the point itself (distance 0)
    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='auto').fit(X)
    distances, _ = nbrs.kneighbors(X)
    
    # Exclude the point itself
    distances = distances[:, 1:]
    
    # To avoid log(0) or div by 0, add small epsilon to distances
    distances = distances + 1e-10
    
    # R_k is the distance to the k-th neighbor
    R_k = distances[:, -1]
    
    # Compute the term for each point
    # d(x_i) = [ 1/(k-1) * sum_{j=1}^{k-1} log(R_k / R_j) ]^{-1}
    log_ratios = np.log(R_k[:, np.newaxis] / distances[:, :-1])
    
    # Mean over the k-1 neighbors
    mean_log_ratios = np.mean(log_ratios, axis=1)
    
    # Avoid division by zero if all neighbors are at exactly the same distance
    valid = mean_log_ratios > 0
    
    local_dims = np.zeros(len(X))
    local_dims[valid] = 1.0 / mean_log_ratios[valid]
    
    # Return the global average of local dimensions
    return float(np.mean(local_dims))
