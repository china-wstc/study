# -*- coding: utf-8 -*-

'''
netinet/ip.h
'''

class iphdr(object):
  def __init__(self):
    # 1 Byte [4Bit Version, 4Bit Lenght]
    self.version_hlength = 0

    # 1 Byte [Type Of Service]
    self.tos = 0

    # 2 Byte [ip包长度]
    self.total_length = 0

    # 2 Byte 唯一标识
    self.uid = 0

    # 2 Byte 片偏移
    self.fragment_offset = 0

    # 1 Byte time to live
    self.ttl = 0

    # 1 Byte
    self.protocol = 0

    # 2 Byte
    self.header_check = 0

    # 4 Byte source ip addr
    self.saddr = 0

    # 4 Byte Destination ip addr
    self.daddr = 0


