"""
TransientX: Using data from https://github.com/ypmen/TransientX/blob/master/src/singlepulse/candplot.cpp, starting on line 415
Fetch: Using data from readme.md or cand2h5 function in https://github.com/devanshkv/fetch/blob/master/bin/candmaker.py
"""
import os
import sys


def parse_arguments():
    if not len(sys.argv) == 3:
        print('Usage: python3 [TransientX cands file] [Filename to output Fetch cands file]')
        sys.exit(1)

    return sys.argv[1:]


def ensure_file_exists(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)


def parse_transientx_line(text: str):
    """
    TransientX cands file:
    TAB separated
    - s_ibeam
    - candidate number
    - timestamp (mjd)
    - dm
    - width
    - snr
    - freq stop
    - freq start
    - png filename
    - s_id
    - fil filename
    """
    data_list = text.split('\t')

    return {
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
    }


def parse_transientx_file(transientx_filename: str):
    with open(transientx_filename, 'r') as f:
        return [parse_transientx_line(line.strip()) for line in f.readlines()]


def write_fetch_file(fetch_filename: str, data: list[dict[str: str]]):
    with open(fetch_filename, 'w') as f:
        for line in data:
            fetch_data = [
                line['fil filename'],
                line['snr'],
                line['start time'],  # NON-EXISTENT
                line['dm'],
                line['width'],
                line['label'],  # NON-EXISTENT
                line['kill mask path']  # NON-EXISTENT
            ]

            f.write(','.join(fetch_data) + '\n')


def main():
    transientx_filename, fetch_filename = parse_arguments()
    ensure_file_exists(transientx_filename)

    data = parse_transientx_file(transientx_filename)
    write_fetch_file(fetch_filename, data)


if __name__ == '__main__':
    main()
