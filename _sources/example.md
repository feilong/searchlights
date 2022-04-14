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

# Visualizing searchlights

This example shows how to get the searchlights using `get_searchlights` and visualize them on cortical surface using [`brainplotlib`](https://feilong.github.io/brainplotlib/)'s `brain_plot`.
These visualized searchlights are the face regions used in our recent preprint ({cite:t}`10.1101/2021.11.17.469009`).
In this example, each faces region is defined as a searchlight with a 10 mm radius.
We render vertices in face regions in one color and other cortical vertices in another color.

Note that searchlights are defined as disks on a cortical surface (the "midthickness" surface in this case).
When searchlights are visualized on an inflated surface, such as in the example below, the shape may look somewhat different due to inflation.

![](face_ROIs.png)

```{code-cell}python
import numpy as np
from searchlights import get_searchlights
from brainplotlib import brain_plot

lh_indices = np.array([3026, 9254, 9243, 1267, 2900, 3007, 3660, 7945, 4585, 3523])
rh_indices = np.array([7832,  142, 2519, 9123, 8793, 9336, 1467, 1478, 7001, 5321])
areas = ['OFA', 'aFFA', 'pFFA', 'ATL', 'pSTS', 'aSTS', 'sIFG', 'mIFG', 'iIFG', 'precuneus']

```
```{margin}
This part set the value of any vertices in a face area to 1, and others to 0.
```
```{code-cell}python
values = []
for lr, center_indices in zip('lr', [lh_indices, rh_indices]):
    nv = {'l': 9372, 'r': 9370}[lr]
    v = np.zeros((nv, ))
    sls = get_searchlights(lr, 10, 'fsaverage')
    for center in center_indices:
        sl = sls[center]
        v[sl] = 1
    values.append(v)
```
```{code-cell}python
img = brain_plot(values, vmax=1, vmin=-1, cmap='coolwarm')

from PIL import Image
im = Image.fromarray(
    np.round(img * 255).astype(np.uint8))
im.save('face_ROIs.png')
```

## References
```{bibliography}
:filter: docname in docnames
:style: unsrt
```
