import os
from glob import glob
import importlib
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


def load_npz(npz_fn):
    npz = np.load(npz_fn)
    sls = np.array_split(npz['concatenated_searchlights'], npz['sections'])
    dists = np.array_split(npz['concatenated_distances'], npz['sections'])
    return sls, dists


def download_searchlights(lr, radius, icoorder):
    if lr not in ['l', 'r']:
        raise ValueError("The `lr` parameter can only be 'l' or 'r'.")
    if radius not in [20, 30]:
        raise ValueError("The `radius` parameter can only be 20 or 30.")
    if icoorder not in [5, 6]:
        raise ValueError("The `icoorder` parameter can only be 5 or 6.")
    if importlib.util.find_spec('datalad') is None:
        raise ModuleNotFoundError(
            'datalad package not found, which is required to download '
            'additional data. See https://www.datalad.org/#install for '
            'instructions on installing datalad.')

    import datalad.api as dl

    dset = dl.install(
        path=os.path.join(DIR, 'datalad'),
        source='https://gin.g-node.org/feilong/searchlights')

    fn = f'sls_fsaverage_{lr}h_{radius}mm_icoorder{icoorder}.npz'
    result = dset.get(fn)[0]

    if result['status'] not in ['ok', 'notneeded']:
        raise ValueError(
            f"datalad `get` status is {result['status']}, likely due to "
            "problems downloading the file.")

    sls, dists = load_npz(result['path'])
    return sls, dists


def load_searchlights(lr, radius, icoorder):
    basename = f'sls_fsaverage_{lr}h_{radius}mm_icoorder{icoorder}.npz'
    fn1 = os.path.join(DIR, 'data', basename)
    if os.path.exists(fn1):
        sls, dists = load_npz(fn1)
        return sls, dists

    sls, dists = download_searchlights(lr, radius, icoorder)
    return sls, dists


def convert_searchlights(sls, dists, lr, radius, mask_space, icoorder):
    """
    Convert higher-resolution/larger-radius/unmasked searchlights to
    lower-resolution/smaller-radius/masked.

    Parameters
    ----------
    sls : list of ndarray
        Each entry is an ndarray of integers, which are the indices of the
        vertices in a searchlight.
    dists : list of ndarray
        Each entry is an ndarray of float numbers, which are the distances
        between vertices in a searchlight and the center of the
        searchlight. The order of vertices are the same as ``sls``.
    lr : {'l', 'r'}
        Whether the searchlights are for the left ('l') or right ('r')
        hemisphere.
    radius : int or float
        The searchlight radius in mm.
    mask_space : {'fsaverage', 'fsaverage6', 'fsaverage5', 'none'}, optional
        Which cortical mask to be used for the searchlights. The mask
        should be the same as the one applied to brain data matrices.
    icoorder : int, default=5
        The spatial resolution of cortical vertices. This should also be
        the same as that of your data matrices.

    Returns
    -------
    sls_new : list of ndarray
        The new list of searchlight indices after conversion.
    dists_new : list of ndarray
        The new list of distnaces to searchlight center after conversion.
    """
    if mask_space != 'none':
        mask = get_mask(lr, mask_space=mask_space, icoorder=icoorder)
        cortical_indices = np.where(mask)[0]
        mapping = np.cumsum(mask) - 1
    else:
        nv = 4**icoorder * 10 + 2
        cortical_indices = np.arange(nv)
        mapping = None

    sls_new, dists_new = [], []
    for i, (sl, d) in enumerate(zip(sls, dists)):
        if i in cortical_indices:
            m = np.logical_and(np.isin(sl, cortical_indices), d <= radius)
            if mapping is None:
                sls_new.append(sl[m])
            else:
                sls_new.append(mapping[sl[m]])
            dists_new.append(d[m])

    return sls_new, dists_new


def get_searchlights(
        lr, radius, mask_space='fsaverage', icoorder=5,
        return_distances=False, cache=False):
    """Get searchlight indices based on precomputed files.

    Parameters
    ----------
    lr : {'l', 'r'}
        Get the searchlights for the left ('l') or right ('r') hemisphere.
    radius : int or float
        The searchlight radius in mm.
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
    cache : bool, default=False
        Whether to store computed searchlights as an npz file for future
        use.

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
    if isinstance(radius, float) and float(int(radius)) == radius:
        radius = int(radius)  # to avoid duplicate files, e.g., 20 and 20.0

    if mask_space == 'none':
        base_name = f'sls_fsaverage_{lr}h_{radius}mm_icoorder{icoorder}.npz'
    else:
        base_name = 'sls_fsaverage_'\
            f'{lr}h_{radius}mm_icoorder{icoorder}_{mask_space}-mask.npz'

    # Load the npz file if it already exists
    npz_fn = os.path.join(DIR, 'data', base_name)
    if os.path.exists(npz_fn):
        sls, dists = load_npz(npz_fn)
        if return_distances:
            return sls, dists
        return sls

    npz_fn2 = os.path.join(DIR, 'datalad', base_name)
    if os.path.exists(npz_fn2):
        sls, dists = load_searchlights(lr, radius, icoorder)
        if return_distances:
            return sls, dists
        return sls


    # Check the parameters.
    if importlib.util.find_spec('datalad') is None:
        assert radius <= 20, "Maximum supported searchlight radius is 20 "\
            "without datalad."
        assert icoorder <= 5, "Maximum supported icoorder is 5 without "\
            "datalad."
    else:
        assert radius <= 30, "Maximum supported searchlight radius is 30."
        assert icoorder <= 6, "Maximum supported icoorder is 6."
    assert mask_space in ['fsaverage', 'fsaverage6', 'fsaverage5', 'none']


    # Convert from precomputed searchlights
    radius_ = [_ for _ in [20, 30] if radius <= _][0]
    icoorder_ = [_ for _ in [5, 6] if icoorder <= _][0]
    all_sls, all_dists = load_searchlights(lr, radius_, icoorder_)
    sls, dists = convert_searchlights(
        all_sls, all_dists, lr, radius, mask_space, icoorder)

    if cache:
        output = {
            'concatenated_searchlights': np.concatenate(sls),
            'concatenated_distances': np.concatenate(dists),
            'sections': np.cumsum([len(_) for _ in sls])[:-1],
        }
        np.savez(npz_fn, **output)

    if return_distances:
        return sls, dists

    return sls


def list_cache_files():
    original_files = [
        'sls_fsaverage_lh_20mm_icoorder5.npz',
        'sls_fsaverage_rh_20mm_icoorder5.npz',
    ]
    fns = sorted(glob(os.path.join(DIR, 'data', '*.npz')))
    fns = [_ for _ in fns if os.path.basename(_) not in original_files]
    return fns
