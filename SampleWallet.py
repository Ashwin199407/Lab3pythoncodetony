from Wallet import Wallet
from PrivateKey import PrivateKey, generatePrivateKey

def generateSampleWallet(keyNames):
    """Generates a Wallet for a given list of keyNames in a random way"""
    wallet = Wallet()
    for keyName in keyNames:
        wallet.addKey(keyName,generatePrivateKey())
    return wallet


def test():
    """Test cases """
    names = ["Alice","Bob","Carol","David"]
    sampleWallet = generateSampleWallet(names)
    print("Wallet generated = \n")
    print(sampleWallet)
    
        
if __name__== "__main__":
    test()    
        
    
