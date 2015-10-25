"""Runs blackwidow simulator on a specified set of files.

This script parses user arguments and configures the blackwidow
module to run based on user arguments.
"""
import argparse
import os.path
from blackwidow import BlackWidow 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a TCP network simulation.')
    parser.add_argument('files', metavar='config_file', type=str, nargs='+',
                        help='name of file to process. e.g. case0.json')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='whether to print verbose statements')
    parser.add_argument('-r', '--real-time', action='store_true',
                        help='whether to graph in real time')
    
    args = vars(parser.parse_args())

    settings = {}

    if 'real_time' in args and args['real_time']:
        settings['real_time'] = True 

    if 'verbose' in args and args['verbose']:
        settings['verbose'] = True

    # Iterate through config files specified.
    for f in args['files']:
        # Make default log_file name the input name without ext. 
        if 'real_time' not in settings:
            base = os.path.basename(f)
            settings['log_file'] = os.path.splitext(base)[0]

        bw = BlackWidow(settings)
        bw.run(f)
