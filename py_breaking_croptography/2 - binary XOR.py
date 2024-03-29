from base64 import b64encode

def fixed_length_xor(text, key):
    """
    Performs a binary XOR of two equal-length strings. 
    
    Parameters
    ----------
    text : bytes
        bytes-object to be xor'd w/ key
    key : bytes
        bytes-object to be xor'd w/ text
        
    Returns
    -------
    bytes
        binary XOR of text & key
    """

    str = []
    for x in range(len(text)):
        str.append(text[x] ^key[x])

    xor_output = bytes(str)
    
    #xor_output = bytes([a ^ b for a, b in zip(text, key)])
    
    return xor_output

# Laat deze asserts onaangetast!
assert type(fixed_length_xor(b'foo',b'bar')) == bytes
assert b64encode(fixed_length_xor(b'foo',b'bar')) == b'BA4d'

def repeating_key_xor(text, key):
    """Takes two bytestrings and XORs them, returning a bytestring.
    Extends the key to match the text length.
    
    Parameters
    ----------
    text : bytes
        bytes-object to be xor'd w/ key
    key : bytes
        bytes-object to be xor'd w/ text
        
    Returns
    -------
    bytes
        binary XOR of text & key
    """
    counter = 0
    
    key = bytearray(key)
    while len(text) != len(key):
        key.append(key[counter])
        counter += 1    

    str = []
    for x in range(len(text)):
        str.append(text[x] ^key[x])

    xor_output = bytes(str)

    return xor_output

# Laat deze asserts onaangetast!

assert type(repeating_key_xor(b'all too many words',b'bar')) == bytes
assert b64encode(repeating_key_xor(b'all too many words',b'bar'))\
   == b'Aw0eQhUdDUEfAw8LQhYdEAUB'

