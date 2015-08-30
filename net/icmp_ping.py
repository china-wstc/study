# -*- coding: utf-8 -*-

'''
TCP/IP详解 卷1 6.3 Page52
'''


import os
import threading
import socket
import time
import protocol

def IcmpListener():
  sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

  while True:
    data, addr = sock.recvfrom(2048)

    ipHdr = protocol.IpHeader()
    if not ipHdr.unpack(data):
      continue

    if ipHdr.protocol != protocol.IpHeader.IP_PROTOCOL_ICMP:
      print 'not icmp packet! '
      continue

    data = data[ipHdr.header_length:]

    icmp = protocol.ICMP()
    if not icmp.unpack(data):
      continue

    if icmp.i_type != protocol.ICMP.ICMP_TYPE_PING_RES:
      print 'not icmp ping res', icmp.i_type
      continue
    iping = protocol.IcmpPing()
    if not iping.unpack(data):
      continue
    print 'receive ', ipHdr, iping
    print '  --ns: %d' % ((int(time.time() * 1000) & 0xFFFFFFFF) - iping.i_data)
  return

def IcmpSender():
  sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  iam = protocol.IcmpPing()
  iam.i_type = protocol.ICMP.ICMP_TYPE_PING_REQ
  iam.i_mark = os.getpid()
  while True:
    iam.i_seqid += 1
    iam.i_data = int(time.time() * 1000) & 0xFFFFFFFF
    sock.sendto(iam.pack(), ("180.97.33.108", 1))
    time.sleep(5)
  return

def Runingbg(func, *args, **kwargs):
  thread = threading.Thread(target = func, *args, **kwargs)
  thread.setDaemon(True)
  thread.start()


def main():
  Runingbg(IcmpListener)
  IcmpSender()
  return

main()
