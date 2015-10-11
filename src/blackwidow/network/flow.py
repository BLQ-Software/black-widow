class Flow:
    """Simple class for flows.
    
    Flows will trigger host behavior.
    """
    def __init__(self, env, name, source, destination, amount):
        """Constructor for Flow class.
        """
        self.source = source
        self.destination = destination
        self.amount = amount

    def make_packet(self, packet_num):
        """Creates a packet with specified number.
        """

    def make_ack(self, packet):
        """ Creates ack based for packet.
        """

    def send_packet(self, packet):
        """ Send a packet.
        """

    def received_packet(self, event):
        """ Generate an ack or respond to bad packet
        """

    def timeout(self, packet_num):
        """
        """


