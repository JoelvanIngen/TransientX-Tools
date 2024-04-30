import os
import warnings
import numpy as np
from scipy.optimize import curve_fit
from astropy.io import fits


def _ensure_file_exist(f: str):
    """
    Raises exception if specified file does not exist, does nothing otherwise.
    :param f: filename to verify
    """
    if not os.path.isfile(f):
        raise FileNotFoundError(f"File {f} does not exist.")


def gauss(x, amp, mu, sigma):
    return amp * np.exp(-(x - mu)**2 / (2 * sigma**2))


class PXReader:
    def __init__(self, filename: str):
        _ensure_file_exist(filename)

        with fits.open(filename) as hdul:
            # Load flux graph
            data = hdul[2].data
            self.flux_datapoints = data[0][1]

            d = hdul[3].data
            # First two indices are to locate the data in the nested arrays
            # Last two are to cut the prefix and suffix
            self.snr = float(d[0][4][6:])
            self.width = float(d[1][4][4:][:3])

            # Python hates the double backslash in this string and does not remove suffix correctly, so we split on
            # space instead for this one
            self.dm = float(d[3][4][5:].split(' ')[0])
            self.max_dm = float(d[15][4][23:])
            self.dm_diff_from_max = self.max_dm - self.dm

            self.date_mjd = float(d[12][4][13:])
            self.gl = float(d[13][4][11:])
            self.gb = float(d[14][4][11:])
            self.distance = float(d[16][4][23:])

            self.filename = filename
            self.fil_filename = d[17][4]

            # Brightness data
            d = hdul[5].data[0]
            self.timestamps = d[0]
            self.frequencies = d[1]
            self.brightness_datapoints = np.reshape(d[2], (d[1].size, d[0].size))

            # Dispersion data
            d = hdul[9].data[0]
            self.dms = d[1]
            self.dispersion_datapoints = np.reshape(d[2], (d[1].size, d[0].size))

            self.flux_amp, self.flux_mu, self.flux_sigma = self.fit_flux_gaussian()

    def get_info_str(self):
        return f"Filename: {self.filename}\n" \
               f".fil filename: {self.fil_filename}\n" \
               f"DM (cm^-3pc): {self.dm}\n" \
               f"S/N ratio: {self.snr}\n" \
               f"Width (ms): {self.width}\n" \
               f"GL (deg): {self.gl}\n" \
               f"GB (deg): {self.gb}\n" \
               f"Distance (pc): {self.distance}\n" \
               f"Max. DM (pr/cc): {self.max_dm}"

    def fit_flux_gaussian(self):
        max_index = np.where(self.flux_datapoints == max(self.flux_datapoints))[0][0]

        initial_guess_params = [
            self.flux_datapoints[max_index],
            self.timestamps[max_index],
            0.05 * (max(self.timestamps) - min(self.timestamps))
        ]

        popt, _ = curve_fit(gauss, self.timestamps, self.flux_datapoints, p0=initial_guess_params)

        return popt
