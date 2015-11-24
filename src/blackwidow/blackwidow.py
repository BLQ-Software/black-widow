import parser
from graph import Grapher
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
    def __init__(self, settings={}):
        """Initializes settings fields.
        
        settings is a dictionary generated from the argsparse arguments,
        with some extra options added in.
        """
        self._settings = settings
        
        self.real_time = False # Default setting
        if 'real_time' in settings:
            self.real_time = settings['real_time'] # Override default


        self.show_verbose = False
        if 'show_verbose' in settings:
            self.show_verbose = settings['show_verbose']
        

        self.static_routing = False
        if 'static_routing' in settings:
            self.static_routing = settings['static_routing']


        self.data_dir = './data'
        if 'data_dir' in settings:
            self.data_dir = settings['data_dir']


        self.routing_packet_size = 32 * 8
        if ('routing_packet_size' in settings and 
                settings['routing_packet_size'] is not None):
            self.routing_packet_size = settings['routing_packet_size']


        self.log_file = None
        if 'log_file' in settings:
            # Regex to match old version of particular case.
            regex = re.compile(r'{}\..*'.format(settings['log_file']))
            
            for f in os.listdir(self.data_dir):
                if regex.match(f) is not None:
                    os.remove('{}/{}'.format(self.data_dir, f))

            self.log_file = settings['log_file'] 


        


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
        sim_time = network.run()

        grapher = Grapher(self)
        grapher.graph(int(sim_time))



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
            with open('{}/{}.{}.csv'.format(self.data_dir, self.log_file, 
                                            data_type), 'a') as f:
                f.write(data + '\n')
        elif self.show_verbose:
            print data
