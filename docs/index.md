---
jupytext:
  cell_metadata_filter: -all
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Welcome to searchlights

Searchlight analysis {cite:p}`10.1073/pnas.0600244103,10.1016/j.neuroimage.2010.04.270,10.1016/j.neuroimage.2010.07.035` is one of the most popular methods in neuroimaging data analysis.
It has been widely used in multivariate pattern analysis (MVPA) {cite:p}`10.1146/annurev-neuro-062012-170325`, including searchlight-based hyperalignment algorithms {cite:p}`10.1093/cercor/bhw068,10.1371/journal.pcbi.1006120,10.1016/j.neuroimage.2018.08.029`.
Essentially, searchlight analysis loops through all brain regions (usually defined as spheres in volume and disks on surface) like a searchlight.
It is often used to find brain regions containing certain information (e.g., regions with highest decoding accuracy).

`searchlights` is a lightweight Python package that provides precomputed searchlights for surface-based analysis of fMRI data.
It supports multiple standard surfaces provided by FreeSurfer (e.g., `fsaverage`, `fsaverage5`) and different spatial resolutions (e.g., `icoorder5`, `icoorder3`).
It only depends on [`NumPy`](https://numpy.org/).

## Installation

`searchlights` can be easily installed with pip
```bash
python -m pip install searchlights
```

## Example

The surface-based fMRI data we usually use (e.g., {cite:t}`10.1016/j.neuroimage.2018.08.029`) are in `fsaverage` space, downsampled to a lower resolution (`icoorder5`, approximately 3 mm vertex spacing).
The surface has 9372 vertices for the left hemisphere, and 9370 vertices for the right hemisphere.
The code below shows how to get the searchlights for the right hemisphere with a 20 mm radius.

```{code-cell}python
import numpy as np
from searchlights import get_searchlights
sls = get_searchlights('l', 20, 'fsaverage')
```

---

There are 9372 searchlights, one for each vertex as the center.
```{code-cell}python
print(len(sls))
```

---

Each entry in `sls` is a NumPy array comprising the indices of vertices in the searchlight.
In this case the indices ranging from 0 to 9371 (0-based indexing).
```{code-cell}python
cat = np.concatenate(sls)
print(cat.min(), cat.max())
```

---

If you have a data matrix `ds` that is in the same space and has the same resolution as the searchlights, you can easily get the data in a searchlight using
```python
sl = sls[0]  # the first searchlight
sub_ds = ds[:, sl]  # data in the first searchlight
```

---

````{admonition} References
<!-- :class: full-width -->

```{bibliography}
:filter: docname in docnames
:style: unsrt
```
````