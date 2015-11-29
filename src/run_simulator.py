"""Runs blackwidow simulator on a specified set of files.

This script parses user arguments and configures the blackwidow
module to run based on user arguments.
"""
import argparse
import os.path
from blackwidow import BlackWidow
from run_interactive import create_bw

if __name__ == "__main__":

    # Configure argument parser
    parser = argparse.ArgumentParser(description='Run a TCP network simulation.')
    parser.add_argument('files', metavar='config_file', type=str, nargs='*',
                        help='name of file to process. e.g. case0.json')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='whether to print verbose statements')
    parser.add_argument('-r', '--real-time', action='store_true',
                        help='whether to graph in real time')
    parser.add_argument('-s', '--static-routing', action='store_true',
                        help='uses static routing instead of dynamic routing.')
    parser.add_argument('-rp', '--routing-packet-size', type=int,
                        help='Sets the size of the routing packet')

    parser.add_argument('-t', '--tcp-alg', type=str,
                        help='Sets the TCP algorithm for the simulation.')

    parser.add_argument('-n', '--no-interactive', action='store_true',
                        help='Sets interactive mode off')

    # Dictionary of alternative settings.
    # Default settings should be set in the BlackWidow class.
    settings = vars(parser.parse_args())

    # Iterate through config files specified.

    if len(settings['files']) != 0:
        for f in settings['files']:
            # Make default log_file name the input name without ext.
            if not settings['real_time']:
                base = os.path.basename(f)
                settings['log_file'] = os.path.splitext(base)[0]
            if settings["no_interactive"]:
                bw = BlackWidow(settings)
                bw.run(f)
            else:
                create_bw(settings, f)
    else:
        create_bw()
