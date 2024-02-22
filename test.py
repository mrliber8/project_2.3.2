from tabulate import tabulate
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
    
    

#print(f"IP: {item['ip']}, MAC: {item['mac']}")