import numpy as np
import pandas as pd
from sklearn.covariance import GraphicalLassoCV

true_cov = np.array([[0.8, 0.0, 0.2, 0.0], [0.0, 0.4, 0.0, 0.0], [0.2, 0.0, 0.3, 0.1], [0.0, 0.0, 0.1, 0.7]])
np.random.seed(0)
X = np.random.multivariate_normal(mean=[0, 0, 0, 0], cov=true_cov, size=200)
cov0 = GraphicalLassoCV(alphas=2, n_refinements=1).fit(X)
cov1 = GraphicalLassoCV(alphas=[0.1, 0.5, 1.0], cv=5).fit(X)

pd.set_option("display.float_format", "{:.3f}".format)

print("True      covariance matrix                   :\n", pd.DataFrame(true_cov))
print("Estimated covariance matrix, empirical        :\n", pd.DataFrame(np.cov(X, rowvar=False)))
print("Estimated covariance matrix, GraphicalLassoCV0:\n", pd.DataFrame(cov0.covariance_))
print("Estimated covariance matrix, GraphicalLassoCV1:\n", pd.DataFrame(cov1.covariance_))

split_score = pd.DataFrame(
    {
        "split_0": cov1.cv_results_["split0_test_score"],
        "split_1": cov1.cv_results_["split1_test_score"],
        "split_2": cov1.cv_results_["split2_test_score"],
        "split_3": cov1.cv_results_["split3_test_score"],
        "split_4": cov1.cv_results_["split4_test_score"],
    }, index=cov1.cv_results_["alphas"],
).T
print("Cross-validation scores for each split:\n", split_score)

breakpoint()