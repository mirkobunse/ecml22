import numpy as np


# smoothing approximation
def smoothness(p):
    return 0.5 * sum((-p_prev + 2*p_i - p_next)**2 for p_prev, p_i, p_next in zip(p[:-2], p[1:-1], p[2:]))


def _check_arrays(prevs):
    prevs = np.asarray(prevs)
    if prevs.ndim==1:
        prevs = prevs.reshape(1,-1)
    return prevs


# mean normalized match distance
def mnmd(prevs, prevs_hat):
    prevs = _check_arrays(prevs)
    prevs_hat = _check_arrays(prevs_hat)
    assert prevs.shape == prevs_hat.shape, f'wrong shape; found {prevs.shape} and {prevs_hat.shape}'

    nmds = [nmd(p, p_hat) for p, p_hat in zip(prevs, prevs_hat)]
    return np.mean(nmds)


# normalized match distance
def nmd(prev, prev_hat):
    n = len(prev)
    return (1./(n-1))*mdpa(prev, prev_hat)

# MDPA implementation of the EMD; see jl/src/Util.jl in this repository
def mdpa(a, b):
    assert len(a) == len(b), "histograms have to have the same length"
    assert np.isclose(sum(a), sum(b)), "histograms have to have the same mass (difference is $(sum(a)-sum(b))"

    # algorithm 1 in [cha2002measuring]
    prefixsum = 0.0
    distance  = 0.0
    for i in range(len(a)):
        prefixsum += a[i] - b[i]
        distance += abs(prefixsum)

    return distance / sum(a)  # the normalization is a fix to the original MDPA

