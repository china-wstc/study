# -*- coding: utf-8 -*-

import binascii
import struct

class EtherHeader(object):
  def __init__(self):
    self.ether_dhost = ''
    self.ether_shost = ''
    self.ether_type = 0


  def format_mac(self, mac):
    mac = mac.upper()
    mac = [mac[:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10]]
    return '-'.join(mac)

  def __str__(self):
    indent = '  '
    return '\n'.join(('EtherHeader: {',
                      '%sdhost: %s' % (indent, self.format_mac(self.ether_dhost)),
                      '%sshost: %s' % (indent, self.format_mac(self.ether_shost)),
                      '%stype: %s' % (indent, hex(self.ether_type)),
                      '}'))

  def unpack(self, buff):
    self.ether_dhost = binascii.b2a_hex(buff[:6])
    self.ether_shost = binascii.b2a_hex(buff[6:12])
    self.ether_type = struct.unpack(">H", buff[12: 14])[0]

  def pack(self):
    return binascii.a2b_hex(self.ether_dhost) + \
           binascii.a2b_hex(self.ether_shost) + \
           struct.pack('>H', self.ether_type)

