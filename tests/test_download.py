import pytest
import numpy as np
from searchlights import download_searchlights


class Test_download_searchlights_exceptions:
    def test_lr(self):
        with pytest.raises(ValueError):
            download_searchlights('lr', 20, 5)

    def test_radius(self):
        with pytest.raises(ValueError):
            download_searchlights('l', 25, 5)

    def test_icoorder(self):
        with pytest.raises(ValueError):
            download_searchlights('l', 20, 5.5)


def test_download_searchlights():
    sls1, dists1 = download_searchlights('l', 20, 5)
    sls2, dists2 = download_searchlights('l', 20, 5)
    assert all([np.all(sl1 == sl2) for sl1, sl2 in zip(sls1, sls2)])
    assert all([np.all(d1 == d2) for d1, d2 in zip(dists1, dists2)])
