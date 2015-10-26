# -*- coding: utf-8 -*-


import protocol
import socket
import binascii
import time
import threading


def ListenIp():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0800))

  while True:
    buff = sock.recv(2048)
    eth = protocol.EtherHeader()
    eth.unpack(buff[: 14])

    ip = protocol.IpHeader()
    ip.unpack(buff[14: ])
    if ip.protocol != ip.IP_PROTOCOL_UDP:
      continue

    udp = protocol.Udp()

    print eth
    print ip

    print hex(udp.CheckSum(ip, ip.data))

    udp.unpack(ip.data)
    print udp
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
