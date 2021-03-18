from __future__ import print_function

from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import copy

class Message:

    """A class representing messages which are array of bytes
    """


    def __init__(self,theByteArray=None):
        """Define the message formed from byte array
           without arguments form the empty message"""
        if theByteArray is None:        
            self.message = bytearray()
        else:
            self.message = copy.deepcopy(theByteArray)
        
    def __copy__(self):
        return Message(self.message)

    def __eq__(self,other):
        return self.message == other.message

    def __repr__(self):
        """default toString method"""
        return str(self.message)
    

    def addByteArray(self,bytes):
        """Add an array of bytes to the message"""
        self.message = copy.deepcopy(bytes)

    def addInteger(self,number):
        """ Adds an integer to the current message"""
        self.addByteArray(number.to_bytes(2,'big'))

    def addPublicKey(self,pubkey):
        """adds a public key to the current message
           public key needs to be an element of Crypto.PublicKey """
        self.addByteArray(pubkey.export_key(format="DER"))

    def toSHA256Hash(self):
        h = SHA256.new(self.message)
        return h

def test():
    """Test cases """
    from Crypto.PublicKey import RSA
    msg = Message()
    msg.addInteger(13)
    key= RSA.generate(2048)
    msg.addPublicKey(key.publickey())
    print("Message = ",msg)
    msg2 = copy.copy(msg)
    msg2.addInteger(15)
    print("msg=",msg)
    print("msg2=",msg2)
    print("msg = msg2",msg == msg2)
    print("msg = msg",msg == msg)    
    


if __name__== "__main__":
    test()
    


    

                          
                        
                          
    
