#Wat is het verschil tussen b’hello world` en “hello world”? 
# b'hello world' is een byte string van hello world. Aangezien 
# encryptie werkt met binaire data kan je het met b omzetten.
# Als je dit alleen omzet kom je alsnog uit op hello world, doordat dit
# ASCII karakters zijn die direct overeenkomen met UTF-8 codering 

import base64


def string_to_b64(asciiString):
    """
    Converts a given ASCII-string to its b64-encoded equivalent.

    Parameters
    ----------
    asciiString : string
        string to be converted

    Returns
    -------
    bytes
        b64-encoded bytes-object representing the original string
    """
    byte_string = asciiString.encode('utf-8')
    
    # Encode the bytes to base64
    b64String = base64.b64encode(byte_string)

    return b64String

# Laat deze asserts onaangetast!
assert type(string_to_b64("foo")) == bytes
assert string_to_b64("Hello World") == b'SGVsbG8gV29ybGQ='

def b64_to_string(b64String):
    """
    Converts a given b64-string to its ASCII equivalent.

    Parameters
    ----------
    b64String : bytes
        b64-encoded bytesobject to be converted

    Returns
    -------
    string
        ASCII string
    """

    # Decode the base64 string to bytes
    byte_string = base64.b64decode(b64String)
    
    # Convert the bytes to an ASCII string
    asciiString = byte_string.decode('utf-8')


    return asciiString

# Laat deze asserts onaangetast!
assert type(b64_to_string("SGVsbG8gV29ybGQ=")) == str
assert b64_to_string("SGVsbG8gV29ybGQ=") == "Hello World"

def base64encoding(string):

    base64_alphabet_string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    #Base64 uses 6-bit characters grouped into 24-bit sequences.

    #Stap 1: Zet alles om naar 6 bit
    # 1.1 Zet om naar unicode
    ascii_representation =""
    list = []
    for c in string:
        list.append(ord(c))

    print("ascii", list)

    # 1.2 Zet om naar 8 bit
    list1 = []
    for ordc in list:
        #list1.append("{0:b}".format(ordc))
        list1.append(format(ordc, '08b'))

    print("ascii_to_8bit", list1)

    list_string = ''.join(list1)

    print("ascii 8bit string",list_string)

    # 1.3 Zet om naar 6 bit
    counter = 0
    counter2 = 1
    bit_list = []
    string = ""
    for character in list_string:
        string += character
        if counter2 == len(list_string):
            while len(string) < 6:
                string += '0'
            bit_list.append(string)
        elif counter < 5:
            counter += 1
            counter2 += 1
        else:
            counter =0
            bit_list.append(string)
            string = ""
            counter2 += 1

    # 1.4 Zet om naar 24-bit sequences
    while len(bit_list) % 4 != 0:
         bit_list.append('000000')

    print("24 bits list: ",bit_list)
    
    # 1.5 Convert binary to decimal
    decimal_list = []
    for binary in bit_list:
        decimal_list.append(int(binary, 2))

    print("Bits to decimal: ",decimal_list)

    # 1.6 Convert the decimal to the base64 alphabet
    base64_list = []
    for x in decimal_list:
        base64_list.append(base64_alphabet_string[x])

    print("base64 output: ", base64_list)
    return True


base64encoding("Hi")


def base64encoding(string):
    
    return True