from blackwidow.network.device import Device
from blackwidow.network.host import Host

def test_construct():
    d = Device('H1')
    assert d.net_addr == 'H1'
