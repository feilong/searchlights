import os
import numpy as np
import nibabel as nib


def compute_cortical_mask(lr, surf_tmpl, fs_dir):
    """
    Compute and save the cortical mask based on FreeSurfer's data.
    """
    counts = {
        'fsaverage': {'l': 9372, 'r': 9370},
        'fsaverage6': {'l': 9372, 'r': 9369},
        'fsaverage5': {'l': 9354, 'r': 9361},
    }

    if surf_tmpl == 'fsaverage':
        fn = '{fs_dir}/{surf_tmpl}/label/{lr}h.aparc.annot'.format(fs_dir=fs_dir, surf_tmpl=surf_tmpl, lr=lr)
        labels, ctab, names = nib.freesurfer.io.read_annot(fn)
        mask = (labels != -1)
    elif surf_tmpl in ['fsaverage6', 'fsaverage5']:
        fn = '{fs_dir}/{surf_tmpl}/label/{lr}h.cortex.label'.format(fs_dir=fs_dir, surf_tmpl=surf_tmpl, lr=lr)
        labels = nib.freesurfer.io.read_label(fn)
        nv = {'fsaverage6': 40962, 'fsaverage5': 10242}[surf_tmpl]
        mask = np.zeros((nv, ), dtype=bool)
        mask[labels] = True
    else:
        raise ValueError

    assert np.sum(mask[:10242]) == counts[surf_tmpl][lr]

    out_fn = f'../src/searchlights/data/mask_{surf_tmpl}_{lr}h.npy'
    os.makedirs(os.path.dirname(out_fn), exist_ok=True)
    np.save(out_fn, mask)


if __name__ == '__main__':
    fs_dir = os.path.expanduser('~/lab/freesurfer/subjects')

    for surf_tmpl in ['fsaverage', 'fsaverage6', 'fsaverage5']:
        for lr in 'lr':
            compute_cortical_mask(lr, surf_tmpl, fs_dir)
