import os
import cmd

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from blackwidow import BlackWidow
from blackwidow import parser
from blackwidow.network import *

from cStringIO import StringIO

plt.ion()


class BlackWidowInteractive(cmd.Cmd):

    def do_create_network(self, line):
        args = line.split()
        if len(args) == 1:
            self.filename = args[0]
        else:
            self.filename = "test"
        self.network = Network()
        self.bw = BlackWidow()
        self.dpi = "300"
        self.proj = "dot"
        self.show_network = True
        self.output = True

    def do_add_router(self, line):
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
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            self.network.delete_device(args[0])
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e

    def do_add_link(self, line):
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
        args = line.split()
        if not check_args(args, 1):
            return
        try:
            self.bw = BlackWidow()
            self.network = parser.config_network(args[0], self.bw)
            if self.show_network:
                self.do_show("")
        except Exception as e:
            print e


    def do_show(self, line):
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
        self.bw.run_network(self.network)

    def do_set_show(self, line):
        args = line.split()
        if not check_args(args, 1):
            return False
        if args[0] == "True":
            self.show_network = True
        else:
            self.show_network = False

    def do_set_output(self, line):
        args = line.split()
        if not check_args(args, 1):
            return False
        if args[0] == "True":
            self.output = True
        else:
            self.output = False

    def do_set_dpi(self, line):
        args = line.split()
        if not check_args(args, 1):
            return
        self.dpi = args[0]

    def do_set_proj(self, line):
        args = line.split()
        if not check_args(args, 1):
            return
        self.proj = args[0]


    def do_EOF(self, line):
        print
        return True

def check_args(args, n, values=None):
    if len(args) != n:
        print "*** invalid number of arguments"
        return False
    if values is not None:
        for v in args:
            if v not in x:
                print "*** invalid argument: {0}".format(v)
                return False
    return True

if __name__ == '__main__':
    b = BlackWidowInteractive()
    b.prompt = "(blackwidow) "
    b.do_create_network("")
    b.cmdloop(intro="Welcome to BlackWidow")
