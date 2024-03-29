from tabulate import tabulate
import turtle
import socket
import pyfiglet
import nmap


def test():
  print("IP\t\t\tMAC Address\t\t\tOpen Ports\t\t\tServices")
  ip_and_mac_list  = []

  client_dict = {"ip": "10.5.4.116", "mac": "hello"}
  ip_and_mac_list.append(client_dict)


  open_ports = [5604, 10051]
  services = ["unknown service", "unknown service"]

  for item in ip_and_mac_list:
      #print(f"IP: {item['ip']}, MAC: {item['mac']}")
      ip = item['ip']
      mac = item['mac']
      #print(ip, "\t\t\t", mac, "\t\t\t{', '.join(open_ports)}\t\t\t{', '.join(services)}")
      table = []


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


def host():
  name = "8.8.8.8"
  #Reverse dns lookup, gives this output: (hostname, alias-list, IP)
  a = socket.gethostbyaddr(name)
  print(a)

  b = socket.getfqdn(name)
  print(b)


def os_fingerprint():
  path = [r"C:\Program Files (x86)\Nmap\nmap.exe",] 

  nm = nmap.PortScanner(nmap_search_path=path)

  os_scan = nm.scan('localhost', arguments='-O')

  #print("Os information1: ", os_scan['scan']['127.0.0.1']['osmatch'][0])
  print("Os version: ", os_scan['scan']['127.0.0.1']['osmatch'][0]['name'])



os_fingerprint()
#host()
#printart()
