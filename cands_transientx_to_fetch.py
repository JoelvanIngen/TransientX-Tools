"""
TransientX: Using data from https://github.com/ypmen/TransientX/blob/master/src/singlepulse/candplot.cpp, starting on line 415
Fetch: Using data from readme.md or cand2h5 function in https://github.com/devanshkv/fetch/blob/master/bin/candmaker.py
"""
import os
import argparse
from dataclasses import dataclass
from sigpyproc.readers import FilReader


@dataclass
class CandidateData:
    fil_filename: str
    snr: str
    tcand: str
    dm: str
    width: str


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='TransientX .cands file to convert', required=True)
    parser.add_argument('-o', '--output', type=str, help='fetch .cands file to write', required=True)
    parser.add_argument('-f', '--filterbank', type=str, help='filterbank file to read', required=True)

    return parser.parse_args()


def ensure_file_exists(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)


def get_tstart_from_fil(fil_filename: str) -> float:
    fil = FilReader(fil_filename)
    return float(fil.header.tstart)


def parse_transientx_line(text: str, fil_tstart: float) -> CandidateData:
    """
    TransientX cands file:
    TAB separated
        's_ibeam': data_list[0],
        'candidate_number': data_list[1],
        'timestamp': data_list[2],
        'dm': data_list[3],
        'width': data_list[4],
        'snr': data_list[5],
        'freq stop': data_list[6],
        'freq start': data_list[7],
        'png filename': data_list[8],
        's_id': data_list[9],
        'fil filename': data_list[10]
    """
    data_list = text.split('\t')

    cand_mjd = float(data_list[2])
    time_elapsed_mjd = cand_mjd - fil_tstart
    time_elapsed_sec = time_elapsed_mjd * 86400

    return CandidateData(
        fil_filename=data_list[10],
        snr=data_list[5],
        tcand=str(time_elapsed_sec),
        dm=data_list[3],
        width=data_list[4]
    )


def parse_transientx_file(transientx_filename: str, fil_tstart: float) -> list[CandidateData]:
    with open(transientx_filename, 'r') as f:
        return [parse_transientx_line(line.strip(), fil_tstart) for line in f.readlines()]


def write_fetch_file(fetch_filename: str, data: list[CandidateData]) -> None:
    with open(fetch_filename, 'w') as f:
        for candidate in data:
            fetch_data = [
                candidate.fil_filename,
                candidate.snr,
                candidate.tcand,
                candidate.dm,
                candidate.width,
            ]

            f.write(','.join(fetch_data) + '\n')


def main():
    cmd_args = parse_arguments()
    ensure_file_exists(cmd_args.input)
    ensure_file_exists(cmd_args.filterbank)

    fil_tstart = get_tstart_from_fil(cmd_args.filterbank)

    data = parse_transientx_file(cmd_args.input, fil_tstart)
    write_fetch_file(cmd_args.output, data)


if __name__ == '__main__':
    main()
