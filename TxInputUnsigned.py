from SampleWallet import generateSampleWallet
from Message import Message
import copy

class TxInputUnsigned:
    """ Specifies one input of a transaction without the signature
        Given by a public key and the amount to be transferred 
    """

    def __init__(self,sender,amount):
        """Create TxInputUnsigned from sender and amount"""
        self.sender = sender
        self.amount = amount

    def __repr__(self):
        """default toString method"""
        return "(sender = " + str(self.sender) + ", amount=" \
               + str(self.amount) + ")"

    def __copy__(self):
        return TxInputUnsigned(copy.copy(self.getSender()),self.getAmount())

    def __eq__(self,other):
        return self.getSender() == other.getSender() and \
                                self.getAmount() == other.getAmount()

    def getSender(self):
        """ Get the Sender"""
        return self.sender

    def getSenderName(self,publicKeyMap):
        """ look up the name of the sender in the publicKeyMap"""
        return publicKeyMap.getKeyName(self.sender)    
        
        

    def getAmount(self):
        """get the Amount"""
        return self.amount

    def str(self,publicKeyMap,word1="(Sender: ", word2=", Amount:  ",
            word3=")"):
        """Create a string in readable format in the form
           word1 <sendername> word2 <amount> word3
           where sendername is looked up from sender using
           publicKeyMap"""
        return (word1 + str(self.getSenderName(publicKeyMap)) +\
                word2 + str(self.getAmount()) + word3)


    def print(self,publicKeyMap,word1="(Sender: ", word2=", Amount:  ",
            word3=")"):
        """Print TxOutputUnsigned in readable format in the form
           word1 <sendername> word2 <amount> word3
           where sendername is looked up from sender using
           publicKeyMap"""
        print(self.str(publicKeyMap,word1,word2,word3))


    
    def getMessageToSign(self,txOutputList):
        """Create the message to be signed, when the input is the current 
           TxInputUnsigned for a given outputlist

           In Bitcoin the sender signs his input and all outputs
           so other inputs of the transaction are not included in the 
           message to sign
        """
        
        message = Message()
        message.addPublicKey(self.getSender().publickey());
        message.addInteger(self.getAmount());
        for txOutput in txOutputList.toList():
            message.addPublicKey(txOutput.getRecipient().publickey())
            message.addInteger(txOutput.getAmount())
        return message
    
    def checkSignature(self,txOutputList,signature):
        """ Check that a signature is correct for input given 
            by the current sender and amount
            and a given txOutputList """
        message = self.getMessageToSign(txOutputList)
        return self.getSender().checkSignature(message,signature)


def test():
    """Test cases """
    wallet = generateSampleWallet(["Alice", "Bob", "Carol", "David"])
    pubKeyMap = wallet.toPublicKeyMap()
    pubKeyA   = pubKeyMap.getPublicKey("Alice")
    pubKeyB =   pubKeyMap.getPublicKey("Bob")                   
    print()
    print("Test (Alice in 10)")
    (TxInputUnsigned(pubKeyA,10)).print(pubKeyMap)
    print()
    print("Test (Bob in 20)");
    (TxInputUnsigned(pubKeyB,20)).print(pubKeyMap);     
    


if __name__== "__main__":
    test()        
