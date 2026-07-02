import sys
import os

# Ensure we can import psf from the root directory
# PSF-framework/Experiments/v0.4/run_iccs.py -> PSF-framework/src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from psf.iccs import ICCS

def run_iccs(signal, y=None, z=None):
    """
    Wrapper around frozen ICCS v0.3.1.
    No methodology changes should be made here.
    """
    iccs = ICCS()
    try:
        profile = iccs.fit(signal, y, z)
        return {
            "M": profile["M"],
            "D_local": profile["D_local"],
            "TE_forward": profile["TE_forward"],
            "TE_reverse": profile["TE_reverse"],
            "CMI": profile["CMI"]
        }
    except Exception as e:
        return {"error": str(e)}
