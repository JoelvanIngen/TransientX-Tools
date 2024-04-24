import os
from astropy.io import fits
import numpy as np


def _ensure_file_exist(f: str):
    """
    Raises exception if specified file does not exist, does nothing otherwise.
    :param f: filename to verify
    """
    if not os.path.isfile(f):
        raise FileNotFoundError(f"File {f} does not exist.")


class TransientXFitsReader:
    def __init__(self, filename: str):
        _ensure_file_exist(filename)

        with fits.open(filename) as hdul:
            # Brightness data
            d = hdul[5].data[0]
            self.timestamps = d[0]
            self.frequencies = d[1]
            self.brightness_datapoints = np.reshape(d[2], (d[1].size, d[0].size))

            # Dispersion data
            d = hdul[9].data[0]
            self.dms = d[1]
            self.dispersion_datapoints = np.reshape(d[2], (d[1].size, d[0].size))
