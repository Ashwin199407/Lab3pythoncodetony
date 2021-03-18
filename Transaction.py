from TxInputList import TxInputList
from TxInput import TxInput
from TxOutputList import TxOutputList
from TxOutput import TxOutput
from Message import Message
from SampleWallet import generateSampleWallet

class Transaction:
    """Transaction consisting of a list of txInputs and a list of txOutputs"""

    def __init__(self,txInputList,txOutputList):
        """Constructor for a transction from a txInputList and 
           a txOuputList"""
        self.txInputList = txInputList
        self.txOutputList = txOutputList        

    def __repr__(self):
        """to String method"""        
        return "TxInputs:" + str(self.goTxInputList()) + \
            "\nTxOutputs:" + str(self.goTxOutputList())

    def __eq__ (self,other):
        return self.goTxInputList() == other.goTxInputList() and \
            self.goTxOutputList() == other.goTxOutputList()

    def __copy__(self):
        return Transaction(self.goTxInputList(),self.goTxOutputList())

    def toTxInputList(self):
        """Returns the underlying TxInputList"""
        return self.txInputList

    def toTxOutputList(self):
        """Returns the underlying TxOutputList"""        
        return self.txOutputList

    def checkTransactionAmountsValid (self):
        """Checks whether the sum of outputs is <= the sum of inputs"""
        return self.toTxInputList().toSum() >= self.toTxOutputList().toSum()

    ################################################################
    # Task 3
    #  check all signatures are valid 
    #
    #  In order for the code to compile it has been defined as True
    #  but that should be adapted
    ################################################################


    def checkSignaturesValid(self):
        # this is not the correct value, only used here so that the code
        # compiles
        Result= TxInput.checkSignature(TxOutput)
        return Result
              


    def str(self,publicKeyMap):
        """creates a String in readable format, looking up keyNames
           in publicKeyMap
        """
        result = "TxInputs: " + str(self.toTxInputList,publicKeyMap) + \
                 "\nTxOutputs: " + str(self.toTxOutputList,publicKeyMap)

    def testCase(self,header,publicKeyMap):
        """ Generic Test cases, providing a headline
            printing out the transaction
            and printing out whether it is valid
        """
        print(header)
        print(publicKeyMap)
        print("Is valid regarding sums = ",self.checkTransactionAmountsValid())
        print()
    

def test():
    """Test cases """
    wallet = generateSampleWallet(["Alice","Bob","Carol","David"])
    pubKeyMap = wallet.toPublicKeyMap()
    sampleMessage1 = Message()
    sampleMessage1.addInteger(15)
    sampleMessage2 = Message()
    sampleMessage2.addInteger(20)
    sampleMessage3 = Message()
    sampleMessage3.addInteger(30)
    signature1 = wallet.signMessage(sampleMessage1,"Alice")
    signature2 = wallet.signMessage(sampleMessage2,"Bob")
    signature3 = wallet.signMessage(sampleMessage3,"Carol")            
    pubKeyA = pubKeyMap.getPublicKey("Alice")
    pubKeyB = pubKeyMap.getPublicKey("Bob")
    pubKeyC = pubKeyMap.getPublicKey("Carol")    
    tx = Transaction(TxInputList(),TxOutputList())      
    tx.testCase("Transaction null to null",pubKeyMap)
    tx = Transaction(TxInputList([TxInput(pubKeyA,10,signature1)]),
                     TxOutputList([TxInput(pubKeyB,5,signature1)]))
    tx.testCase("Transaction Alice 10  to Bob 5",pubKeyMap)
    
    tx = Transaction(TxInputList([TxInput(pubKeyA,5,signature1)]),
                     TxOutputList([TxOutput(pubKeyB,10)]))
    tx.testCase("Transaction Alice 5  to Bob 10",pubKeyMap)
        
    tx = Transaction(TxInputList([TxInput(pubKeyA,10,signature1),
                                  TxInput(pubKeyB,5,signature1)]),
                     TxOutputList([TxOutput(pubKeyA,7),TxOutput(pubKeyC,8)]))
    tx.testCase("Transaction Alice 10  Bob 5 to Alice 7 Carol 8",pubKeyMap)

    tx = Transaction(TxInputList([TxInput(pubKeyA,10,signature1),
                                TxInput(pubKeyB,5,signature1)]),
                     TxOutputList([TxOutput(pubKeyA,10),
                                   TxOutput(pubKeyC,8)]))
    tx.testCase("Transaction Alice 10  Bob 5 to Alice 10 Carol 8",pubKeyMap)

  

if __name__=="__main__":
    test()    










