# -*- coding: utf-8 -*-

import protocol
import socket
import binascii
import time
import threading

def InitRarpRequest():
  eth = protocol.EtherHeader()
  eth.ether_dhost = 'ffffffffffff'
  eth.ether_shost = '000c29739926'
  eth.ether_type  = 0x0835

  rarp = protocol.RarpProtocol()
  rarp.rarp_hardware  = 0x0001
  rarp.rarp_protocol  = 0x0800
  rarp.rarp_haddr_len = 0x06
  rarp.rarp_paddr_len = 0x04
  rarp.rarp_oper      = 0x0003

  rarp.rarp_eth_src   = '000c29739926'
  rarp.rarp_ip_src    = '0.0.0.0'
  rarp.rarp_eth_dest  = 'ffffffffffff'
  rarp.rarp_ip_dest   = '0.0.0.0'

  return (eth, rarp)


def ListenRarp():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0835))

  while True:
    buff = sock.recv(2048)
    eth, rarp = protocol.EtherHeader(), protocol.RarpProtocol()

    eth.unpack(buff[: 14])
    rarp.unpack(buff[14: ])
    print 'rarp : ', rarp
  return

def SendRarpRequest():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0835))

  while True:
    eth, rarp = InitRarpRequest()
    data = eth.pack() + rarp.pack() + chr(0) * 18

    rarp1 = protocol.RarpProtocol()
    rarp1.unpack(rarp.pack())

    print '------------', rarp1
    sock.send(data)
    print 'send request', eth, rarp
    time.sleep(10)
  return

def Runingbg(func, *args, **kwargs):
  thread = threading.Thread(target = func, *args, **kwargs)
  thread.setDaemon(True)
  thread.start()


def main():
  while True:
    time.sleep(1)

Runingbg(SendRarpRequest)
Runingbg(ListenRarp)

main()
