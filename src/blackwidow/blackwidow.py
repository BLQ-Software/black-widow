import parser as parser
import graph

def run(filename):
    """Runs the overall simulation, configuring from arguments.

    :param filename: name of config file
    :type filename: string

    :Example:

    >>> import blackwidow
    >>> a = blackwidow.run('config.txt')
    """

    #:
    print
    print "Parsing {0} ...".format(filename), "\n"
    network = parser.config_network(filename)

    print "Parsed network: \n"
    network.dump()

    print "\nRunning network: \n"
    network.run()

    # data = sim.simulate(network)

    # graph.display(data)
