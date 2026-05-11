import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf

pd.set_option("display.float_format", "{:.3f}".format)

real_cov = np.array([[0.4, 0.2], [0.2, 0.8]])
np.random.seed(0)
X = np.random.multivariate_normal(mean=[0, 0], cov=real_cov, size=50)
cov = LedoitWolf().fit(X)


print("Real        covariance matrix:\n", pd.DataFrame(real_cov), "\n")
print("Sample      covariance matrix:\n", pd.DataFrame(np.cov(X, rowvar=False)), "\n")
print("Ledoit-Wolf covariance matrix :\n", pd.DataFrame(cov.covariance_), "\n")
