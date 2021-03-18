from Crypto.PublicKey import RSA
from PublicKeyMap import PublicKeyMap
from PublicKey import PublicKey
from PrivateKey import PrivateKey

class Wallet:
    """A Wallet is a map keyMap from keyNames (which are strings) to 
         private keys
       For efficency reasons, we maintain as well a publicKeyMap
       which is considered as derived,
       so when using __copy__, __deepcopy__, __eq__ only
       keyMap is used
    """

    def __init__(self,keyMap = None):
        """Constructs the wallet from a keyMap which is a 
           map from keyNames to keys as defined in """
        self.keyMap = dict()
        self.publicKeyMap = PublicKeyMap()
        if keyMap is not None:
            for keyName in keyMap.keys():
                self.addKey(self,keyName,keyMap[keyName])

    def __repr__(self):
        """default toString method"""
        result = ""
        for keyName in self.getKeyNames():
            result += "(key=" + keyName  + ", privateKey=" + \
                        str(self.getPrivateKey(keyName)) + ")\n"
        return result

    def __copy__(self):
        return Wallet(self.keyMap)


    def toPublicKeyMap(self):
        """ computes the underlying publicKeyMap
            note it recomputes it instead of taking the 
            derived self.publicKeyMap 
        """
        result =PublicKeyMap()
        for keyName in self.keyMap.keys():
            result.addKey(keyName,self.getPublicKey(keyName))
        return result

    def addKey(self,keyName,key):
        """Adds a key given by a keyName and element of PrivateKey"""
        self.keyMap[keyName]= key
        self.publicKeyMap.addKey(keyName,key.toPublicKey())

    def getKeyName(self,publicKey):
        """Returns the KeyName from an element of PublicKey"""
        return self.publicKeyMap.getKeyName(publicKey)

    def getPublicKey(self,keyName):
        """Returns the element of PublicKey for KeyName"""        
        return self.publicKeyMap.getPublicKey(keyName)
    

    def getPublicKeyString(self,keyName):
        """Returns the PublicKey as a String"""                
        return self.publicKeyMap.getPublicKeyString(keyName)

    def getPrivateKey(self,keyName):
        """returns the private Key for keyName"""
        return self.keyMap[keyName]

    def getKeyNames(self):
        """gest a list of keyNames"""
        return  self.keyMap.keys()

    def toSubWallet(self,keyNames):
        """ Creates a subwallet from a wallet, containing those
            keys for which the keynanme is in the list keyNames
        """ 
        result = Wallet()
        for keyName in self.keyNames:
            result.addKey(keyName,result.getKey(keyName))
        return result

    def signMessage(self,message,keyName):
        """Sign a message using the key with name keyName"""
        privateKey= self.getPrivateKey(keyName)
        return privateKey.sign(message)

def test():
    """Test cases """
    wallet = Wallet()
    keyAlice = PrivateKey(RSA.generate(2048))
    wallet.addKey("Alice",keyAlice)
    keyBob = PrivateKey(RSA.generate(2048))
    wallet.addKey("Bob",keyBob)    
    print(wallet)            

    AliceBack = wallet.getKeyName(wallet.getPublicKey("Alice"))
    print("AliceBack = ",AliceBack)

    BobBack = wallet.getKeyName(wallet.getPublicKey("Bob"))
    print("BobBack = ",BobBack)    


    print("Public Key for Alice = ",wallet.getPublicKeyString("Alice"))
    
    
if __name__== "__main__":
    test()    
    
