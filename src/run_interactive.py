import os
import cmd
from blackwidow import BlackWidow
from blackwidow.network import *


class BlackWidowInteractive(cmd.Cmd):

    def do_create_network(self, line):
        args = line.split()
        if len(args) == 1:
            self.filename = args[0]
        else:
            self.filename = "test.dot"
        self.network = Network()
        self.bw = BlackWidow()

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
        except AttributeError:
            print "*** network must be created first"

    def do_show_network(self, line):
        self.network.dump(self.filename)
        os.system("dot -T png -Gdpi=3000 {0} > {1}.png ; open {1}.png".format(self.filename, self.filename[0:-4]))

    def do_run(self, line):
        self.bw.run_network(self.network)


    def do_EOF(self, line):
        print
        return True

if __name__ == '__main__':
    b = BlackWidowInteractive()
    b.prompt = "(blackwidow) "
    b.cmdloop(intro="Welcome to BlackWidow")
