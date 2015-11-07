import parser
import graph
from datetime import datetime

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
                Name of file to write to.

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
    def __init__(self, settings):
        self.real_time = False # Default setting
        if 'real_time' in settings:
            self.real_time = settings['real_time'] # Override default

        self.show_verbose = False
        if 'show_verbose' in settings:
            self.real_time = settings['show_verbose']

        self.log_file = None
        if 'log_file' in settings:
            self.log_file = settings['log_file'] + "_" + datetime.now().strftime("%m-%d-%Y_%H:%M")



    def run(self, file_name):
        """Runs the overall simulation based on settings specified when
        the BlackWidow object is constructed.

        Parameters
        ----------
        file_name : string
            Name of config file
        """

        print "Parsing {0} ...".format(file_name), "\n"
        network = parser.config_network(file_name, self)

        print "Parsed network: \n"
        network.dump()

        print "\nRunning network: \n"
        network.run()

        #TODO: integrate graph (will graph if we produced log files).
        #if self.log_file is not None:
        #     graph.plot(self.log_file)



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
            graph.plot(data, data_type) # TODO: integrate with graph module.
        elif self.log_file is not None:
            # Write data to file with extension based on data type.
            # appends to the end of the file.
            with open('{0}.{1}.csv'.format(self.log_file, data_type), 'a') as f:
                f.write(data + '\n')
        elif self.show_verbose:
            print data
