import parser
import sim
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
    network = parser.config(filename)
    
    # data = sim.simulate(network)

    # graph.display(data)
