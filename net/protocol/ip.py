# -*- coding: utf-8 -*-

'''
netinet/ip.h
'''

import struct
import socket

class IpHeader(object):

  IP_PROTOCOL_ICMP    = 1
  IP_PROTOCOL_IP      = 4
  IP_PROTOCOL_TCP     = 6
  IP_PROTOCOL_UDP     = 17

  def __init__(self):
    # 4Bit Version, 4Bit Lenght]
    self.version = 0

    # 4Bit
    self.header_length = 0

    # 1 Byte [Type Of Service]
    self.tos = 0

    # 2 Byte [ip包长度]
    self.total_length = 0

    # 2 Byte 唯一标识
    self.uid = 0

    # 3 Bit [R|DF|MF] 分片标志
    # R:  保留未用
    # DF: Don’t Fragment, 不分片位，如果将这一比特置1，IP 层将不对数据报进行分片
    # MF：More Fragment, 更多的片，除了最后一片外，其它每个组成数据报的片都要把比特置1
    self.fragment_flag = 0

    # 13 Bit 偏移
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

    # raw datas
    self.data = ''


  def __str__(self):
    indent = '  '
    return '\n'.join(('IpHeader {',
                      '%sversion: %d' % (indent, self.version),
                      '%sheader_length: %d' % (indent, self.header_length),
                      '%stos: %x' % (indent, self.tos),
                      '%stotal_length: %d' % (indent, self.total_length),
                      '%suid: %d' % (indent, self.uid),
                      '%sfragment_flag: %d' % (indent, self.fragment_flag),
                      '%sfragment_offset: %d' % (indent, self.fragment_offset),
                      '%sttl: %d' % (indent, self.ttl),
                      '%sprotocol: %d' % (indent, self.protocol),
                      '%sheader_check: %x' % (indent, self.header_check),
                      '%ssaddr: %s' % (indent, self.saddr),
                      '%sdaddr: %s' % (indent, self.daddr),
                      '}'))

  def unpack(self, buff):
    first = struct.unpack('B', buff[0])[0]
    self.version = first >> 4
    self.header_length = (first & 0xF) * 4

    if len(buff) < self.header_length:
      print 'ip header length: %d, buff_length: %d' % (self.header_length, len(buff))
      return

    _, self.tos, self.total_length, self.uid, fragment, self.ttl, self.protocol, self.header_check = \
        struct.unpack('>BBHHHBBH', buff[:12])

    self.fragment_flag = fragment >> 13
    self.fragment_offset = fragment & ((1 << 14) - 1)

    self.saddr = socket.inet_ntoa(buffer(buff, 12, 4))
    self.daddr = socket.inet_ntoa(buffer(buff, 16, 4))

    self.data = buff[20:]
    return True

class Udp(object):
  def __init__(self):
    self.src_port = 0
    self.dest_port = 0
    self.udp_length = 0
    self.udp_checksum = 0
    self.data = ''

  def __str__(self):
    indent = '  '
    return '\n'.join(('Udp {',
                      '%ssrc_port: %d' % (indent, self.src_port),
                      '%sdest_port: %d' % (indent, self.dest_port),
                      '%slength: %d' % (indent, self.udp_length),
                      '%schecksum: %x' % (indent, self.udp_checksum),
                      '}'))

  def unpack(self, buff):
    self.src_port, self.dest_port, self.udp_length, self.udp_checksum = \
        struct.unpack('>HHHH', buff[:8])
    self.data = buff[8:]


