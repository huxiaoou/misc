import warnings
import numpy as np

# Example code that might produce the warning
a = np.array([1.0, 0])
b = np.array([2.0, 1.0])

with warnings.catch_warnings():
    warnings.filterwarnings("error", category=RuntimeWarning)
    try:
        result = b / a
    except RuntimeWarning as e:
        print(f"Caught RuntimeWarning: {e}")
