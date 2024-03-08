# project_2.3.2

![GitHub repo size](https://img.shields.io/github/repo-size/mrliber8/project_2.3.2)
![GitHub License](https://img.shields.io/github/license/mrliber8/project_2.3.2)
![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Security](https://img.shields.io/badge/security-network%20scanning-blueviolet)

This project is part of a series of practical assignments focused on implementing and testing security measures within a Windows domain, carrying out offensive reconnaissance, writing tooling for the detection and exploitation of vulnerabilities, and assessing & selecting cryptographic protocols. The Network Scanner is the first tool in this series, designed to scan and analyze network environments using Python's socket and Scapy modules.

## Table of Contents
- [Assignment 2: Network Mapper](#assignment-2-network-scanner)
- [Assignment 3: Side Channel Attack](#assignment-3-side-channel-attack)
- [Assignment 4: Cryptography](#assignment-4-cryptography)
- [Assignment 5: Vulnerability Scan](#assignment-5-vulnerability-scan)

## Assignment 2: Network Scanner
For this assignment we had to make a network scanner in python, while using the nmap module as least as possible

### Features
- **Subnet Scan**: The ability to scan a full subnet, but also one specific host
- **Arp request**: Get the Ip and MAc address of a target using an arp request broadcast
- **Port and service Scanning**: Enumerate open ports on targeted hosts while retrieving the service behind it
- **Host and OS name**: Able to retrieve not only the hostname, but also the os name of the targeted host(s)

### To do
- **Progress**: Adding print statements to show progress reports. This will be my first time that print statements are a feature and not for testing

### Action
![Gif of the script in action](https://github.com/mrliber8/project_2.3.2/blob/main/py_network_scanner/test1.gif)

### Installation
1. Modules
For this scanner, the following non-standard modules where imported:
* colorama
* pyfiglet
* python-nmap
* scapy
* tabulate

If one of these modules is not already installed, pleas do so using:
```
pip install module_name
```
Or by using 
```
pip install -r requirements.txt
```

2. Run the scanner.py file
The main.py file is depricated and should not be used. You can run the scanner.py file from the command line with the following options:
```
usage: scanner.py [-h] [-m] [-s] [-n] [-f] target

A nice network scanner based on python's scapy and socket module

positional arguments:
  target             Input a network address or a subnet

options:
  -h, --help         show this help message and exit
  -m, --mac          Choose if you want the mac address
  -s, --service      Choose if you want an estimation of the sevrice behind a port
  -n, --hostname     Choose if you want an estimation of the hostname
  -f, --fingerprint  Choose if you want an estimation of the OS name
```


## Assignment 3: Side Channel Attack
In this assignment, we had to practice a side-channel attack. A "vulnerable" server was set up to check the password character by character. By timing the response, it is possible to determine whether a character is correct.

To achieve this, I developed 3 main functions:

1. `find_username`
   * This function sends a string of numbers to the server. If the response is 'Incorrect password. Access Denied.', we know the username exists; otherwise, it is not valid.
2. `find_password_length`
   * Since the server first checks the password length and, if it is correct, sleeps for a short time before checking the first character, the length that takes the longest to process is most likely the correct length.
3. `find_password`
   * Once the username and password length are known, we can attempt to guess the password. Starting at index 0, we fill the rest of the string with zeros. We then send a character 'x' number of times, repeating this for every possible character at that index. The character with the highest mean response time is most likely the correct one, so we fill the index with that character and then proceed to the next index.

To support the `find_password` function, I also created a helper function:
1. `increment_char`
    * This function takes a character, converts it into Unicode, increments it by one, then converts it back into a character and returns it.

## Assignment 4: Cryptography
In this assignment the goal was to learn about several encryption methods, to ultimately execute an Adaptive Chosen-plaintext attack.

* Base 64 encoding
* Binary XOR
* ECB-mode AES (Electronic Codebook)
* CBC-mode AES
* Adaptive Chosen-plaintext Attack (ACPA)

## Assignment 5: Vulnerability Scan
