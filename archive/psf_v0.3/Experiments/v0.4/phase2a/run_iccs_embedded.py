import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))
from psf.iccs import ICCS
from delay_embedder import embed_signal

def run_iccs_embedded(signal, m, tau):
    """
    Wrapper around frozen ICCS v0.3.1 with external delay embedding.
    """
    iccs = ICCS()
    try:
        if m == 1:
            X_geom = signal
        else:
            X_geom = embed_signal(signal, m, tau)
            
        profile = iccs.fit(X_geom)
        
        return {
            "M": profile["M"],
            "D_local": profile["D_local"],
            "TE_forward": profile["TE_forward"]
        }
    except Exception as e:
        return {"error": str(e)}
