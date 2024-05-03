"""
TransientX: Using data from https://github.com/ypmen/TransientX/blob/master/src/singlepulse/candplot.cpp, starting on line 415
Fetch: Using data from readme.md or cand2h5 function in https://github.com/devanshkv/fetch/blob/master/bin/candmaker.py
"""
import os
import argparse
from dataclasses import dataclass


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


def parse_transientx_line(text: str) -> CandidateData:
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

    return CandidateData(
        fil_filename=data_list[10],
        snr=data_list[5],
        tcand="PLACEHOLDER",  # TODO: Implement
        dm=data_list[3],
        width=data_list[4]
    )


def parse_transientx_file(transientx_filename: str) -> list[CandidateData]:
    with open(transientx_filename, 'r') as f:
        return [parse_transientx_line(line.strip()) for line in f.readlines()]


def write_fetch_file(fetch_filename: str, data: list[CandidateData]) -> None:
    with open(fetch_filename, 'w') as f:
        for candidate in data:
            fetch_data = [
                candidate.fil_filename,
                candidate.snr,
                candidate.tcand,  # TODO: Implement
                candidate.dm,
                candidate.width,
            ]

            f.write(','.join(fetch_data) + '\n')


def main():
    cmd_args = parse_arguments()
    ensure_file_exists(cmd_args.input)

    data = parse_transientx_file(cmd_args.input)
    write_fetch_file(cmd_args.output, data)


if __name__ == '__main__':
    main()
