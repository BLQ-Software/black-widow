"""Runs blackwidow simulator on a specified set of files.

This script parses user arguments and configures the blackwidow
module to run based on user arguments.
"""
import argparse
import os.path
from blackwidow import BlackWidow
from run_interactive import create_bw

def main():
    """Runs the simulator."""

    # Configure argument parser
    parser = argparse.ArgumentParser(description='Run a TCP network'
                                                 'simulation')

    # Files containing network configurations. Multiple files can be provided.
    parser.add_argument('files', metavar='config_file', type=str, nargs='*',
                        help='name of file to process. e.g. case0.json')
    # Flag to show verbose output
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='whether to print verbose statements')
    # Flag to graph in real time
    parser.add_argument('-r', '--real-time', action='store_true',
                        help='whether to graph in real time')
    # Flag to use static routing instead of dynamic routing
    parser.add_argument('-s', '--static-routing', action='store_true',
                        help='uses static routing instead of dynamic routing.')
    # Flag to set the routing packet size
    parser.add_argument('-rp', '--routing-packet-size', type=int,
                        help='Sets the size of the routing packet')
    # Flag to set the TCP algorithm. Valid arguments are: Reno, Tahoe, Fast
    parser.add_argument('-t', '--tcp-alg', type=str,
                        help='Sets the TCP algorithm for the simulation.')
    # Flag to use non-interactive mode
    parser.add_argument('-n', '--no-interactive', action='store_true',
                        help='Sets interactive mode off')

    # Dictionary of alternative settings.
    # Default settings should be set in the BlackWidow class.
    settings = vars(parser.parse_args())

    # Iterate through config files specified.

    if len(settings['files']) != 0:
        for f in settings['files']:
            # Make default log_file name the input name without ext.
            # Set the log file if not running in real time since data will be
            # written to file.
            if not settings['real_time']:
                base = os.path.basename(f)
                settings['log_file'] = os.path.splitext(base)[0]

            # Run non-interactive mode if no_interactive flag is set.
            if settings["no_interactive"]:
                bw = BlackWidow(settings)
                bw.run(f)
            # Otherwise, run interactive mode and load file
            else:
                create_bw(settings, f)
    # Run interactive mode without loading any files
    else:
        create_bw()

if __name__ == "__main__":
    main()
