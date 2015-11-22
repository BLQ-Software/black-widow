import cmd

class BlackWidowInteractive(cmd.Cmd):
    def do_add_router(self, line):
        print "Router"
    def do_add_host(self, line):
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
