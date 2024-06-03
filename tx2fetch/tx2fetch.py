import argparse
import converter


def parse_arguments():
    parser = argparse.ArgumentParser()

    # Files
    parser.add_argument('-i', '--input', type=str, help='TransientX .cands file to convert', required=True)
    parser.add_argument('-o', '--output', type=str, help='Heimdall candidate file to write',
                        default='heimdall_cands.csv')
    parser.add_argument('-f', '--filterbank', type=str, help='filterbank file to read', required=True)
    pass

    return parser.parse_args()


def main():
    converter.convert(args)


if __name__ == '__main__':
    args = parse_arguments()

    main()
