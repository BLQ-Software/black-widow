"""Runs blackwidow simulator on a specified set of files.

This script parses user arguments and configures the blackwidow
module to run based on user arguments.
"""
import argparse
from blackwidow import BlackWidow 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a network simulation.')
    parser.add_argument('files', metavar='config_file', type=str, nargs='+',
                        help='a file to process')
    args = parser.parse_args()

    
    settings = {}

    bw = BlackWidow(settings)
    # Iterate through config files specified.
    for f in args.files:
        bw.run(f)
