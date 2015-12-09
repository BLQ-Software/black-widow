import parser
from graph import CsvGrapher
import re
import os


class BlackWidow(object):
    """Runs simulation based on settings.

    Generalizes Python's print to adapt to custom settings,
    and direct different types of messages to different outputs
    including files, or functions that dynamically generate graphs.

    Parameters
    ----------
    settings : dict
        Contains settings to initialize the printer. Values include:
            real_time : bool
                Whether to graph in real time or write to files.
            show_verbose : bool
                Whether to print statements labelled verbose.
            log_file : str
                Name of file to write to. This is the prefix for all data types
                written to files. See documentation for write for more
                information.

    Methods
    -------
    run(file_name)
        Runs the overall simulation based on settings specified when
        the BlackWidow object is constructed.
    print_verbose(msg)
        Handles a verbose message based on specified settings.
    record(data, data_type)
        Records data based on specified settings.


    Examples
    -------
    >>> from blackwidow import BlackWidow
    >>> settings = {'filename': 'case0.json' ... }
    >>> bw = BlackWidow(settings)
    >>> bw.run()
    """
    def __init__(self, settings={}):
        """Initializes settings fields.

        settings is a dictionary generated from the argsparse arguments,
        with some extra options added in.
        """

        # Set settings

        # Real time graphing
        self.real_time = False  # Default setting
        if 'real_time' in settings:
            self.real_time = settings['real_time']  # Override default

        # Show verbose output
        self.show_verbose = False
        if 'show_verbose' in settings:
            self.show_verbose = settings['show_verbose']

        # Static routing
        self.static_routing = False
        if 'static_routing' in settings:
            self.static_routing = settings['static_routing']

        # Directory to write data to
        self.data_dir = './data'
        if 'data_dir' in settings:
            self.data_dir = settings['data_dir']

        # Size of routing packet
        self.routing_packet_size = 32 * 8 * 0
        if ('routing_packet_size' in settings and
                settings['routing_packet_size'] is not None):
            self.routing_packet_size = settings['routing_packet_size']

        # Log file. Prefix for all data files
        self.log_file = None
        if 'log_file' in settings:
            # Regex to match old version of particular case.
            regex = re.compile(r'{}\..*'.format(settings['log_file']))

            for f in os.listdir(self.data_dir):
                if regex.match(f) is not None:
                    os.remove('{}/{}'.format(self.data_dir, f))

            self.log_file = settings['log_file']

        # TCP algorithm
        self.tcp_alg = 'Reno'
        if ('tcp_alg' in settings and settings['tcp_alg'] is not None):
            self.tcp_alg = settings['tcp_alg']

        # Initialize the data to be empty. This dictionary will contain all
        # recorded data.
        self.data = {}

    def run(self, file_name):
        """Runs the overall simulation based on settings specified when the
        BlackWidow object is constructed.

        Parameters
        ----------
        file_name : string
            Name of config file containing network.

        Returns
        -------
        sim_time : float
            The amount of time taken for the network to finish running.
        """

        print "Parsing {0} ...".format(file_name), "\n"
        # Create network from file
        self.network = parser.config_network(file_name, self)
        # Initialize grapher
        self.grapher = CsvGrapher(self)

        print "Parsed network: \n"
        self.network.dump()

        # Run the network.
        print "\nRunning network: \n"
        # sim_time is the amount of time taken for the network to run
        sim_time = self.network.run()

        # Graph the data if we are not graphing in real time
        if not self.real_time:
            self.grapher.graph(int(sim_time))

        return sim_time

    def run_network(self, network):
        """Runs the overall simulation based on settings specified when the
        BlackWidow object is constructed.

        Parameters
        ----------
        network : `Network`
            The network to run.

        Returns
        -------
        sim_time : float
            The amount of time taken for the network to finish running.
        """

        self.network = network
        self.grapher = CsvGrapher(self)
        sim_time = network.run()
        if not self.real_time:
            self.grapher.graph(int(sim_time))
        return sim_time

    def print_verbose(self, msg):
        """Handles a verbose message based on specified settings.

        Parameters
        ----------
        msg : str
            Message to show.
        """
        if self.show_verbose:
            print msg

    def record(self, data, data_type):
        """Records data based on specified settings.

        Parameters
        ----------
        data : str
            Data point to record/plot.
        data_type : str
            Type of data, will be used as a file extension.

        Notes
        -----
        Standard data types:
            link.drop    -  "Time in ms", "Number of drops"
            link.sent    -  "Time in ms", "Number of packets sent"
            flow.window  -  "Time in ms", "Window size"
            flow.sent    -  "Time in ms", "Mega bits"
            flow.delay   -  "Time in ms", "Delay in ms"
        """
        if self.real_time:
            data_num = [float(x) for x in data.split(", ")]
            pass

        # Add to existing data type
        if data_type in self.data:
            self.data[data_type].append(data)

        # Create new data type and add the data
        else:
            self.data[data_type] = [data]
        if self.show_verbose:
            print data

    def write(self):
        """ Writes data to files.

        This function writes each type of data to a file. The files are
        dependent on the extensions used to save data and the log_file file.
        Files are created as:
            [log_file].[data_type].csv
        Files are created in the data_dir directory in CSV format.

        """

        # Check if the log file is defined. If not, we cannot write data.
        if self.log_file is not None:
            # Write each data type to a file
            for data_type in self.data:
                # Open file
                with open('{}/{}.{}.csv'.format(self.data_dir, self.log_file,
                                                data_type), 'a') as f:
                    # Write data
                    for data in self.data[data_type]:
                        f.write(data + '\n')
