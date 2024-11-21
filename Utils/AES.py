import base64
from Crypto.Cipher import AES
from Crypto import Random

def encrypt(key,source,encode=True,keyType = 'hex'):
    source = source.encode()
    if keyType == 'hex':
        key = bytes(bytearray.fromhex(key))
    
    IV = Random.new().read(AES.block_size)
    encryptor = AES.new(key,AES.MODE_CBC, IV)
    padding = AES.block_size - len(source)  % AES.block_size
    source += bytes([padding]) * padding
    data = IV + encryptor.encrypt(source)
    return base64.b64encode(data).decode() if encode else data 



def decrypt(key, source, decode=True, keyType='hex'):
    if decode:
        source = base64.b64decode(source) 
    
    if keyType == 'hex':
        key = bytes(bytearray.fromhex(key))  

    IV = source[:AES.block_size]
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid Padding... ..")
    
    return data[:-padding]


key = 'b1a2f7a9c8e5d1d4eb6f24f3b61e6d0fa378547348c7ac23d763b3b83e5f25a0'  # 32-byte key (hex format)
data = "Tushar."


# encrypted = encrypt(key, data)
# print("Encrypted:", encrypted)


# decrypted = decrypt(key, encrypted)
# print("Decrypted:", decrypted)
