# -*- coding: utf-8 -*-


import protocol
import socket
import binascii
import time
import threading


def ListenIp():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0800))

  global ARP_TABLE
  while True:
    buff = sock.recv(2048)
    eth, arp = protocol.EtherHeader(), protocol.ArpProtocol()

    eth.unpack(buff[: 14])
    print eth
  return

def Runingbg(func, *args, **kwargs):
  thread = threading.Thread(target = func, *args, **kwargs)
  thread.setDaemon(True)
  thread.start()


def main():
  while True:
    time.sleep(1)

Runingbg(ListenIp)

main()
