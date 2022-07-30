import os
from glob import glob
import importlib
import numpy as np

from surface_spaces import get_cortical_mask

DIR = os.path.dirname(os.path.realpath(__file__))

__all__ = ['get_searchlights', 'convert_searchlights']


def convert_searchlights(sls, dists, radius, mask):
    """
    Convert larger-radius/unmasked searchlights to smaller-radius/masked.

    Parameters
    ----------
    sls : list of ndarray
        Each entry is an ndarray of integers, which are the indices of the
        vertices in a searchlight.
    dists : list of ndarray
        Each entry is an ndarray of float numbers, which are the distances
        between vertices in a searchlight and the center of the
        searchlight. The order of vertices are the same as ``sls``.
    radius : int or float
        The searchlight radius in mm.
    mask : ndarray
        A boolean ndarray indicating whether a vertex belongs to the cortex
        (True) or not (False).

    Returns
    -------
    sls_new : list of ndarray
        The new list of searchlight indices after conversion.
    dists_new : list of ndarray
        The new list of distnaces to searchlight center after conversion.
    """
    if mask is not None:
        cortical_indices = np.where(mask)[0]
        mapping = np.cumsum(mask) - 1

    sls_new, dists_new = [], []
    for i, (sl, d) in enumerate(zip(sls, dists)):
        if mask is None or i in cortical_indices:
            m = (d <= radius)
            if mask is not None:
                m = np.logical_and(np.isin(sl, cortical_indices), m)
                sls_new.append(mapping[sl[m]])
            else:
                sls_new.append(sl[m])
            dists_new.append(d[m])

    return sls_new, dists_new


def load_npz(npz_fn):
    npz = np.load(npz_fn)
    sls = np.array_split(npz['concatenated_searchlights'], npz['boundaries'])
    dists = np.array_split(npz['concatenated_distances'], npz['boundaries'])
    return sls, dists


def load_searchlights(lr, radius, space, geometry):
    npz_fn = os.path.join(DIR, 'data', f'{geometry}_dijkstra', f'{space}_{lr}h_{radius}mm.npz')
    sls, dists = load_npz(npz_fn)
    return sls, dists


def get_searchlights(lr, radius, space, geometry='on1031', mask=None):
    radius_ = 20
    sls, dists = load_searchlights(lr, radius_, space, geometry)
    if mask is not None:
        mask = get_cortical_mask(lr, space, mask)
    sls, dists = convert_searchlights(sls, dists, radius, mask)
    return sls, dists
