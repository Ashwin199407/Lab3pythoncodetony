from SampleWallet import generateSampleWallet
import copy

class TxOutput:
    """ TxOutput specifies a recipient (element of PublicKey)
        and the amount to be send.
        It will be used in a transaction as one arrow going out
        of one transaction """

    def __init__(self, recipient,amount):
        """Create new TxOutput from a public key for the recipient 
           and an amount"""
        self.amount = amount
        self.recipient = recipient

    def __repr__(self):
        """to String method"""
        return "(" + str(self.getRecipient()) + "," +\
            str(self.getAmount()) + ")"

    def __copy__(self):
        return TxOutput(copy.copy(self.recipient),self.amount)

    def __eq__(self,other):
        return self.getRecipient() == other.getRecipient() and \
                                self.getAmount() == other.getAmount()

    def getRecipient(self):
        """ get the recpient of the TxOutput"""
        return self.recipient

    def getRecipientName(self,publicKeyMap):
        """ look up the name of the recipient in the publicKeyMap"""
        return publicKeyMap.getKeyName(self.recipient)
        
        

    def getAmount(self):
        """get the Amount"""
        return self.amount

    def str(self,publicKeyMap,word1="(Recipient: ", word2=", Amount:  ",
            word3=")"):
        """Print Output in readable format in the form
           word1 <recipientName> word2 <amount> word3
           where recipientName is looked up from recipient using
           publicKeyMap"""
        return (word1 + str(self.getRecipientName(publicKeyMap)) +\
                word2 + str(self.getAmount()) + word3)

def test():
    """Test cases"""
    wallet = generateSampleWallet(["Alice","Bob","Bob","David"])
    print("Wallet =\n",wallet)
    pubKeyMap = wallet.toPublicKeyMap()
    pubKeyA = pubKeyMap.getPublicKey("Alice")
    AliceBack = pubKeyMap.getKeyName(pubKeyA)
    print("AliceBack=",AliceBack)
    pubKeyB = pubKeyMap.getPublicKey("Bob")
    txo = TxOutput(pubKeyA,10)
    print("TxOutput(Alice,10)=",txo.str(pubKeyMap))
    print("txo using __str__=",str(txo))
    txo = TxOutput(pubKeyB,20) 
    print("TxOutput(Bob,20)=",txo.str(pubKeyMap))
    

if __name__=="__main__":
    test()    
