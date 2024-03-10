from Crypto.Cipher import AES
from base64 import b64decode

def ECB_decrypt(ciphertext, key):
    """Accepts a ciphertext in byte-form,
    as well as 16-byte key, and returns 
    the corresponding plaintext.

    Parameters
    ----------
    ciphertext : bytes
        ciphertext to be decrypted
    key : bytes
        key to be used in decryption

    Returns
    -------
    bytes
        decrypted plaintext
    """

    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


# Laat deze asserts onaangetast & onderaan je code!
ciphertext = b64decode('86ueC+xlCMwpjrosuZ+pKCPWXgOeNJqL0VI3qB59SSY=')
key = b'SECRETSAREHIDDEN'
assert ECB_decrypt(ciphertext, key)[:28] == \
    b64decode('SGFzdCBkdSBldHdhcyBaZWl0IGZ1ciBtaWNoPw==')


with open("py_breaking_croptography/file3.txt", "r") as f:
    file = f.read()

ciphertext = b64decode(file)

print(ECB_decrypt(ciphertext, key))

def ECB_encrypt(plaintext, key):


    return ciphertext




'''
https://www.techtarget.com/whatis/definition/ASCII-American-Standard-Code-for-Information-Interchange#:~:text=The%20standard%20ASCII%20character%20set%20is%20only%207%20bits%2C%20and,bit%20is%20set%20to%201.
Een ASCII character is 7 bits, maar wordt weergeven als 8 bits waarbij 
de voorste bit op 0 wordt gezet. Bij de extended ASCII lijst wordt de 
voorste bit juist op 1 gezet. Zo is het euro teken bijvoorbeeld binary
1000 0000.

#Secretsarehidden is:
print(len(key)) # 16 lang

bit_lengte = len(key) * 8 
print(bit_lengte) # 128

Er wordt dus gebruik gemaakt van AES-128
'''