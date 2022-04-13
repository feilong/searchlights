import os
import pytest
import numpy as np
from searchlights import get_searchlights


def test_compare_with_legacy_files():
    legacy_dir = os.path.expanduser('~/github/hyperalignment/searchlights')
    if not os.path.exists(legacy_dir):
        pytest.skip("Legacy files does not exist.")

    for mask_type in ['fsaverage', 'fsaverage5']:
        for lr in 'lr':
            for radius in [7, 10, 13, 15, 20]:
                fn = os.path.join(
                    legacy_dir,
                    f'{mask_type}_{lr}h_{radius}mm_icoorder5.npz')
                if not os.path.exists(fn):
                    continue
                print(lr, radius, mask_type)

                npz = np.load(fn)
                sls1 = np.array_split(
                    npz['concatenated'], npz['sections'])
                dists1 = np.array_split(
                    npz['concatenated_dists'], npz['sections'])
                sls2, dists2 = get_searchlights(
                    lr, radius, mask_type=mask_type, return_distances=True)

                for sl1, sl2, d1, d2 in zip(sls1, sls2, dists1, dists2):
                    np.testing.assert_array_equal(sl1, sl2)
                    np.testing.assert_array_equal(d1, d2)


def test_searchlights_without_masking():
    mask_type = 'none'
    radius = 20
    for lr in 'lr':
        sls = get_searchlights(
            lr, radius, mask_type=mask_type, return_distances=False)
        cat = np.concatenate(sls)
        assert len(sls) == 10242
        assert cat.min() == 0
        assert cat.max() == 10241
