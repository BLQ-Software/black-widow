import os
import cmd

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from blackwidow import BlackWidow
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

    def do_add_router(self, line):
        args = line.split()
        if len(args) != 1:
            print "*** invalid number of arguments"
            return
        try:
            self.network.add_router(args[0], self.bw)
        except Exception as e:
            print e

    def do_add_host(self, line):
        args = line.split()
        if len(args) != 1:
            print "*** invalid number of arguments"
            return
        try:
            self.network.add_host(args[0])
        except Exception as e:
            print e

    def do_add_link(self, line):
        args = line.split()
        if len(args) != 6:
            print "*** invalid number of arguments"
            return

        try:
            self.network.add_link(args[0], args[1], args[2], float(args[3]), float(args[4]), float(args[5]), self.bw)
        except Exception as e:
            print e

    def do_add_flow(self, line):
        args = line.split()
        if len(args) != 5:
            print "*** invalid number of arguments"
            return
        try:
            self.network.add_flow(args[0], args[1], args[2], float(args[3]), float(args[4]), self.bw)
        except Exception as e:
            print e

    def do_show_network(self, line):
        d = self.network.dump(self.filename + ".dot")
        d.set_dpi(self.dpi)
        png_str = d.create_png()
        sio = StringIO()
        sio.write(png_str)
        sio.seek(0)

        image = mpimg.imread(sio)
        plt.axis('off')
        plt.imshow(image)
        plt.show()

    def do_run(self, line):
        self.bw.run_network(self.network)

    def do_set_dpi(self, line):
        args = line.split()
        if len(args) != 1:
            print "*** invalid number of arguments"
            return
        self.dpi = args[0]


    def do_EOF(self, line):
        print
        return True

if __name__ == '__main__':
    b = BlackWidowInteractive()
    b.prompt = "(blackwidow) "
    b.do_create_network("")
    b.cmdloop(intro="Welcome to BlackWidow")
