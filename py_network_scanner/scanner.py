import argparse
import nmap
import pyfiglet
import scapy.all as scapy
import socket
import sys

from colorama import Fore, Back, Style
from datetime import datetime
from scapy.all import srp, Ether, ARP, conf
from tabulate import tabulate


'''
Notities uit gesprek met Mark:
Udp poorten moeten nog worden geimplementeerd, helemaal vergeten xd
Poorten staan nu nog op maar 2 vanwege het testen, dit nog snel omzetten naar een loop
Kijken naar multithreading
Scannen alleen in het eigen netwerk
'''


def main():
    # Define the parser
    parser = argparse.ArgumentParser(description="A nice network scanner based on python's scapy and socket module")
    # Get the address
    parser.add_argument('target', help='Input a network address or a subnet')
    # Get the flags
    parser.add_argument('-m', '--mac', help='Choose if you want the mac address', action='store_true')
    parser.add_argument('-s', '--service', help='Choose if you want an estimation of the service behind a port', action='store_true')
    parser.add_argument('-n', '--hostname', help='Choose if you want an estimation of the hostname', action='store_true')
    parser.add_argument('-f', '--fingerprint', help='Choose if you want an estimation of the OS name', action='store_true')
    # Parse the flags
    args = parser.parse_args()

    printart()
    
    print("-----------------------------------------------------------------------------------")

    # Check the subnet
    target = args.target
    if '/' not in target:  # Check if subnet is included
        # If no subnet, add the /32 subnet so it only scans one host
        target = target + '/32'
    
    print(Fore.MAGENTA + 'Starting the scan for the subnet: ', target)
    print("-----------------------------------------------------------------------------------")

    print(Fore.BLUE)

    # Check the mac option
    if args.mac:
        mac = args.mac
        ip_list, mac_list = scan_ip_and_mac(target, mac)
    else:
        ip_list = scan_ip_and_mac(target, False)

    if len(ip_list) < 1:
        sys.exit("Found nothing")


    # If service option is not used, set it to false
    if not args.service:
        service = False
    else:
        service = True

    for ip in ip_list:
        open_ports = []
        closed_ports = []
        services = []

        #port_list = [21221, 31016, 5601, 10051]
        port_list = [22, 80]
        print(Fore.GREEN)
        print("-----------------------------------------------------------------------------------")
        for port in port_list:
        #for port in range(1, 1025):
                status, service_name = port_and_service_scan(ip, port, service)
                if status and service:
                    open_ports.append(str(port))
                    services.append(service_name)
                    print("ip: ", ip, "port: ", port, "service: ", service_name)
                elif status and not service:
                    open_ports.append(str(port))
                    print("ip: ", ip, "port: ", port)
                elif not status:
                    closed_ports.append(str(port))

    print(Fore.CYAN)
    print("-----------------------------------------------------------------------------------")
    if args.mac:
        print("ip: ", ip_list, "mac: ", mac_list)
    else:
        print("ip: ", ip_list)
    
    print(Fore.YELLOW)
    print("-----------------------------------------------------------------------------------")
    for ip in ip_list:
        if args.hostname:
            hostname_list = hostname(ip)
            print("ip: ", ip, "hostname : ", hostname_list)
    
    print(Fore.RED)
    print("-----------------------------------------------------------------------------------")
    for ip in ip_list:
        if args.fingerprint:
            fingerprint_list = os_fingerprint(ip)
            print("Os version: ", fingerprint_list)    

    print(Fore.RESET)
    print("-----------------------------------------------------------------------------------")



def os_fingerprint(ip):

  # Hardcoded becouse nmap wants to make my life hard
  path = [r"C:\Program Files (x86)\Nmap\nmap.exe",] 

  nm = nmap.PortScanner(nmap_search_path=path)

  os_scan = nm.scan(ip, arguments='-O')

  return os_scan['scan'][ip]['osmatch'][0]['name']


def hostname(ip):

  try:
    hostname = socket.gethostbyaddr(ip)
  except socket.herror as e:
    if e.errno == 11004:
        hostname = "not found"
    else:
        hostname = "Socket error occured"
  except Exception as e:
        hostname = "Something went wrong"

  return hostname   



# 2.c and d, open ports and the services that belong to it
def port_and_service_scan(ip, port, service):
    # Make a new socket object
        # AF_INET is IPV4
        # SOCK_STREAM is TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect_ex() returns 0 if it can connect
    socket.setdefaulttimeout(1)
    result = s.connect_ex((ip, port))

    if result == 0 and service:
        try:
            service_name = socket.getservbyport(port)
        except:
            service_name = 'Unknown service'
        return True, service_name
    elif result == 0:
        return True, None


    s.close()

    return False, None


def scan_ip_and_mac(target, mac):
    # Define the Arp request
    arp_request = ARP(pdst=target)

    # Give the range where to send it, ff:ff:ff:ff:ff:ff means everyone
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combine the variables                  
    arp_request_broadcast = broadcast/arp_request         

    # Send the Arp request
    #answer, no_answer = scapy.srp(arp_request_broadcast, timeout=5, iface="WAN Miniport (Network Monitor)")
    answer, no_answer = srp(arp_request_broadcast, timeout=30, iface="VMware Virtual Ethernet Adapter for VMnet8")
    #answer, no_answer = srp(arp_request_broadcast, timeout=10)

    print("answer: ", answer)
    print("no_answer: ", no_answer)

    ip_list=[]
    mac_list=[]

    for element in answer:
        if mac:
            ip_list.append(element[1].psrc)
            mac_list.append(element[1].hwsrc)
        else:
            ip_list.append(element[1].psrc)

    # return the list
    if mac:
        return ip_list, mac_list
    else:
        return ip_list


def printart():
  #T = input("Enter Text you want to convert to ASCII art : ")
  T = ("Patrick's Network Scanner")
  ASCII_art_1 = pyfiglet.figlet_format(T)
  print(ASCII_art_1)

  T = ("LN: 376303")
  ASCII_art_1 = pyfiglet.figlet_format(T)
  print(ASCII_art_1)

  T = ("p.r.ten.brinke@st.hanze.nl")
  ASCII_art_1 = pyfiglet.figlet_format(T)
  print(ASCII_art_1)    


main()