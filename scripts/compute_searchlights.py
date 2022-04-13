import os
import numpy as np
import nibabel as nib
from mvpa2.support.nibabel.surf import Surface


def compute_searchlights(
        lr, radius=20, icoorder=5, overwrite=False, surf_tmpl='fsaverage',
        fs_dir=os.path.expanduser('~/singularity_home/freesurfer/subjects')):
    """
    Notes
    -----
    The geometry of ``fsaverage`` in the most recent version of FreeSurfer
    (freesurfer-linux-centos7_x86_64-7.2.0-20210720-aa8f76b) is slightly
    different from the one we've been using
    (freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1-f53a55a). This
    difference can be ignored in most cases. However, the searchlights
    generated from different versions of ``fsaverage`` won't be identical.
    We keep using the same version we've been using to maximize
    replicability.
    """
    out_fn = 'sls_{surf_tmpl}_{lr}h_{radius}mm_icoorder{icoorder}.npz'\
        ''.format(**locals())
    if os.path.exists(out_fn) and not overwrite:
        return

    coords1, faces1 = nib.freesurfer.io.read_geometry(
        os.path.join(fs_dir, 'fsaverage', 'surf', lr+'h.white'))
    coords2, faces2 = nib.freesurfer.io.read_geometry(
        os.path.join(fs_dir, 'fsaverage', 'surf', lr+'h.pial'))
    np.testing.assert_array_equal(faces1, faces2)
    coords = (coords1.astype(np.float) + coords2.astype(np.float)) * 0.5
    surf = Surface(coords, faces1)

    sls = []
    dists = []

    nv = 4**icoorder * 10 + 2
    indices = np.arange(nv)

    for center in indices:
        pairs = surf.dijkstra_distance(center, maxdistance=radius).items()
        neighbors = np.array([_[0] for _ in pairs])
        d = np.array([_[1] for _ in pairs])

        mask = np.in1d(neighbors, indices)
        neighbors = neighbors[mask]
        d = d[mask]

        sls.append(neighbors)
        dists.append(d)

    np.savez(out_fn, sls=sls, dists=dists)
    print(out_fn, len(sls))


if __name__ == '__main__':
    for lr in 'lr':
        compute_searchlights(lr)
