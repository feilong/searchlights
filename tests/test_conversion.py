import numpy as np
from searchlights import load_searchlights, convert_searchlights


def test_load_searchlights():
    for lr in 'lr':
        sls1, dists1 = load_searchlights(lr, 20, 5)
        for radius in [20, 30]:
            for icoorder in [5, 6]:
                sls_all, dists_all = load_searchlights(lr, radius, icoorder)
                sls2, dists2 = convert_searchlights(sls_all, dists_all, lr, 20, 'none', 5)
                for sl1, sl2, d1, d2 in zip(sls1, sls2, dists1, dists2):
                    np.testing.assert_array_equal(sl1, sl2)
                    np.testing.assert_array_equal(d1, d2)


def test_convert_searchlights():
    conditions = [
        ['fsaverage5', (9354, 9361)],
        ['fsaverage6', (9372, 9369)],
        ['fsaverage', (9372, 9370)],
    ]
    for mask_space, nvs in conditions:
        for lr, nv in zip('lr', nvs):
            sls1, dists1 = load_searchlights(lr, 20, 5)
            sls, dists = convert_searchlights(sls1, dists1, lr, 20, mask_space, 5)
            assert len(sls) == nv
            cat = np.concatenate(sls)
            assert cat.max() == nv - 1
            assert cat.min() == 0
            for sl, d in zip(sls, dists):
                assert len(sl) == len(d)
