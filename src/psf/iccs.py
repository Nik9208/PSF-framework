from .memory import compute_memory_profile
from .geometry import compute_local_dimension
from .causal import compute_causal_fingerprint

class ICCSProfile:
    def __init__(self, M, D_local, TE_forward, TE_reverse, CMI):
        self.vector = {
            "M": M,
            "D_local": D_local,
            "TE_forward": TE_forward,
            "TE_reverse": TE_reverse,
            "CMI": CMI
        }
        
    def __repr__(self):
        return str(self.vector)
        
    def __getitem__(self, key):
        return self.vector[key]
        
    def __contains__(self, key):
        return key in self.vector

class ICCS:
    def __init__(self, max_k_memory=10, k_neighbors_mi=5, k_neighbors_id=10):
        self.max_k_memory = max_k_memory
        self.k_neighbors_mi = k_neighbors_mi
        self.k_neighbors_id = k_neighbors_id
        
    def fit(self, X, Y=None, Z=None):
        """
        Computes the Information-theoretic Causal Complexity Score vector.
        If X is a univariate time series, Y and Z will be generated via delay embedding in the causal layer.
        If X is multivariate, geometry uses the full space, but memory and causal default to the first dimension.
        """
        X_geom = X
        if len(X.shape) > 1:
            X = X[:, 0]
            
        M = compute_memory_profile(X, max_k=self.max_k_memory, n_neighbors=self.k_neighbors_mi)
        D_local = compute_local_dimension(X_geom, k=self.k_neighbors_id)
        te_fwd, te_rev, cmi = compute_causal_fingerprint(X, Y, Z)
        
        return ICCSProfile(
            M=M,
            D_local=D_local,
            TE_forward=te_fwd,
            TE_reverse=te_rev,
            CMI=cmi
        )
