# -*- coding: utf-8 -*-

import struct

class ICMP(object):


  ICMP_TYPE_PING_RES        = 0
  ICMP_TYPE_PING_REQ        = 8

  # 地址掩码请求
  ICMP_TYPE_ADDR_MASK_REQ   = 17
  # 地址掩码回应
  ICMP_TYPE_ADDR_MASK_RES   = 18

  def __init__(self):
    # 1Byte 类型
    self.i_type = 0

    # 1Byte 代码
    self.i_code = 0

    # 2Byte
    self.i_checksum = 0


  def __str__(self):
    indent = '  '
    return '\n'.join(('ICMP {',
                      '%si_type: %d' % (indent, self.i_type),
                      '%si_code: %d' % (indent, self.i_code),
                      '%si_checksum: %x' % (indent, self.i_checksum),
                      '}'))

  def checksum(self, buff):
    sum = 0
    for num in struct.unpack('>%sH' % (len(buff) / 2), buff):
      sum += (~num) & 0xFFFF
      sum = (sum >> 16) + sum & 0xFFFF
    return sum & 0xFFFF


  def unpack(self, buff):
    self.i_type, self.i_code, self.i_checksum = \
        struct.unpack('>BBH', buff[:4])
    return True

  def _pack(self):
    return ''

  def pack(self):
    self.i_checksum = 0
    buff = self._pack()
    return buff[:2] + struct.pack('>H', self.checksum(buff)) + buff[4:]

class IcmpAddrMask(ICMP):
  def __init__(self):
    super(IcmpAddrMask, self).__init__()
    # 2 Byte 标识符
    self.i_mark = 0
    # 2 Byte 序列号
    self.i_seqid = 0

    # 4Byte 掩码
    self.i_mask = 0
    return

  def __str__(self):
    indent = '  '
    return '\n'.join(('IcmpAddrMask: {',
                      '%si_type: %d' % (indent, self.i_type),
                      '%si_code: %d' % (indent, self.i_code),
                      '%si_checksum: %x' % (indent, self.i_checksum),
                      '%si_mark: %d' % (indent, self.i_mark),
                      '%si_seqid: %d' % (indent, self.i_seqid),
                      '%si_mask: %x' % (indent, self.i_mask),
                      '}'))

  def _pack(self):
    self.i_checksum = 0
    return struct.pack('>BBHHHI', self.i_type, self.i_code, self.i_checksum, self.i_mark, self.i_seqid, self.i_mask)

  def unpack(self, buff):
    self.i_type, self.i_code, self.i_checksum, self.i_mark, self.i_seqid, self.i_mask = \
        struct.unpack('>BBHHHI', buff)
    return True

class IcmpFetchTime(ICMP):
  def __init__(self):
    super(IcmpFetchTime, self).__init__()

    # 2 Byte 标识符
    self.i_mark = 0
    # 2 Byte 序列号
    self.i_seqid = 0

    # 4 Byte 发起时间
    self.i_origt = 0

    # 4 Byte 接收时间
    self.i_recvt = 0

    # 4 Byte 传送时间
    self.i_sendt = 0

  def __str__(self):
    return 'IcmpFetchTime ' + \
        ', '.join(('i_type: %d' % self.i_type,
                   'i_code: %d' % self.i_code,
                   'i_checksum: %s' % hex(self.i_checksum),
                   'i_mark: %d' % self.i_mark,
                   'i_seqid: %d' % self.i_seqid,
                   'i_origt: %d' % self.i_origt,
                   'i_recvt: %d' % self.i_recvt,
                   'i_sendt: %d' % self.i_sendt,
                   ))

  def _pack(self):
    self.i_checksum = 0
    return struct.pack('>BBH2H3I',
        self.i_type,
        self.i_code,
        self.i_checksum,
        self.i_mark,
        self.i_seqid,
        self.i_origt,
        self.i_recvt,
        self.i_sendt
        )

  def unpack(self, buff):
    self.i_type, \
    self.i_code, \
    self.i_checksum, \
    self.i_mark, \
    self.i_seqid, \
    self.i_origt, \
    self.i_recvt, \
    self.i_sendt = struct.unpack('>BBH2H3I', buff)
    return

class IcmpPing(ICMP):
  def __init__(self):
    super(IcmpPing, self).__init__()
    self.i_mark = 0
    self.i_seqid = 0
    self.i_data = 0

  def __str__(self):
    indent = '  '
    return '\n'.join(('IcmpPing: {',
                      '%si_type: %d' % (indent, self.i_type),
                      '%si_code: %d' % (indent, self.i_code),
                      '%si_checksum: %x' % (indent, self.i_checksum),
                      '%si_mark: %d' % (indent, self.i_mark),
                      '%si_seqid: %d' % (indent, self.i_seqid),
                      '%si_data: %d' % (indent, self.i_data),
                      '}'))


  def _pack(self):
    self.i_checksum = 0
    return struct.pack('>BBHHHI', self.i_type, self.i_code, self.i_checksum, self.i_mark, self.i_seqid, self.i_data)

  def unpack(self, buff):
    self.i_type, self.i_code, self.i_checksum, self.i_mark, self.i_seqid, self.i_data = \
        struct.unpack('>BBHHHI', buff)
    return True

