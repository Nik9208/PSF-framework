import sys
import platform
import os

def generate_environment_md():
    try:
        import wfdb
        import numpy as np
        import pandas as pd
        import scipy
        import sklearn
        import matplotlib
        
        env_md = f"""# Environment Log

**Python:** {sys.version.split()[0]}
**OS:** {platform.system()} {platform.release()}
**ICCS version:** v0.3.1 (frozen)

## Packages
- wfdb: {wfdb.__version__}
- numpy: {np.__version__}
- pandas: {pd.__version__}
- scipy: {scipy.__version__}
- scikit-learn: {sklearn.__version__}
- matplotlib: {matplotlib.__version__}
"""
        with open("environment.md", "w") as f:
            f.write(env_md)
        print("environment.md successfully generated with installed package versions.")
    except ImportError as e:
        print(f"Error: Missing dependency ({e}).")
        print("Please install the dependencies by running:")
        print("python -m pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure working directory is correct
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_environment_md()
