import re, sys, os, copy, json5
import numpy as np
import scipy.io as spio

class duct(dict):
    """ duct is an object derived from dict object which allows accessing its items as class attributes. It is able to import from or export to .json files by using json5 library.
    """

    def __init__(self, other=None):
        super().__init__()
        if type(other) == str:
            ext = os.path.splitext(other)[1]
            if ext == ".json":
                self.load_json(other)
            else:
                pass
        else:
            return self.update(other)

    def __setattr__(self, key, value):
        return self.__setitem__(key, value)

    def __getattr__(self, key):
        return super().__getitem__(key)

    def __delattr__(self, key):
        return super().__delitem__(key)

    def __setitem__(self, key, value):
        warn_msg = None
        if re.search("^[a-zA-Z_$][a-zA-Z_$0-9]*$", key) is None:
            warn_msg = "invalid variable name"
        if key in self.__dir__():
            warn_msg = "a class method with the same name exists"
        if warn_msg is not None:
            sys.stderr.write(
                """Warning: '%s' cannot be used as a class attribute (%s)."""
                """ However, it can be accessed by index.\n"""
                % (key, warn_msg)
            )
        return super().__setitem__(key, value)

    def copy(self):
        other = duct()
        for key, value in self.items():
            other[key] = copy.deepcopy(value)
        return other

    def __copy__(self, memo=None):
        return self.copy()
    
    def __deepcopy__(self, memo=None):
        return self.copy()
    
    def update(self, other=None):
        if other is not None:
            _other = duct()
            for key, value in other.items():
                _other[key] = copy.deepcopy(value)
            return super().update(_other)

    def load_json(self, fn, clear=True):
        """ Loads data from .json file

        Parameters:

        fn: str
            path of .json file
        clear: bool
            determines whether the data in duct will be cleared before loading .json file

        """
        if clear:
            self.clear()
        with open(fn, "r") as f:
            source_dict = json5.load(f)
            for key, value in source_dict.items():
                setattr(self, key, value)

    def save_json(self, fn, indent=4):
        """ Saves data to .json file

        Parameters:

        fn: str
            path of .json file
        indent: int, optional
            indentation in .json file (default value: 4).
        """
        with open(fn, "w") as f:
            json5.dump(self, f, indent=indent)

class numduct(duct):
    """ numduct is an extension of duct objects for numerical codes. It allows working with .mat files 
    """
    def __init__(self, other=None):
        super().__init__()
        if type(other) == str:
            ext = os.path.splitext(other)[1]
            if ext == ".json":
                self.load_json(other)
            elif ext == ".mat":
                self.loadmat(other)
            elif ext == '.npz':
                self.loadz(other)
            else:
                pass
        else:
            return self.update(other)

    def __squeeze_all_axes(self, x: np.ndarray):
        return np.squeeze(x, tuple(np.where(np.array(x.shape, dtype=int) == 1)[0]))

    def save_json(self, fn, indent=None, squeeze_all=False):
        with open(fn, "w") as f:
            other = self.copy()
            for key, value in other.items():
                if type(other[key]) == np.ndarray:
                    if squeeze_all:
                        other[key] = self.__squeeze_all_axes(value).tolist()
                    else:
                        other[key] = value.tolist()
            json5.dump(other, f, indent=indent)

    def savemat(self, fn, *args):
        """ Saves data to .mat file by converting lists into numpy arrays. Additional arguments are passed to scipy.io.savemat routine."""
        other = self.copy()
        for key, value in other.items():
            if type(other[key]) == list:
                other[key] = np.array(value, dtype=object)
        spio.savemat(fn, other, *args)

    def loadmat(self, fn, squeeze_floats=True, squeeze_all=False):
        """ Loads data from .mat file.
            
            Parameters:

            squeeze_floats: bool, optional
                reshape two dimensional arrays with size==1 as floats (default value: True)
            
            squeeze_all: bool, optional
                squeeze all variables in .mat file (default value: False)
                
        """
        other = numduct(spio.loadmat(fn, squeeze_me=squeeze_all))
        if (not squeeze_all) and squeeze_floats:
            for key, value in other.items():
                if (type(value) == np.ndarray) and (value.size == 1):
                    other[key] = value[0, 0]

        self.update(other)

    def savez(self, fn, compress=True):
        """ Saves data to .npz file.
            
            Parameters:

            compress: bool, optional
                determines whether .npz file is compressed (default value: True).
        """
        if compress:
            np.savez_compressed(fn, **self)
        else:
            np.savez(fn, **self)
    
    def loadz(self, fn):
        """ Loads data from .npz file."""
        with np.load(fn) as data:
            self.update({file: data[file] for file in data.files})