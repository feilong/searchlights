import os
import numpy as np

DIR = os.path.dirname(os.path.realpath(__file__))


def get_mask(lr, mask_type='fsaverage', icoorder=None):
    fn = os.path.join(DIR, 'data', f'mask_{mask_type}_{lr}h.npy')
    mask = np.load(fn)
    if icoorder is not None:
        nv = 4**icoorder * 10 + 2
        mask = mask[:nv]
    return mask


def get_searchlights(lr, radius, mask_type='fsaverage', icoorder=5, return_distances=False):
    assert radius <= 20
    assert icoorder <= 5
    assert mask_type in ['fsaverage', 'fsaverage6', 'fsaverage5', 'none']

    if mask_type != 'none':
        mask = get_mask(lr, mask_type=mask_type, icoorder=icoorder)
        cortical_indices = np.where(mask)[0]
        mapping = np.cumsum(mask) - 1
    else:
        nv = 4**icoorder * 10 + 2
        cortical_indices = np.arange(nv)
        mapping = None

    npz = np.load(os.path.join(DIR, 'data', f'sls_fsaverage_{lr}h_20mm_icoorder5.npz'))

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
