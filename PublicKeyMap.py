from PublicKey import PublicKey
import copy

class PublicKeyMap:

    """ defines a map keyName2PublicKey from keyNames (strings) to public keys 
        For efficiency reason we maintain as well the inverse,
        publicKey2KeyName 
        When only using operations in  this class consistency 
        will be maintained 

        Note that publicKey2KeyName is considered as derived,
        when using copy, deepcopy, or comparison, only keyName2PublicKey is used
    """
    
    def __init__(self,keyName2PublicKey = None):
        """Constructs the public key map, 
           initialised with all keyName to public key items
               in keyName2PublicKey.
           With no argument, constructs the empty public key map"""
        self.keyName2PublicKey = dict()
        self.publicKey2KeyName = dict()
        if keyName2PublicKey is not None:
            for keyName in keyName2PublicKey.keys():
                self.addKey(keyName,keyName2PublicKey[keyName])


    def __repr__(self):
        """default toString method"""
        result = ""
        for keyName in self.getKeyNames():
            result += "(keyName=" + keyName + ", PublicKey=" +\
                                  str(self.getPublicKey(keyName)) + ")\n"
        return result





    def __eq__(self,other):
        return self.keyName2PublicKey == other.keyName2PublicKey 

    def __copy__(self):
        return PublicKeyMap(self.keyName2PublicKey)
             

    def addKey(self, keyName, publicKey):
        """Add a key to PublicKeymap"""
        self.keyName2PublicKey[keyName] = publicKey
        self.publicKey2KeyName[publicKey] = keyName

    def getKeyName(self,publicKey):
        """Lookup the keyName for a public key in PublicKeyMap"""
        return self.publicKey2KeyName[publicKey]

    def getPublicKey(self,keyName):
        """Lookup the Public Key for a keyName in PublicKeyMap"""        
        return self.keyName2PublicKey[keyName]


    def getPublicKeyString(self,keyName):
        """Lookup the Public Key as a string for a keyName in PublicKeyMap"""        
        return str(self.keyName2PublicKey[keyName])

    def getKeyNames(self):
        """Get a list of keyNames"""
        return self.keyName2PublicKey.keys()

    def addPublicKeyMap(self,publicKeyMap):
        """Add a public key map -- allows to combine several
           public key maps into one"""
        for keyName in publicKeyMap.getKeyNames():
            self.addKey(keyName,publicKeyMap.getPublicKey(keyName))

    


def test():
    """Test cases """
    from Crypto.PublicKey import RSA

    keyAlice= PublicKey(RSA.generate(2048).publickey())
    keyBob= PublicKey(RSA.generate(2048).publickey())
    
    pbkm = PublicKeyMap()
    pbkm.addKey("Alice",keyAlice)
    pbkm.addKey("Bob",keyBob)
    print("After adding keys for Alice and Bob")
    print(pbkm)
    print("public key for Alice = ",pbkm.getPublicKey("Alice"))
    print("keyname for keyAlice = ",pbkm.getKeyName(keyAlice))
    print("Keynames = ",pbkm.getKeyNames())
    print("PublicKeyMap=\n",pbkm)
          
    
if __name__== "__main__":
    test()

       


    
    
