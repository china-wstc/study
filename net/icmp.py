# -*- coding: utf-8 -*-

import struct


class ICMP(object):
  def __init__(self):
    # 1Byte 类型
    self.i_type = 0

    # 1Byte 代码
    self.i_code = 0

    # 2Byte
    self.i_checksum = 0


  def __str__(self):
    return 'ICMP: ' + ', '.join(('i_type: %d' % self.i_type,
                                 'i_code: %d' % self.i_code,
                                 'i_checksum: %s' % hex(self.i_checksum)))


  def checksum(self, buff):
    sum = 0
    for num in struct.unpack('>%sH' % (len(buff) / 2), buff):
      sum += (~num) & 0xFFFF
      sum = (sum >> 16) + sum & 0xFFFF
    return sum & 0xFFFF


  def unpack(self, buff):
    self.i_type, self.i_code, self.i_checksum = \
        struct.unpack('>BBH', buff[:4])
    return

  def _pack(self):
    return ''

  def pack(self):
    self.i_checksum = 0
    buff = self._pack()
    print '----------', len(buff), self.checksum(buff)
    return buff[:2] + struct.pack('>H', self.checksum(buff)) + buff[4:]


class IcmpAddrMask(ICMP):
  def __init__(self):
    super(IcmpAddrMask, self).__init__()
    # 4Byte [2Byte标识符、2Byte序列号], 其实就是一个rpc的token
    self.i_token = 0

    # 4Byte 掩码
    self.i_mask = 0
    return

  def _pack(self):
    self.i_checksum = 0
    return struct.pack('>BBHII', self.i_type, self.i_code, self.i_checksum, self.i_token, self.i_mask)

  def unpack(self, buff):
    self.i_type, self.i_code, self.i_checksum, self.i_token, self.i_mask = \
        struct.unpack('>BBHII', buff)
    return

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

