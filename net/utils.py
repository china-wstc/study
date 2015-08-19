# -*- coding: utf-8 -*-

import binascii
import struct

def eth_btoa(buff):
  '''
  Net order bytes to Hex Mac Addr
  '''
  assert len(buff) == 6, "mac addr bytes must length 6"

  return binascii.b2a_hex(buff)

def inet_btoa(buff):
  '''
  Net order bytes To IP addr xxx.xxx.xxx.xxx
  '''

  assert len(buff) == 4, "ip addr bytes must length 4"

  return '.'.join([str(byte) for byte in struct.unpack('4B', buff)])

