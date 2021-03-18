import Message 
import PublicKey
import PrivateKey 
import PublicKeyMap
import Wallet
import SampleWallet
import TxOutput
import TxOutputList
import TxInputUnsigned
import TxInput
import TxInputList
import AccountBalance

def test():
    """Test cases """
    print("Testing Message")
    Message.test()
    print("Testing PublicKey")
    PublicKey.test()
    print("Testing PrivateKey")        
    PrivateKey.test()
    print("Testing PublicKeyMap")
    PublicKeyMap.test()
    print("Testing Wallet")        
    Wallet.test()
    print("Testing SampleWallet")        
    SampleWallet.test()
    print("Testing TxOutput")
    TxOutput.test()
    print("Testing TxOutputList")
    TxOutputList.test()
    print("Testing TxInputUnsigned")
    TxInputUnsigned.test()
    print("Testing TxInput")
    TxInput.test()
    print("Testing TxInputList")
    TxInputList.test()    
    print("Testing AccountBalance")
    AccountBalance.test()    
    

if __name__== "__main__":
    test()
    


