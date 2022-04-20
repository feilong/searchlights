import numpy as np
from searchlights import get_searchlights


def test_resolution():
    conditions = [
        [3, (588, 587)],
        [4, (2343, 2344)],
        [5, (9372, 9370)],
        # [6, (37487, 37482)],
    ]
    for icoorder, nvs in conditions:
        for lr, nv in zip('lr', nvs):
            sls = get_searchlights(lr, 20, 'fsaverage', icoorder)
            assert len(sls) == nv
            cat = np.concatenate(sls)
            assert cat.max() == nv - 1
            assert cat.min() == 0

    for icoorder in [3, 4, 5]:
        nv = 4**icoorder * 10 + 2
        for lr in 'lr':
            sls = get_searchlights(lr, 20, 'none', icoorder)
            assert len(sls) == nv
            cat = np.concatenate(sls)
            assert cat.max() == nv - 1
            assert cat.min() == 0
