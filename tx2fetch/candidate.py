from math import log2


class Candidate:
    def __init__(self,
                 fil_filename: str,
                 snr: str | float,
                 tcand_mjd: str | float,
                 width: str | float,
                 dm: str | float,
                 fil_tstart: float):

        self.fil_filename: str = fil_filename
        self.snr: float = float(snr)
        self.tcand: float = mjd_to_seconds(float(tcand_mjd), fil_tstart)
        self.width: float = float(width)
        self.dm: float = float(dm)

    def to_csv(self):
        return ','.join([
            self.fil_filename,
            str(self.snr),
            str(self.tcand),
            str(log2(self.width)),
            str(self.dm),
        ]) + '\n'


def mjd_to_seconds(cand_mjd: float, fil_tstart: float) -> float:
    time_elapsed_mjd = cand_mjd - fil_tstart
    return time_elapsed_mjd * 86400
