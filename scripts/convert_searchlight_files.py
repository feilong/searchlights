import os
from glob import glob
import numpy as np


if __name__ == '__main__':
    for fn in sorted(glob('sls_*.npz')):
        out_fn = os.path.join('../src/searchlights/data', fn)
        if os.path.exists(out_fn):
            continue

        npz = np.load(fn, allow_pickle=True, encoding='bytes')
        sls, dists = npz['sls'], npz['dists']

        out_sls, out_dists = [], []
        for sl, d in zip(sls, dists):
            sort_idx = np.argsort(d)
            out_sls.append(sl[sort_idx])
            out_dists.append(d[sort_idx])

        concatenated_sls = np.concatenate(out_sls)
        print(concatenated_sls.max())
        concatenated_sls = concatenated_sls.astype(np.uint16)
        print(concatenated_sls.max())

        sections = np.cumsum([len(_) for _ in sls][:-1])
        print(sections.max())
        sections = sections.astype(np.uint32)
        print(sections.max())

        concatenated_dists = np.concatenate(out_dists)

        np.savez(
            out_fn,
            concatenated_searchlights=concatenated_sls,
            concatenated_distances=concatenated_dists, 
            sections=sections)

        os.remove(fn)
