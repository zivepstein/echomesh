#!/usr/bin/python

# From here: http://stackoverflow.com/questions/159137/getting-mac-address
# Only works on Linux.

import fcntl, socket, struct

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def MacAddress():
  return getHwAddr('eth0')

