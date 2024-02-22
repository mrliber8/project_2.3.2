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

import scapy
import socket
from datetime import datetime