# -*- coding: utf-8 -*-

import utils
import struct
import socket

class EtherHeader(object):
  def __init__(self):
    self.ether_dhost = ''
    self.ether_shost = ''
    self.ether_type = 0


  def __str__(self):
    return 'EtherHeader: ' + \
           ','.join(('dhost: %s' % self.ether_dhost,
                     'shost: %s' % self.ether_shost,
                     'type: %s' % hex(self.ether_type)))

  def unpack(self, buff):
    self.ether_dhost = utils.eth_btoa(buff[:6])
    self.ether_shost = utils.eth_btoa(buff[6:12])
    self.ether_type = struct.unpack(">H", buff[12: 14])[0]

  def pack(self):
    return utils.eth_atob(self.ether_dhost) + \
           utils.eth_atob(self.ether_shost) + \
           struct.pack('>H', self.ether_type)

class ArpProtocol(object):
  def __init__(self):
    # 2Byte 硬件类型
    self.arp_hardware = 0x0800

    # 2Byte 协议类型
    self.arp_protocol = 0x0001

    # 1Byte 硬件地址长度
    self.arp_haddr_len = 6

    # 1Byte 协议地址长度
    self.arp_paddr_len = 4

    # 2Byte 操作类型
    self.arp_oper = 0

    self.arp_eth_src = ''
    self.arp_ip_src = ''

    self.arp_eth_dest = ''
    self.arp_ip_dest = ''

  def __str__(self):
    return 'ArpProtocol: ' + \
           ', '.join(('hardware: %d' % self.arp_hardware,
                      'protocol: %s' % hex(self.arp_protocol),
                      'haddr_len: %d' % self.arp_haddr_len,
                      'paddr_len: %d' % self.arp_paddr_len,
                      'oper: %d' % self.arp_oper,
                      'eth_src: %s' % self.arp_eth_src,
                      'ip_src: %s' % self.arp_ip_src,
                      'eth_dest: %s' % self.arp_eth_dest,
                      'ip_dect: %s' % self.arp_ip_dest,
                     ))

  def __eq__(self, other):
    for k, v in self.__dict__.items():
      if k.startswith('arp_') and v != other.__dict__[k]:
        return False
    return True

  def unpack(self, buff):
    self.arp_hardware, self.arp_protocol, self.arp_haddr_len, self.arp_paddr_len, self.arp_oper = \
        struct.unpack(">HHBBH", buff[: 8])
    self.arp_eth_src = utils.eth_btoa(buff[8: 14])
    self.arp_ip_src = utils.inet_btoa(buff[14: 18])

    self.arp_eth_dest = utils.eth_btoa(buff[18: 24])
    self.arp_ip_dest = utils.inet_btoa(buff[24: 28])

  def pack(self):
    return struct.pack('>HHBBH', self.arp_hardware, self.arp_protocol, self.arp_haddr_len, self.arp_paddr_len, self.arp_oper) + \
        utils.eth_atob(self.arp_eth_src) + \
        socket.inet_aton(self.arp_ip_src) + \
        utils.eth_atob(self.arp_eth_dest) + \
        socket.inet_aton(self.arp_ip_dest)


