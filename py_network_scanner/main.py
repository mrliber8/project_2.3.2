"""
Eisen Netwerkscanner 
1.	De gebruiker kan zowel een volledig subnet scannen, als één specifieke host. 
2.	De scanner is in staat om de volgende informatie van hosts in het netwerk te identificeren: 
    a.	Het IP-adres 
    b.	Het MAC-adres 
    c.	Openstaande poorten 
    d.	Welke service bij een openstaande poort hoort 
    e.	De hostnaam 
    f.	Het besturingssysteem 
3.	De output van de scanner is overzichtelijk, makkelijk leesbaar, en netjes geformatteerd (gebruik hiervoor bijvoorbeeld f-strings)
"""
import scapy.all as scapy
from scapy.all import srp, Ether, ARP, conf
import socket
from datetime import datetime
import sys


# 2.a and b.
# Arp requests consists of IP and Mac address
def scan_ip_and_mac(target):
    # Make an Arp request
    #arp_request = ARP()
    #print(arp_request.summary())

    # Define the Arp request
    arp_request = ARP(pdst=target)

    # Give the range where to send it, ff:ff:ff:ff:ff:ff means everyone
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    # Combine the variables                  
    arp_request_broadcast = broadcast/arp_request         

    # Send the Arp request
    answer, no_answer = scapy.srp(arp_request_broadcast, timeout = 1)

    #print(answer.summary()) 

    #print(no_answer.summary())
    
    # print(answer)

    # Add the output to a list
    ip_and_mac_list = []

    # return the list
    return ip_and_mac_list

def main():
    # 1.	De gebruiker kan zowel een volledig subnet scannen, als één specifieke host.
    target = sys.argv[1]

    # 2. a and b
    scan_ip_and_mac(target)


    print("Succes!")

if __name__ == "__main__":
    main()