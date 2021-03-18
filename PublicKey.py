from Crypto.Signature import pss
from Crypto.PublicKey import RSA
import copy
from Message import Message


class PublicKey:
    "Class maintaining public keys"""

    def __init__(self,key):
        """ generates an element of PublicKey 
            from an element of Crypt.PublicKey"""
            
        self.publicKey= key.publickey()


    def __repr__(self):
        return str(self.publicKey.export_key())

    def __hash__(self):
        return hash(str(self))

    def __eq__(self,other):
        return self.publicKey == other.publicKey

    def __copy__(self):
        return PublicKey(self.publicKey)

    def publickey(self):
        """Returns the public Key as an element of Crypto.PublicKey"""
        return self.publicKey

    def checkSignature(self,message,signature):
        """Checks whether signature is a valid signature
           for message which is signed by the private key
           corresponding to the current public key
        """
        h = message.toSHA256Hash()
        verifier = pss.new(self.publicKey)
        try:
            verifier.verify(h,signature)
            return True
        except (ValueError, TypeError):
            return False


def test():
    from PrivateKey import PrivateKey
    """Test cases """
    from Crypto.PublicKey import RSA
    key= RSA.generate(2048)
    pbk = PublicKey(key)
    print("Public key generated = ",pbk)
    testdict = dict()
    testdict[pbk] = "Alice"
    print("testdic mapping pbk to Alice =",testdict)


    key= RSA.generate(2048)
    pbk = PublicKey(key.publickey())
    print("Public key generated = ",pbk)
    msg = Message()
    msg.addInteger(13)
    key= RSA.generate(2048)
    msg.addPublicKey(key.publickey())
    print("Message = ",msg)
    keyForSigning = RSA.generate(2048)
    privateKeyForSigning= PrivateKey(keyForSigning)
    publicKeyForSigning = PublicKey(keyForSigning.publickey())
    print("Public Key for Signing=",publicKeyForSigning)    
    publicKeyFromPrivateKeyForSigning = privateKeyForSigning.toPublicKey()
    print("Private Key from Public Key",publicKeyFromPrivateKeyForSigning)

    print ("Two keys are equal (should return True) = ",
           publicKeyForSigning == publicKeyFromPrivateKeyForSigning)
    signature = privateKeyForSigning.sign(msg)
    print("Signature (should return true) =",signature)
    print("Verify Signature=",
          publicKeyForSigning.checkSignature(msg,signature))
    
if __name__== "__main__":
    test()    
