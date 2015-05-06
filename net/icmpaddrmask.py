# -*- coding: utf-8 -*-

'''
TCP/IP详解 卷1 6.3 Page52
'''


import socket
import icmp
import time

def main():
  sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  callid = 1
  while True:
    iam = icmp.IcmpAddrMask()
    iam.i_type = 17
    iam.i_token = callid
    iam.i_mask = 0


    sock.sendto(iam.pack(), ("192.168.1.255", 1))

    data, addr = sock.recvfrom(2048)

    print len(data)

    iam = icmp.IcmpAddrMask()
    iam.unpack(data[20:])

    print addr, iam

    time.sleep(10)

main()

