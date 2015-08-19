# -*- coding: utf-8 -*-


import arp
import ether
import socket

def main():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0806))

  while True:
    data = sock.recv(2048)

    eth = ether.EtherHeader()
    eth.unpack(data)

    ar = arp.ArpProtocol()
    ar.unpack(data[14: ])

    print eth
    print ar
  return

main()
