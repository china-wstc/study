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

def main():
  sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
  sock.bind(("eth0", 0x0806))

  for i in range(255):
    eth, arp = InitArpRequest("192.168.11.%s" % i)
    data = eth.pack() + arp.pack() + chr(0) * 18
    sock.send(data)
    time.sleep(1)

  while True:
    time.sleep(1)
  return

thread = threading.Thread(target = ListenArp)
thread.setDaemon(True)
thread.start()
main()
