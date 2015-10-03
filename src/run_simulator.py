"""Runs blackwidow simulator on a specified set of files.

This script parses user arguments and configures the blackwidow
module to run based on user arguments.
"""
import argparse
import blackwidow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a network simulation.')
    parser.add_argument('files', metavar='config_file', type=str, nargs='+',
                        help='a file to process')
    args = parser.parse_args()

    # Iterate through config files specified.
    for f in args.files:
        blackwidow.run(f)
