# -*- coding: utf-8 -*-

import utils
import struct

class EtherHeader(object):
  def __init__(self):
    self.ether_dhost = ''
    self.ether_shost = ''
    self.ether_type = 0


  def __str__(self):
    return 'ether_dhost: %s, ether_shost: %s, ether_type: %s' % \
        (self.ether_dhost, self.ether_shost, hex(self.ether_type))

  def unpack(self, buff):
    self.ether_dhost = utils.eth_btoa(buff[:6])
    self.ether_shost = utils.eth_btoa(buff[6:12])
    self.ether_type = struct.unpack(">H", buff[12: 14])[0]

