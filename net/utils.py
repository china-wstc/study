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


