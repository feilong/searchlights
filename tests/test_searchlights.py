import os
import pytest
import importlib
import numpy as np
from searchlights import get_searchlights, list_cache_files


def test_compare_with_legacy_files():
    legacy_dir = os.path.expanduser('~/github/hyperalignment/searchlights')
    if not os.path.exists(legacy_dir):
        pytest.skip("Legacy files does not exist.")

    for mask_space in ['fsaverage', 'fsaverage5']:
        for lr in 'lr':
            for radius in [7, 10, 13, 15, 20]:
                fn = os.path.join(
                    legacy_dir,
                    f'{mask_space}_{lr}h_{radius}mm_icoorder5.npz')
                if not os.path.exists(fn):
                    continue
                print(lr, radius, mask_space)

                npz = np.load(fn)
                sls1 = np.array_split(
                    npz['concatenated'], npz['sections'])
                dists1 = np.array_split(
                    npz['concatenated_dists'], npz['sections'])
                sls2, dists2 = get_searchlights(
                    lr, radius, mask_space=mask_space, return_distances=True)

                for sl1, sl2, d1, d2 in zip(sls1, sls2, dists1, dists2):
                    np.testing.assert_array_equal(sl1, sl2)
                    np.testing.assert_array_equal(d1, d2)


def test_searchlights_without_masking():
    mask_space = 'none'
    radius = 20
    for lr in 'lr':
        sls = get_searchlights(
            lr, radius, mask_space=mask_space, return_distances=False)
        cat = np.concatenate(sls)
        assert len(sls) == 10242
        assert cat.min() == 0
        assert cat.max() == 10241


def test_various_mask_spaces():
    radius = 20
    conditions = [
        ['fsaverage5', (9354, 9361)],
        ['fsaverage6', (9372, 9369)],
        ['fsaverage', (9372, 9370)],
    ]
    for mask_space, nvs in conditions:
        for lr, nv in zip('lr', nvs):
            sls, dists = get_searchlights(
                lr, radius, mask_space=mask_space, return_distances=True)
            cat = np.concatenate(sls)
            assert len(sls) == nv
            assert cat.max() == nv - 1
            assert cat.min() == 0


def test_datalad_files():
    if importlib.util.find_spec('datalad') is None:
        pytest.skip("Skip downloading tests: datalad not installed.")
    for lr in 'lr':
        sls, dists = get_searchlights(
            lr, 30, 'none', 5, return_distances=True, cache=False)
        sls2 = get_searchlights(
            lr, 30.0, 'none', 5, return_distances=False, cache=False)
        for sl1, sl2 in zip(sls, sls2):
            np.testing.assert_array_equal(sl1, sl2)


def test_original_data_files():
    for lr in 'lr':
        sls, dists = get_searchlights(
            lr, 20, 'none', 5, return_distances=True, cache=False)
        sls2 = get_searchlights(
            lr, 20.0, 'none', 5, return_distances=False, cache=False)
        for sl1, sl2 in zip(sls, sls2):
            np.testing.assert_array_equal(sl1, sl2)


def test_save_files():
    for fn in list_cache_files():
        os.remove(fn)

    for lr in 'lr':
        sls, dists = get_searchlights(
            lr, 10, 'fsaverage', 5, return_distances=True, cache=True)
