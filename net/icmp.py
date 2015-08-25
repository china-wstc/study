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


  def unpack(self, buff):
    self.i_type, self.i_code, self.i_checksum = \
        struct.unpack('>BBH', buff[:4])
    return



class IcmpAddrMask(ICMP):
  def __init__(self):
    super(IcmpAddrMask, self).__init__()
    # 4Byte [2Byte标识符、2Byte序列号], 其实就是一个rpc的token
    self.i_token = 0

    # 4Byte 掩码
    self.i_mask = 0
    return


  def _checksum(self):
    def _s(num):
      return (~num) & 0xFFFF

    # little endian
    csum = _s(self.i_type << 8)
    csum += _s(self.i_checksum)

    csum = (csum >> 16) + (csum & 0xFFFF)
    csum += _s(self.i_token >> 16)

    csum = (csum >> 16) + (csum & 0xFFFF)
    csum += _s(self.i_token & 0xFFFF)

    csum = (csum >> 16) + (csum & 0xFFFF)

    csum += _s(self.i_mask >> 16)
    csum = (csum >> 16) + (csum & 0xFFFF)

    csum += _s(self.i_mask & 0xFFFF)
    csum = (csum >> 16) + (csum & 0xFFFF)
    return csum

  def _pack(self):
    buff = self._pack()
    csum = 0
    for num in struct.unpack('>%sH' % (len(buff) / 2), buff):
      csum += num
      csum = (csum >> 16) + (csum & 0xFFFF)
    csum = (~csum) & 0xFFFF

    print 'check sum2 ', csum
    return

  def pack(self):
    self.i_checksum = self._checksum()
    print 'check sum ', self._checksum()
    return struct.pack('>BBHII', self.i_type, self.i_code, self.i_checksum, self.i_token, self.i_mask)

  def unpack(self, buff):
    self.i_type, self.i_code, self.i_checksum, self.i_token, self.i_mask = \
        struct.unpack('>BBHII', buff)
    return

