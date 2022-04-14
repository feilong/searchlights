[![PyPI](https://img.shields.io/pypi/v/searchlights)](https://pypi.org/project/searchlights/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/searchlights)](https://pypistats.org/packages/searchlights)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/searchlights)

`searchlights` is a Python package that provides precomputed searchlights for surface-based analysis of fMRI data.
It only depends on `NumPy`.

## Installation
The package can be installed with pip:
```bash
python -m pip install searchlights
```

## Example usage

The surface-based fMRI data we usually use (e.g., [Feilong et al., 2018](https://doi.org/10.1016/j.neuroimage.2018.08.029)) are in `fsaverage` space, downsampled to a lower resolution (`icoorder5`, approximately 3 mm vertex spacing).
The surface has 9372 vertices for the left hemisphere, and 9370 vertices for the right hemisphere.
The code below shows how to get the searchlights for the left hemisphere with a 20 mm radius.

```python
import numpy as np
from searchlights import get_searchlights
sls = get_searchlights('l', 20, 'fsaverage')
```

See the [documentation](https://feilong.github.io/searchlights/#example) for more examples and details.
