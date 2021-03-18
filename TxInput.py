from SampleWallet import generateSampleWallet
from Message import Message
from TxInputUnsigned import TxInputUnsigned
from TxOutputList import TxOutputList
from TxOutput import TxOutput
import copy


class TxInput:
    """ Specifies one input of a transaction
        given by the sender given by a public key, the amount to be transferred 
        and a signature for the message to be signed """

    def __init__(self,sender,amount,signature):
        """Create TxInput from sender and amount"""
        self.txInputUnsigned = TxInputUnsigned(sender,amount)
        self.signature = signature

    def __repr__(self):
        """default toString method"""
        return "(sender = " + str(self.getSender()) + ", amount=" \
               + str(self.getAmount) + "signature=" \
               + str(self.getSignature()) + ")"

    def __copy__(self):
        return TxInput(copy.copy(self.getSender()),self.getAmount(),\
                       copy.copy(self.getSignature()))

    def __eq__(self,other):
        return self.getSender() == other.getSender() and \
               self.getAmount() == other.getAmount() and \
               self.getSignature() == other.getSignature()
                                
    def getSender(self):
        """ Get the Sender"""
        return self.txInputUnsigned.sender

    def getSenderName(self,publicKeyMap):
        """ look up the name of the sender in the publicKeyMap"""
        return publicKeyMap.getKeyName(self.txInputUnsigned.sender)    
        
        

    def getAmount(self):
        """get the Amount"""
        return self.txInputUnsigned.amount

    def getSignature(self):
        """get the Signature"""
        return self.signature

    def toTxInputUnsigned(self):
        """get the underlying TxInputUsigned"""
        return self.txInputUnsigned

    ###################################################################
    #    Task 1
    #    Check the signature is correct for a given TxOutputList.
    #       (The TxOutputList is needed to determine the message to be signed which
    #            consists of the sender, amount, and the public keys and amounts for
    #        each output.
    #        It is computed in the method getMessageToSign  of TxInputList.py
    #
    #   This can be done by getting the underlying TxInputUnsigned
    #    and executing the method checkSignature for it referring to the TxOutputList
    #    and the signature which is a field of TxInput
    #
    #    In order for the code to compile it has been defined in the questions as True
    #    but that should be replaced by the correct value.
    ##################################################################

    def checkSignature(self,txOutputList):
        # this is not the correct value, only used here so that the code
        # compiles
        txolus=self.toTxInputUnsigned()
        result=bool(txolus.checkSignature(txOutputList,self.signature))
        return result
    
    


    def str(self,publicKeyMap,word1="(Sender: ", word2=", Amount:  ",
            word3=")"):
        """Create a string in readable format in the form
           word1 <sendername> word2 <amount> word3
           where sendername is looked up from sender using
           publicKeyMap"""
        return (word1 + str(self.getSenderName(publicKeyMap)) +\
                word2 + str(self.getAmount()) + word3)


    def print(self,publicKeyMap,word1="(Sender: ",
                                word2=", Amount:  ",
                                word3=")"):
        """Print TxOutputUnsigned in readable format in the form
           word1 <sendername> word2 <amount> word3
           where sendername is looked up from sender using
           publicKeyMap"""
        print(self.str(publicKeyMap,word1,word2,word3))


def createTxInput(senderName,amount,txOutputList,wallet):
    """If we have a Wallet covering the sender
          and an txOutputList
       then we can compute the signature by signing the transaction to be signed consisting
        of the public key and input amount and the txOutput list
        using the private key of the sender
       createTxInput computes the resulting TxInput"""
    sender = wallet.getPublicKey(senderName)
    txInputUnsigned = TxInputUnsigned(sender,amount)
    messageToSign = txInputUnsigned.getMessageToSign(txOutputList)
    signature = wallet.signMessage(messageToSign,senderName)
    return TxInput(sender,amount,signature)
    
def test():
    
    """Test cases """
    wallet = generateSampleWallet(["Alice", "Bob", "Carol", "David"])
    pubKeyMap = wallet.toPublicKeyMap()
    sampleMessage1 = Message()
    sampleMessage1.addInteger(15)
    sampleMessage2 = Message()
    sampleMessage2.addInteger(20)
    sampleMessage3 = Message()
    sampleMessage3.addInteger(30)
    signature1 = wallet.signMessage(sampleMessage1,"Alice")
    print("signature1 =",signature1)
    pubKeyA =   pubKeyMap.getPublicKey("Alice");
    pubKeyB =   pubKeyMap.getPublicKey("Bob");          
    print("Test Alice 10");
    (TxInput(pubKeyA,10,signature1)).print(pubKeyMap)
    print()
    print("Test Bob 20");
    (TxInput(pubKeyB,20,signature1)).print(pubKeyMap)
    txOutputList = TxOutputList([TxOutput(pubKeyA,10),TxOutput(pubKeyA,10)])
    txInput = createTxInput("Alice",10,txOutputList,wallet)
    print("Check Signature",txInput.checkSignature(txOutputList,signature1))

if __name__== "__main__":
    test()        
    
