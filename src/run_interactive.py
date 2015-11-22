import cmd
from blackwidow import BlackWidow
from blackwidow.network import *

bw = None
network = None

class BlackWidowInteractive(cmd.Cmd):

    def do_create_network(self, line):
        self.network = Network()
        self.bw = BlackWidow()

    def do_add_router(self, line):
        args = line.split(" ")
        self.network.add_router(args[0], bw)
        print "Router"

    def do_add_host(self, line):
        args = line.split(" ")
        self.network.add_host(args[0])
        print "Host"

    def do_add_link(self, line):
        print "Link"

    def do_add_flow(self, line):
        print "Flow"

    def do_EOF(self, line):
        print
        return True

if __name__ == '__main__':
    bw = BlackWidowInteractive()
    bw.prompt = "(blackwidow) "
    bw.cmdloop()
