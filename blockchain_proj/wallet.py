import rsa
import hashlib
from base64 import b64encode, b64decode

pubkey, privkey = rsa.newkeys(512)
mesg="hola".encode('utf-8')
print(mesg)
#hashy = hashlib.sha512(mesg).hexdigest().encode('utf-8')
#print(hashy)
sign = b64encode(rsa.sign(mesg, privkey,"SHA-256"))

#dsign = rsa.decrypt(sign, privkey)
print(rsa.verify(mesg,b64decode(sign),pubkey))
