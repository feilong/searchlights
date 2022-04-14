import os
import numpy as np

DIR = os.path.dirname(os.path.realpath(__file__))

__all__ = ['get_searchlights', 'get_mask']


def get_mask(lr, mask_space='fsaverage', icoorder=None):
    """Get the boolean cortical mask.

    Parameters
    ----------
    lr : {'l', 'r'}
        Get the mask for the left ('l') or right ('r') hemisphere.
    mask_space : {'fsaverage', 'fsaverage6', 'fsaverage5', 'none'}, optional
        Which cortical mask to get. Note that the masks slightly differ
        for different ``mask_space``, even at the same resolution.
    icoorder : int or None
        The spatial resolution of the output mask. If it's an integer, the
        resolution of the output mask will be reduced so that it won't be
        higher than the desired ``icoorder``. If it's None, then the
        resolution will not be reduced.

    Returns
    -------
    mask : ndarray
        A boolean array. The value is True for cortical vertices and False
        for non-cortical vertices. The resolution is determined by
        ``icoorder``.
    """
    fn = os.path.join(DIR, 'data', f'mask_{mask_space}_{lr}h.npy')
    mask = np.load(fn)
    if icoorder is not None:
        nv = 4**icoorder * 10 + 2
        mask = mask[:nv]
    return mask


def get_searchlights(
        lr, radius, mask_space='fsaverage', icoorder=5, return_distances=False):
    """Get searchlight indices based on precomputed files.

    Parameters
    ----------
    lr : {'l', 'r'}
        Get the searchlights for the left ('l') or right ('r') hemisphere.
    radius : int or float
        The searchlight radius.
    mask_space : {'fsaverage', 'fsaverage6', 'fsaverage5', 'none'}, optional
        Which cortical mask to be used for the searchlights. The mask
        should be the same as the one applied to brain data matrices.
    icoorder : int, default=5
        The spatial resolution of cortical vertices. This should also be
        the same as that of your data matrices.
    return_distances : bool, default=False
        Whether to also return the distances to the searchlight center
        (True) or not (False). If ``return_distances=True``, two lists are
        returned instead of one.

    Returns
    -------
    sls : list of ndarray
        Each entry is an ndarray of integers, which are the indices of the
        vertices in a searchlight.
    dists : list of ndarray
        Each entry is an ndarray of float numbers, which are the distances
        between vertices in a searchlight and the center of the
        searchlight. The order of vertices are the same as ``sls``. Only
        returned when ``return_distances=True``.
    """
    assert radius <= 20
    assert icoorder <= 5
    assert mask_space in ['fsaverage', 'fsaverage6', 'fsaverage5', 'none']

    if mask_space != 'none':
        mask = get_mask(lr, mask_space=mask_space, icoorder=icoorder)
        cortical_indices = np.where(mask)[0]
        mapping = np.cumsum(mask) - 1
    else:
        nv = 4**icoorder * 10 + 2
        cortical_indices = np.arange(nv)
        mapping = None

    npz = np.load(os.path.join(
        DIR, 'data', f'sls_fsaverage_{lr}h_20mm_icoorder5.npz'))

    sls_all = np.array_split(npz['concatenated_searchlights'], npz['sections'])
    dists_all = np.array_split(npz['concatenated_distances'], npz['sections'])

    sls, dists = [], []
    for i, (sl, d) in enumerate(zip(sls_all, dists_all)):
        if i in cortical_indices:
            m = np.logical_and(np.isin(sl, cortical_indices), d <= radius)
            if mapping is None:
                sls.append(sl[m])
            else:
                sls.append(mapping[sl[m]])
            dists.append(d[m])

    if return_distances:
        return sls, dists

    return sls
