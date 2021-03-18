from Crypto.Signature import pss
from Crypto.PublicKey import RSA
from Message import Message
from PublicKey import PublicKey
import copy


class PrivateKey:
    "Class maintaining private keys"""

    def __init__(self,key):
        """ generates an element of PublicKey from a key
            as defined in Crypto.PublicKey"""
        self.privateKey= key

    def __copy__(self):
        return PrivateKey(self.privateKey)

    def __repr__(self):
        return str(self.privateKey.export_key())

    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return self.privateKey == other.privateKey


    def toPublicKey(self):
        return PublicKey(self.privateKey.publickey())


    def sign(self,message):
        """Signs a message using the current private key"""
        return pss.new(self.privateKey).sign(message.toSHA256Hash())



def generatePrivateKey():
    """Generates a random private key"""
    return PrivateKey(RSA.generate(2048))

def test():
    """Test cases """
    prk= generatePrivateKey()
    print("Private key generated = ",prk)
    msg = Message()
    msg.addInteger(13)
    msg.addPublicKey(RSA.generate(2048).publickey())
    print("Message = ",msg)
    keyForSigning = RSA.generate(2048)
    privateKeyForSigning= PrivateKey(keyForSigning)
    signature = privateKeyForSigning.sign(msg)
    print("Signature=",signature)

    
if __name__== "__main__":
    test()
