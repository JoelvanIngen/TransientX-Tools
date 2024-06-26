import sys
import os
import argparse

import filetools

import logging
logger = logging.getLogger(__name__)


DM_IDX: int = 3
ID_IDX: int = 1
PNGFILE_IDX: int = 8
SNR_IDX: int = 5


class TXCandidate:
    def __init__(self, candidate_str: str):
        self.candidate_str: str = candidate_str
        self.candidate: list[str] = candidate_str.split('\t')

        logger.debug("Instantiated candidate with string " + self.candidate_str)

    @property
    def dm(self):
        return self.candidate[DM_IDX]

    @property
    def id(self):
        return self.candidate[ID_IDX]

    @property
    def png_file(self):
        return self.candidate[PNGFILE_IDX]

    @property
    def snr(self):
        return self.candidate[SNR_IDX]


def ask_overwrite_confirmation():
    if (args.overwrite or args.clean) and not args.force:
        print("Warning: you are about to overwrite candidate files or remove PNG files. This cannot be undone.")
        print("Make sure you have a copy or backup of the original files somewhere.")
        print("Are you sure you want to perform this action (y/N)?")
        print("Hint: you can disable this warning by using the -f or --force argument.")

        while True:
            i = input("").lower().strip()
            if i == "y":
                return
            elif i == "n":
                sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=False, help="Input file")
    parser.add_argument("-n", "--number", type=int, required=True, help="Number of candidates to keep")
    parser.add_argument("--dmc", type=int, required=False, help="DM cutoff under which value to drop candidates")
    parser.add_argument("-o", "--output", type=str, required=False, help="Output file")
    parser.add_argument("-c", "--clean", required=False, action='store_true', help="Remove PNGs from rejected candidates")
    parser.add_argument("-w", "--overwrite", required=False, action='store_true', help="Overwrite input file")
    parser.add_argument("-d", "--debug", required=False, action='store_true', help="Print debug logging output")
    parser.add_argument("-f", "--force", required=False, action='store_true', help="Ignore and auto-accept warnings")
    return parser.parse_args()


def remove_cand(cand: TXCandidate) -> None:
    if args.clean:
        if os.path.isfile(cand.png_file):
            logger.debug(f"Removing PNG with filename {cand.png_file}")
            os.remove(cand.png_file)
        else:
            logger.warning("Candidate PNG " + cand.png_file + " does not exist, skipping PNG deletion")


def filter_cand(cand: TXCandidate) -> bool:
    """
    Returns True if candidate passed all filters, and false if not and should be dropped
    """

    if args.dmc and float(cand.dm) < args.dmc:
        logger.debug(f"Dropped candidate {cand.id} because DM is under cutoff: {cand.dm} / {args.dmc}")
        return False

    return True


def convert_file(in_file: str, out_file: str):
    """
    Converts a single file in_file to out_file. Assumes files exist
    """
    with open(in_file, 'r') as f:
        cands = [TXCandidate(line.strip()) for line in f]

    n_cands_initial = len(cands)

    # Apply filters
    cands_filtered = []
    for cand in cands:
        if filter_cand(cand):
            cands_filtered.append(cand)
        else:
            remove_cand(cand)

    cands = cands_filtered

    cands.sort(key=lambda x: x.snr, reverse=True)

    if len(cands) > args.number:
        logger.debug(f"Removing {len(cands[args.number:])} candidates that did not have high enough SNR")
        [remove_cand(cand) for cand in cands[args.number:]]

    cands = cands[0:args.number]

    n_cands_final = len(cands)

    with open(out_file, 'w') as f:
        for c in cands:
            f.write(c.candidate_str + '\n')

    logger.info(f"Processed file {in_file}; kept {n_cands_final} (max {args.number}) out of {n_cands_initial}")


def main():
    if args.input:
        if not os.path.isfile(args.input):
            raise FileNotFoundError

        in_files = [args.input]

    else:
        in_files = [file for file in os.listdir() if file.endswith(".cands")]

    # Prevent future exceptions by disallowing multiple input files if specific output file name
    if args.output and len(in_files) > 1:
        logger.error("Can only use single input file if output filename is specified")
        sys.exit(1)

    out_files = []
    for in_file in in_files:
        if args.output:
            out_files.append(args.output)
        elif args.overwrite:
            out_files.append(in_file)
        else:
            out_files.append(filetools.add_to_filename(in_file, "trunc"))

    for in_file, out_file in zip(in_files, out_files):
        convert_file(in_file, out_file)


if __name__ == '__main__':
    args = parse_args()

    if args.debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    ask_overwrite_confirmation()

    main()
