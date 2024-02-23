"""

"""
import scapy.all as scapy
from scapy.all import srp, Ether, ARP, conf
import socket
from datetime import datetime
import sys
from tabulate import tabulate
from test import printart


# 2.a and b.
# Arp requests consists of IP and Mac address
def scan_ip_and_mac(target, mac):
    # Define the Arp request
    arp_request = ARP(pdst=target)

    # Give the range where to send it, ff:ff:ff:ff:ff:ff means everyone
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combine the variables                  
    arp_request_broadcast = broadcast/arp_request         

    # Send the Arp request
    answer, no_answer = scapy.srp(arp_request_broadcast, timeout = 1)
    print("answer: ", answer)
    print("no_answer: ", no_answer)
    ip_and_mac_list = []

    # Add the output to a list
    for element in answer:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        print(element[1].psrc)
        print(element[1].hwsrc)
        ip_and_mac_list.append(client_dict)
    
    client_dict = {"ip": "10.5.4.116", "mac": "hello"}
    ip_and_mac_list.append(client_dict)
    # return the list
    # print(ip_and_mac_list)
    return ip_and_mac_list

# 2.c and d, open ports and the services that belong to it
def port_and_service_scan(ip, port):
    # Make a new socket object
        # AF_INET is IPV4
        # SOCK_STREAM is TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect_ex() returns 0 if it can connect
    socket.setdefaulttimeout(1)
    result = s.connect_ex((ip, port))

    if result == 0:
        try:
            service = socket.getservbyport(port)
            print(service)
        except:
            service = 'Unknown service'
        return True, service

    s.close()

    return False, None
    

def main():
    # 1.	De gebruiker kan zowel een volledig subnet scannen, als één specifieke host.
    target = sys.argv[1]
    printart()
    start_time = datetime.now()

    ##### Flag Logic

    mac = False
    '''
    If flag:
        Mac = true    
    '''

    # 2. a and b
    ip_and_mac_list = scan_ip_and_mac(target, mac)

    #Loop through the list
    for item in ip_and_mac_list:
        ip = item['ip']
        open_ports = []
        services = []

        table = [['IP', 'MAC', 'Open ports', 'Services']]

        port_list = [21221, 31016, 5601, 10051]
        for port in port_list:
        #for port in range(1, 1025):
                status, service = port_and_service_scan(ip, port)
                if status:
                    open_ports.append(str(port))
                    services.append(service)
                    list = [item['ip'], item['mac'], port, service]
                    table.append(list)
                  
    end_time = datetime.now()
    total_time = end_time - start_time
    print("Network scanner completed in: ", total_time)
    
    if len(table)> 1:
        print(tabulate(table))
    else:
        print("Failure :(")


if __name__ == "__main__":
    main()