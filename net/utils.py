# -*- coding: utf-8 -*-

import binascii
import struct
import socket

def eth_btoa(buff):
  '''
  Net order bytes to Hex Mac Addr
  '''
  assert len(buff) == 6, "mac addr bytes must length 6"

  return binascii.b2a_hex(buff)

def eth_atob(addr):
  '''
  hex max addr to net order bytes
  '''
  assert len(addr) == 12, "mac hex addr must length 12"

  return binascii.a2b_hex(addr)

def inet_btoa(buff):
  '''
  Net order bytes To IP addr xxx.xxx.xxx.xxx
  '''

  assert len(buff) == 4, "ip addr bytes must length 4"

  return '.'.join([str(byte) for byte in struct.unpack('4B', buff)])

def inet_atob(addr):
  '''
  IP addr xxx.xxx.xxx.xxx TO net order bytes
  '''

  return struct.pack('>I', socket.inet_aton(addr))

