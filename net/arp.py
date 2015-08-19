# -*- coding: utf-8 -*-

import utils
import struct

class ArpProtocol(object):
  def __init__(self):
    # 硬件类型 [2Byte]
    self.arp_hardware = 0

    # 协议类型 [2Byte]
    self.arp_protocol = 0

    # 硬件地址长度 [1Byte]
    self.arp_haddr_len = 0

    # 协议地址长度 [1Byte]
    self.arp_paddr_len = 0

    self.arp_oper = 0

    self.arp_eth_src = ''
    self.arp_ip_src = ''

    self.arp_eth_dest = ''
    self.arp_ip_dest = ''

  def __str__(self):
    return ', '.join(('arp_hardware: %d' % self.arp_hardware,
                      'arp_protocol: %s' % hex(self.arp_protocol),
                      'arp_haddr_len: %d' % self.arp_haddr_len,
                      'arp_paddr_len: %d' % self.arp_paddr_len,
                      'arp_oper: %d' % self.arp_oper,
                      'arp_eth_src: %s' % self.arp_eth_src,
                      'arp_ip_src: %s' % self.arp_ip_src,
                      'arp_eth_dest: %s' % self.arp_eth_dest,
                      'arp_ip_dect: %s' % self.arp_ip_dest,
                     ))

  def unpack(self, buff):
    self.arp_hardware, self.arp_protocol, self.arp_haddr_len, self.arp_paddr_len, self.arp_oper = \
        struct.unpack(">HHBBH", buff[: 8])
    self.arp_eth_src = utils.eth_btoa(buff[8: 14])
    self.arp_ip_src = utils.inet_btoa(buff[14: 18])

    self.arp_eth_dest = utils.eth_btoa(buff[18: 24])
    self.arp_ip_dest = utils.inet_btoa(buff[24: 28])


