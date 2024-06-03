import os
from sigpyproc.readers import FilReader
from candidate import Candidate


def ensure_file_exists(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(path)


def get_tstart_from_fil(fil_filename: str) -> float:
    return float(FilReader(fil_filename).header.tstart)


def parse_transientx_line(text: str, fil_tstart: float) -> Candidate:
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
    data = text.split('\t')

    return Candidate(
        fil_filename=data[10],
        snr=data[5],
        tcand_mjd=data[2],
        dm=data[3],
        width=data[4],
        fil_tstart=fil_tstart
    )


def parse_transientx_file(args) -> list[Candidate]:
    fil_tstart = get_tstart_from_fil(args.filterbank)

    with open(args.input, 'r') as f:
        return [parse_transientx_line(line.strip(), fil_tstart) for line in f.readlines()]


def write_heimdall_file(heimdall_filename: str, data: list[Candidate]) -> None:
    with open(heimdall_filename, 'w') as f:
        f.write("file,snr,stime,width,dm,label,chan_mask_path,num_files\n")

        for candidate in data:
            f.write(candidate.to_csv())


def convert(args) -> None:
    # Ensure files exist
    ensure_file_exists(args.input)
    ensure_file_exists(args.filterbank)

    # Read data from TransientX's .cands file
    data = parse_transientx_file(args)

    # Write data in Heimdall format
    write_heimdall_file(args.output, data)
