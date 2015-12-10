import os
import cmd
import signal

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from blackwidow import BlackWidow
from blackwidow import parser
from blackwidow.network import *

import spider

import json

from cStringIO import StringIO


class BlackWidowInteractive(cmd.Cmd):
    """Command module to run the simulator in interactive mode.

    This class runs the simulator in interactive mode and supports various
    command.
    """

    def create_network(self, settings=None, f=None):
        """Initializes the network and bw variables.

        Parameters
        ----------
        settings : dict, optional
            A dictionary of settings (the default is None). See `Blackwidow`
            for valid values.
        f : string, optional
            The filename containing the network (the default is None).
        """

        # If settings are not provided, initialize bw and network without any
        # settings.
        if settings is None:
            self.bw = BlackWidow()
            self.network = Network(self.bw)

        # Initialize bw and network with settings
        else:
            self.bw = BlackWidow(settings)
            self.network = parser.config_network(f, self.bw)

        # Reset visual parameters
        self.do_reset_v("")

        # Clear the plot
        self.do_clear("")

        # Create a new figure to show the network
        f = plt.figure(2)
        self.do_show("")

    def do_reset_v(self, line):
        """Resets parameters for interactive

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """

        # Set the dpi and graph projection type
        self.dpi = "300"
        self.proj = "dot"

        # Show the network on every change
        self.show_network = True

        # Hide text output for each change
        self.output = False

    def help_reset_v(self):
        """Prints help message for reset_v command"""
        print "Reset visual parameters"

    def do_reset(self, line):
        """Resets network

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """

        # Initialize bw and network without settings
        self.bw = BlackWidow()
        self.network = Network(self.bw)

        # Clear the figure
        f = plt.figure(2)

        # Reset visual parameters
        self.do_reset_v("")

        # Show the network
        self.do_show("")

    def help_reset(self):
        """Prints help message for reset command"""
        print "Reset the network"

    def do_set_verbose(self, line):
        """Sets verbose output.

        Parameters
        ----------
        line : string
            A string containing command line arguments. See help_set_verbose.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return

        # Set verbose
        if args[0] == "True":
            self.bw.show_verbose = True
        else:
            self.bw.show_verbose = False

    def help_set_verbose(self):
        """Prints help message for set_verbose command"""
        print "set_verbose [verbose]"
        print "Set verbose output. verbose can be True or False"

    def do_set_static_routing(self, line):
        """Sets static routing.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_set_static_routing.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return

        # Set static routing
        if args[0] == "True":
            self.bw.static_routing = True
        else:
            self.bw.static_routing = False

    def help_set_static_routing(self):
        """Prints help message for set_static_routing command"""
        print "set_static_routing [static_routing]"
        print "Set static routing. static_routing can be True or False"

    def do_set_routing_packet_size(self, line):
        """Sets routing packet size.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_set_routing_packet_size.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return

        # Set the routing packet size
        try:
            self.bw.routing_packet_size = float(args[0])
        except Exception as e:
            print e

    def help_set_routing_packet_size(self):
        """Prints help message for set_routing_packet_size command"""
        print "set_routing_packet_size [size]"
        print "Set routing packet size"

    def do_set_tcp_alg(self, line):
        """Sets TCP algorithm.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_set_tcp_alg.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return

        # Set the TCP algorithm
        self.bw.tcp_alg = args[0]

    def help_set_tcp_alg(self):
        """Prints help message for set_tcp_alg command"""
        print "set_tcp_alg [alg]"
        print "Set TP algorithm. Valid options are: Reno, Tahoe, Fast"

    def do_add_router(self, line):
        """Adds multiple routers.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_add_router.
        """

        # Get the args
        args = line.split()

        # Make sure at least 1 argument is provided
        if len(args) < 1:
            return

        # Iterate through each id and add a router
        try:
            for id in args:
                self.network.add_router(id)
            # Show the network after each addition if show_network is True
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_add_router(self):
        """Prints help message for add_router command"""
        print "add_router [id] [id] ... [id]"
        print "Add multiple routers"""

    def do_add_host(self, line):
        """Adds multiple hosts.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_add_host.
        """

        # Get the args
        args = line.split()

        # Make sure at least 1 argument is provided
        if len(args) < 1:
            return

        # Iterate through each id and add a host
        try:
            for id in args:
                self.network.add_host(id)
            # Show the network after each addition if show_network is True
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_add_host(self):
        """Prints help message for add_host command"""
        print "add_host [id] [id] ... [id]"
        print "Add multiple hosts"""

    def do_delete_device(self, line):
        """Deletes multiple devices.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_delete_device.
        """

        # Get the args
        args = line.split()

        # Make sure at least 1 argument is provided
        if len(args) < 1:
            return
        try:
            # If the argument is *, delete all devices
            if len(args) == 1 and args[0] == "*":
                # Iterate through the ids for devices
                for id in self.network.devices.keys()[:]:
                    self.network.delete_device(id)
            else:
                # Delete devices specified
                for id in args:
                    self.network.delete_device(id)
            # Show the network if show_network is True
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_delete_device(self):
        """Prints help message for delete_device command"""
        print "delete_device [id] [id] ... [id]"
        print ("Delete multiple devices. Can also run delete_device * to"
               " delete all devices")

    def do_add_link(self, line):
        """Adds a link.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_add_link.
        """

        # Get the args
        args = line.split()

        # Make sure the correct number of arguments is provided
        if not check_args(args, 6):
            return

        # Add the link
        try:
            self.network.add_link(args[0], args[1], args[2], float(args[3]),
                                  float(args[4]), float(args[5]))
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_add_link(self):
        """Prints help message for add_link command"""
        print "add_link [id] [device_id] [device_id] [delay] [rate] [buffer]"
        print "Add a link"

    def do_delete_link(self, line):
        """Deletes multiple links.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_delete_link.
        """

        # Get the args
        args = line.split()

        # Make sure at least 1 argument is provided
        if len(args) < 1:
            return
        try:
            # If the argument is *, delete all links
            if len(args) == 1 and args[0] == "*":
                # Iterate through link ids
                for id in self.network.links.keys()[:]:
                    self.network.delete_link(id)
            else:
                # Delete links specified
                for id in args:
                    self.network.delete_link(id)
            # Show the network if show_network is True
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_delete_link(self):
        """Prints help message for delete_link command"""
        print "delete_link [id] [id] ... [id]"
        print ("Delete multiple links. Can also run delete_link * to delete"
               " all links")

    def do_add_flow(self, line):
        """Adds a flow.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_add_flow.
        """

        # Get the args
        args = line.split()

        # Make sure the correct number of arguments is provided
        if not check_args(args, 5):
            return

        # Add the flo
        try:
            self.network.add_flow(args[0], args[1], args[2], float(args[3]),
                                  float(args[4]))
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_add_flow(self):
        """Prints help message for add_flow command"""
        print "add_flow [id] [src] [dest] [amount] [start]"
        print "Add a flow"

    def do_delete_flow(self, line):
        """Deletes mulitple flows.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_delete_flow.
        """

        # Get the args
        args = line.split()

        # Make sure at least 1 argument is provided
        if len(args) < 1:
            return
        try:
            # If the argument is *, delete all flows
            if len(args) == 1 and args[0] == "*":
                # Iterate through the flow ids
                for id in self.network.flows.keys()[:]:
                    self.network.delete_flow(id)
            else:
                # Delete flows specified
                for id in args:
                    self.network.delete_flow(id)
            # Show the network if show_network is True
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_delete_flow(self):
        """Prints help message for delete_flow command"""
        print "delete_flow [id] [id] ... [id]"
        print ("Delete multiple flows. Can also run delete_flow * to delete"
               " all flows")

    def do_load(self, line):
        """Loads a file.

        Parameters
        ----------
        line : string
            A string containing command line arguments.
            See help_load.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return
        try:
            # Initialize bw with the log file
            base = os.path.basename(args[0])
            self.bw = BlackWidow({'log_file': os.path.splitext(base)[0]})

            # Initialie network from the file
            self.network = parser.config_network(args[0], self.bw)

            # Create a new figure
            f = plt.figure(2)

            # Show the network if show_network is True
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def help_load(self):
        """Prints help message for load command"""
        print "load [filename"
        print "Load a file"

    def do_show(self, line):
        """Shows the network.

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """
        try:
            # Get the pydot object for the network
            d = self.network.dump(self.output)

            # Set the dpi
            d.set_dpi(self.dpi)

            # Get a PNG string with the specified projection
            png_str = d.create_png(prog=self.proj)

            # Write the string to a StringIO object
            sio = StringIO()
            sio.write(png_str)
            sio.seek(0)

            # Show the image
            image = mpimg.imread(sio)
            plt.axis('off')
            plt.imshow(image)
            plt.show()
        except Exception as e:
            print e

    def help_show(self):
        """Prints help message for show command"""
        print "Show the network"

    def do_run(self, line):
        """Runs the network.

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """
        try:
            # Prompt the user for a log file if not provided and set the log
            # file for the bw object
            if self.bw.log_file is None:
                self.bw.log_file = raw_input("Log file name: ")
            # Run the network
            self.bw.run_network(self.network)
        except Exception as e:
            print e

    def help_run(self):
        """Prints help message for run command"""
        print "Run the network"

    def do_clear(self, line):
        """Clears the graph.

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """
        plt.clf()

    def help_clear(self):
        """Prints help message for clear command"""
        print "Clear the graph"

    def do_close(self, line):
        """Closes the graph.

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """
        plt.close()

    def help_close(self):
        """Prints help message for close command"""
        print "Close the graph"

    def do_set_show(self, line):
        """Sets network graph display behavior.

        Parameters
        ----------
        line : string
            A string containing command line arguments. See help_set_show.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return False

        # Set show_network
        if args[0] == "True":
            self.show_network = True
        else:
            self.show_network = False

    def help_set_show(self):
        """Prints help message for set_show command"""
        print "set_show [show]"
        print "Show the network after every command if show == True"

    def do_set_output(self, line):
        """Sets network graph textual behavior.

        Parameters
        ----------
        line : string
            A string containing command line arguments. See help_set_output.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return False

        # Set output
        if args[0] == "True":
            self.output = True
        else:
            self.output = False

    def help_set_output(self):
        """Prints help message for set_output command"""
        print "set_output [output]"
        print ("Show text output of the network when the show command is"
               " entered if output == True")

    def do_set_dpi(self, line):
        """Sets the dpi to show the network.

        Parameters
        ----------
        line : string
            A string containing command line arguments. See help_set_dpi.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return

        # Set the dpi
        self.dpi = args[0]
        if self.show_network:
            self.do_show("")

    def help_set_dpi(self):
        """Prints help message for set_dpi command"""
        print "set_dpi [dpi]"
        print "Set the dpi"

    def do_set_proj(self, line):
        """Sets the projection to show the network.

        Parameters
        ----------
        line : string
            A string containing command line arguments. See help_set_proj.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return

        # Set proj
        self.proj = args[0]
        if self.show_network:
            self.do_show("")

    def help_set_proj(self):
        """Prints help message for set_proj command"""
        print "set_proj [proj]"
        print ("Set the projection type. See graphviz documentation for valid"
               " projection types")

    def do_exit(self, line):
        """Ends the program.

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """
        print
        return True

    def help_exit(self):
        """Prints help message for exit command"""
        print "End the program"

    def do_stop(self, line):
        """Stops the network.

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """
        self.network.empty()

    def help_stop(self):
        """Prints help message for stop command"""
        print "Stop the network with Ctrl-C"

    def do_dump(self, line):
        """Saves the network to a file.

        Parameters
        ----------
        line : string
            A string containing command line arguments. See help_dump.
        """

        # Get the args
        args = line.split()

        # Make sure only 1 argument is provided
        if not check_args(args, 1):
            return
        try:
            # Get the JSON representation of the network
            data = self.network.to_json()

            # Write the network to the file
            with open(args[0], "w") as f:
                json.dump(data, f)
        except Exception as e:
            print e

    def help_dump(self):
        """Prints help message for dump command"""
        print "dump [filename]"
        print "Saves the network to a file"

    def do_EOF(self, line):
        """Ends the program.

        Parameters
        ----------
        line : string
            A string containing command line arguments. Ignored.
        """
        print
        return True

    def help_EOF(self):
        """Prints help message for EOF command"""
        print "End the program"

    # Base methods

    def default(self, line):
        """Overrides the default method on the base class to provide shortcut
        aliases for commands.

        Commands can be entered by typing partial commands that identify a
        command uniquely.

        Parameters
        ----------
        line : string
            String containing command and argument

        """
        # Get the command and arguments
        cmd, arg, line = self.parseline(line)
        if cmd is not None:
            # Get all functions that partially match command
            func = [getattr(self, n) for n in self.get_names() if n.startswith(
                    'do_' + cmd)]

            # Run function if given command uniquely identifies a command
            if len(func) == 1:
                return func[0](arg)
        print "Command not found. Type 'help' for a list of possible commands"


def check_args(args, n):
    """Checks the provided list of args.

    Checks if the provided list of args has the correct number of args.

    Parameters
    ----------
    args : list
        A list of strings.
    n : int
        The number of arguments that should be provided.

    Returns
    -------
    boolean
        Returns True if the number of args is correct, or False otherwise.

    """
    if len(args) != n:
        print "*** invalid number of arguments"
        return False
    return True


def main():
    create_bw()


def create_bw(settings=None, f=None):
    """Creates a command module and runs it.

    Parameters
    ----------
    settings : dict, optional
        A dictionary of settings (the default is None).
    f : string, optional
        The filename containing the network (the default is None).
    """

    # Turn interactive mode on for showing graph
    plt.ion()

    # Create new instance of command module
    b = BlackWidowInteractive()

    # Set command prompt
    b.prompt = "(blackwidow) "

    # Initialize command variables
    b.create_network(settings, f)

    # Install signal handler to stop network for Ctrl-C
    def signal_handler(signal, frame):
        b.do_stop("")

    signal.signal(signal.SIGINT, signal_handler)

    # Run the command module
    b.cmdloop(intro=spider.spider + "\nWelcome to BlackWidow")


if __name__ == '__main__':
    main()
