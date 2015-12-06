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

    def create_network(self, settings, f):
        if settings is None:
            self.bw = BlackWidow()
            self.network = Network(self.bw)
        else:
            self.bw = BlackWidow(settings)
            self.network = parser.config_network(f, self.bw)
        self.do_reset_v("")
        self.do_clear("")
        f = plt.figure(2)
        self.do_show("")

    def do_reset_v(self, line):
        """Reset parameters for interactive"""
        self.dpi = "300"
        self.proj = "dot"
        self.show_network = True
        self.output = False

    def do_reset(self, line):
        """Reset network"""
        self.bw = BlackWidow()
        self.network = Network(self.bw)
        self.do_reset_v("")

    def do_set_verbose(self, line):
        """set_verbose [verbose]
        Set verbose output"""
        args = line.split()
        if not check_args(args, 1):
            return
        if args[0] == "True":
            self.bw.real_time = True
        else:
            self.bw.real_time = False

    def do_set_static_routing(self, line):
        """set_static_routing [static_routing]
        Set static routing"""
        args = line.split()
        if not check_args(args, 1):
            return
        if args[0] == "True":
            self.bw.static_routing = True
        else:
            self.bw.static_routing = False

    def do_set_routing_packet_size(self, line):
        """set_routing_packet_size [size]
        Set routing packet size"""
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            self.bw.routing_packet_size = float(args[0])
        except Exception as e:
            print e

    def do_set_tcp_alg(self, line):
        """set_tcp_alg [alg]
        Set TCP algorithm"""
        args = line.split()
        if not check_args(args, 1):
            return
        self.bw.tcp_alg = args[0]

    def do_add_router(self, line):
        """add_router [id]
        Add a router"""
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            self.network.add_router(args[0], self.bw)
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e


    def do_add_host(self, line):
        """add_host [id]
        Add a host"""
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            self.network.add_host(args[0])
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def do_delete_device(self, line):
        """delete_device [id]
        Delete a device"""
        args = line.split()
        if len(args) < 1:
            return
        try:
            if len(args) == 1 and args[0] == "*":
                for id in self.network.devices.keys()[:]:
                    self.network.delete_device(id)
            else:
                for id in args:
                    self.network.delete_device(id)
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def do_add_link(self, line):
        """add_link [id] [device_id] [device_id] [delay] [rate] [buffer]
        Add a link"""
        args = line.split()
        if not check_args(args, 6):
            return

        try:
            self.network.add_link(args[0], args[1], args[2], float(args[3]), float(args[4]), float(args[5]), self.bw)
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def do_delete_link(self, line):
        """delete_link [id]
        Delete a link"""
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            self.network.delete_link(args[0])
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def do_add_flow(self, line):
        """add_flow [id] [src] [dest] [amount] [start]
        Add a flow"""
        args = line.split()
        if not check_args(args, 5):
            return
        try:
            self.network.add_flow(args[0], args[1], args[2], float(args[3]), float(args[4]), self.bw)
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def do_delete_flow(self, line):
        """delete_flow [id]
        Delete a flow"""
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            self.network.delete_flow(args[0])
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def do_load(self, line):
        """load [filename]
        Load a file"""
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            base = os.path.basename(args[0])
            self.bw = BlackWidow({'log_file': os.path.splitext(base)[0]})
            self.network = parser.config_network(args[0], self.bw)
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e


    def do_show(self, line):
        """Show the network"""
        try:
            d = self.network.dump(self.output)
            d.set_dpi(self.dpi)
            png_str = d.create_png(prog=self.proj)
            sio = StringIO()
            sio.write(png_str)
            sio.seek(0)

            image = mpimg.imread(sio)
            plt.axis('off')
            plt.imshow(image)
            plt.show()
        except Exception as e:
            print e

    def do_run(self, line):
        """Run the network"""
        try:
            self.bw.run_network(self.network)
        except Exception as e:
            print e

    def do_clear(self, line):
        """Clear the graph"""
        plt.clf()

    def do_close(self, line):
        """Close the graph"""
        plt.close()

    def do_set_show(self, line):
        """set_show [show]
        Show the network after every command if show == True"""
        args = line.split()
        if not check_args(args, 1):
            return False
        if args[0] == "True":
            self.show_network = True
        else:
            self.show_network = False

    def do_set_output(self, line):
        """set_output [output]
        Show text output of the network if output == True"""
        args = line.split()
        if not check_args(args, 1):
            return False
        if args[0] == "True":
            self.output = True
        else:
            self.output = False

    def do_set_dpi(self, line):
        """set_dpi [dpi]
        Set the dpi"""
        args = line.split()
        if not check_args(args, 1):
            return
        self.dpi = args[0]
        if self.show_network:
            self.do_show("")

    def do_set_proj(self, line):
        """set_proj [proj]
        Set the projection type"""
        args = line.split()
        if not check_args(args, 1):
            return
        self.proj = args[0]
        if self.show_network:
            self.do_show("")

    def do_exit(self, line):
        """End the program"""
        print
        return True

    def do_stop(self, line):
        """Stop the network with Ctrl-C"""
        self.network.empty()

    def do_dump(self, line):
        """dump [filename]
        Saves the network to a file"""
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            data = self.network.to_json()
            with open(args[0], "w") as f:
                json.dump(data, f)
        except Exception as e:
            print e


    def do_EOF(self, line):
        """End the program"""
        print
        return True

    # Base methods

    def default(self, line):
        cmd, arg, line = self.parseline(line)
        if cmd is not None:
            func = [getattr(self, n) for n in self.get_names() if n.startswith('do_' + cmd)]
            if len(func) == 1:
                return func[0](arg)
        print "Command not found. Type 'help' for a list of possible commands"

def check_args(args, n):
    if len(args) != n:
        print "*** invalid number of arguments"
        return False
    return True

def main():
    create_bw()

def create_bw(settings=None, f=None):
    plt.ion()
    b = BlackWidowInteractive()
    b.prompt = "(blackwidow) "
    b.create_network(settings, f)

    def signal_handler(signal, frame):
        b.do_stop("")

    signal.signal(signal.SIGINT, signal_handler)

    b.cmdloop(intro=spider.spider + "\nWelcome to BlackWidow")


if __name__ == '__main__':
    main()
