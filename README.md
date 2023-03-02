# ductionary
A dictionary-derived object class to store items as attributes

## Description
This library provides a dictionary structure with the functionality of accessing items by using class attributes. There are two classes in the library called `duct` and `numduct`:

* `duct` object is for general use and it supports data input/output by using `.json` files via `save_json()` and `load_json()` functions.
* `numduct` object is for numerical codes and it supports `.mat` (via `savemat()` and `loadmat()` functionas) and `.npz` formats (via `savez()` and `loadz()` functions).

## Examples

```python
from ductionary import duct
d = duct()
d.a = 3
d.b = 'test'

print(d, d.a, d['a'])

d.save_json('output.json', indent=2)
e = duct()
e.load_json('output.json')
print(e)

```

```python
from ductionary import numduct
import numpy as np

d = numduct()
d.a = np.random.rand(3,4)
d.savemat('matfile.mat')
d.savez('npzfile.npz')

e = numduct()
e.loadmat('matfile.mat')
print(e.a)

```

## Dependencies
```
python = "^3.9.13"
numpy = "^1.21.5"
scipy = "^1.9.1"
json5 = "^0.9.6"
```

## Installation
Clone repository by using the command below:
`git clone https://github.com/cinarn/ductionary.git`

Install the package by using pip
`python -m pip install git+https://github.com/cinarn/ductionary.git`
