r"""
MMV with non-negative norms
===========================
In this tutorial we will use the ``spg_mmv`` solver which solves a
multi-measurement vector basis pursuit denoise problem. Both standard L12
and L12non-negative norms will be compared. The latter set of norms is used in
case allowsour solution to have only positive values in case we have access to
such a kind of prior information.
"""
import numpy as np
import matplotlib.pyplot as plt

from spgl1 import spg_mmv
from spgl1 import norm_l12nn_primal, norm_l12nn_dual, norm_l12nn_project


###############################################################################
# Let's first import our data, matrix operator and weights
data = np.load('../testdata/mmvnn.npz')

A = data['A']
B = data['B']
weights = data['weights']

###############################################################################
# We apply unweighted inversions with and without non-negative
# norms.
X, _, _, info = spg_mmv(A, B, 0.5, iter_lim=100, verbosity=0)

XNN, _, _, infoNN = spg_mmv(A, B, 0.5, iter_lim=100, verbosity=0,
                            project=norm_l12nn_project,
                            primal_norm=norm_l12nn_primal,
                            dual_norm=norm_l12nn_dual)
print('Negative X - MMV:', np.any(X < 0))
print('Negative X - MMVNN:', np.any(XNN < 0))
print('Residual norm - MMV:', info['rnorm'])
print('Residual norm - MMVNN:', infoNN['rnorm'])

plt.figure()
plt.plot(X[:, 0], 'k', label='Coefficients')
plt.plot(XNN[:, 0], '--r', label='Coefficients NN')
plt.legend()
plt.title('Unweighted Basis Pursuit with Multiple Measurement Vectors')

plt.figure()
plt.plot(X[:, 1], 'k', label='Coefficients')
plt.plot(XNN[:, 1], '--r', label='Coefficients NN')
plt.legend()
plt.title('Unweighted Basis Pursuit with Multiple Measurement Vectors')

###############################################################################
# We repeat the same steps with weighted norms.
X, _, _, info = spg_mmv(A, B, 0.5, iter_lim=100,
                        weights=np.array(weights), verbosity=0)
XNN, _, _, infoNN = spg_mmv(A, B, 0.5, iter_lim=100, verbosity=0,
                            weights=np.array(weights),
                            project=norm_l12nn_project,
                            primal_norm=norm_l12nn_primal,
                            dual_norm=norm_l12nn_dual)
print('Negative X - MMV:', np.any(X < 0))
print('Negative X - MMVNN:', np.any(XNN < 0))
print('Residual norm - MMV:', info['rnorm'])
print('Residual norm - MMVNN:', infoNN['rnorm'])

plt.figure()
plt.plot(X[:, 0], 'k', label='Coefficients')
plt.plot(XNN[:, 0], '--r', label='Coefficients NN')
plt.legend()
plt.title('Weighted Basis Pursuit with Multiple Measurement Vectors')

plt.figure()
plt.plot(X[:, 1], 'k', label='Coefficients')
plt.plot(XNN[:, 1], '--r', label='Coefficients NN')
plt.legend()
plt.title('Weighted Basis Pursuit with Multiple Measurement Vectors')
