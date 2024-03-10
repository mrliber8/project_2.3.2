from Crypto.Cipher import AES
from base64 import b64decode
from base64 import b64encode

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

#print(ECB_decrypt(ciphertext, key))

def ECB_encrypt(plaintext, key):

    #Each 16-byte block of plaintext is encrypted independently.
    # ECb encrypt per block van 16
    #print(AES.block_size)
    padding_length = 16 - (len(plaintext) % 16)

    # PKCS#7-padding:
    # Padd de text met de [lengte] * de lengte
    # Voorbeeld padding_length is 4, stop dan de waarde 4 in een array
    # En doe dit keer vier, zodat je data\x04\x04\x04\x04 krijgt. Bij de
    # Decryptie kan ja dan heel gemakkelijk dit weer weghalen, door te kijken
    # Wat de laatste value is en dit X aantal keer weg te halen
    padded_plaintext = plaintext + bytes([padding_length] * padding_length)

    # Initialiseer de cipher in AES-ECb mode
    cipher = AES.new(key, AES.MODE_ECB)
    # Encrypt
    ciphertext = cipher.encrypt(padded_plaintext)

    return ciphertext


plaintext = b64decode('SGFzdCBkdSBldHdhcyBaZWl0IGZ1ciBtaWNoPw==')
key = b"SECRETSAREHIDDEN"

ciphertext = ECB_encrypt(plaintext, key)

assert ECB_encrypt(plaintext, key) == b64decode('86ueC+xlCMwpjrosuZ+pKCPWXgOeNJqL0VI3qB59SSY=')

#print(b64encode(ciphertext))

def ECB_decrypt_padding(ciphertext, key):
    # Zelfde als de vorige functie
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext)

    # Laatste element/byte is de padding
    padding_length = padded_plaintext[-1]
    # Slice de padding weg
    plaintext = padded_plaintext[:-padding_length]
    
    return plaintext



plaintext = b"Is this the Crusty Krab? No this is Patrick"
key = b"SECRETSAREHIDDEN"

# Encryptie van de plaintext
ciphertext = ECB_encrypt(plaintext, key)

# Decryptie van de ciphertext met padding verwijdering
decrypted_plaintext = ECB_decrypt_padding(ciphertext, key)

print(decrypted_plaintext, plaintext)


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