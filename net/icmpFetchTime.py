# -*- coding: utf-8 -*-

'''
TCP/IP详解 卷1 6.3 Page52
'''


import socket
import icmp
import time
import os

def main():
  sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

  sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  callid = 1
  while True:
    iam = icmp.IcmpFetchTime()
    iam.i_type = 13
    iam.i_seqid = os.getpid()
    iam.i_mark  = 2
    iam.i_origt = 30000


    buff = iam.pack()

    print 'send ', len(buff), hex(iam.checksum(buff))
    sock.sendto(buff, ("192.168.1.255", 0))

    data, addr = sock.recvfrom(2048)

    iam = icmp.IcmpFetchTime()

    print addr, len(data), hex(iam.checksum(data[20:]))
    iam.unpack(data[20:])
    print addr, len(data), iam
    time.sleep(10)

main()

