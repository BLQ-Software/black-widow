import parser
import graph

class BlackWidow(object):
    """Runs simulation based on settings.

    Generalizes Python's print to adapt to custom settings,
    and direct different types of messages to different outputs
    including files, or functions that dynamically generate graphs.
    
    Attributes
    ----------
    real_time : bool 
        whether to graph in real time or write to files. 
    show_verbose : bool
        whether to print statements labeled verbose.
    data_file : str  
        name of file to write to.

    Methods
    -------
    __init__(settings)
        Construct printer based on settings dictionary.
    
    Example
    -------
    >>> from blackwidow import BlackWidow
    >>> settings = {'filename': 'case0.json' ... }
    >>> bw = BlackWidow(settings)
    >>> bw.run()
    """
    def __init__(self, settings):
        """Configures printer based on settings dictionary.

        The settings dictionary contains exactly all non-default
        settings.

        Parameters
        ----------
        settings : dict 
        """
        self.real_time = False # Default setting
        if 'real_time' in settings:
            self.real_time = settings['real_time'] # Override default

        self.show_verbose = False 
        if 'show_verbose' in settings:
            self.real_time = settings['show_verbose']

        self.file_name = None
        if 'file_name' in settings: 
            self.file_name = settings['file_name']

        self.log_file = None
        if 'log_file' in settings:
            self.log_file = settings['log_file']
  


    def run(self, file_name):
        """Runs the overall simulation based on settings specified when
        the BlackWidow object is constructed.

        :param filename: name of config file
        :type filename: string

        """

        print "Parsing {0} ...".format(file_name), "\n"
        network = parser.config_network(file_name)

        print "Parsed network: \n"
        network.dump()

        print "\nRunning network: \n"
        network.run()

        #TODO: integrate graph (will graph if we
        # produced log files).
        #if self.log_file is not None:
        #     graph.display(self.log_file)



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

        Standard data types:
            link.drop
            link.rate
        """
        if self.real_time:
            graph.plot(data, data_type) # TODO: integrate with graph module. 
        elif self.log_file is not None:
            # Write data to file with extension based on data type.
            with open('{0}.{1}'.format(self.log_file, data_type), 'a') as f:
                f.write(data)
