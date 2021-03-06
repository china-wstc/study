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

    if icmp.i_type != protocol.ICMP.ICMP_TYPE_ADDR_MASK_RES and \
        icmp.i_type != protocol.ICMP.ICMP_TYPE_ADDR_MASK_REQ:
      print 'not icmp addr mask', icmp.i_type
      continue
    imsk = protocol.IcmpAddrMask()
    if not imsk.unpack(data):
      continue

    print 'receive ', ipHdr, imsk
  return

def IcmpSender():
  sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  iam = protocol.IcmpAddrMask()
  iam.i_type = 17
  iam.i_seqid = os.getpid()
  iam.i_mask = 0
  while True:
    iam.i_mark += 1
    sock.sendto(iam.pack(), ("192.168.11.255", 1))
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
