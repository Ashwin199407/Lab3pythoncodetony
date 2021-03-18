from TxInput import TxInput
from SampleWallet import generateSampleWallet
from Message import Message
import copy 
from TxInputUnsigned import TxInputUnsigned
class TxInputList:
    """List of TxInputs of a transaction """

    def __init__(self,txInputList=None):
        """Constructor, construct txInputList from a list of TxInput
           without arguments returns the empty txInputList"""
        self.txInputList = []
        if txInputList is not None:
            for txInput in txInputList:
                self.addEntry(txInput)

    def __repr__(self):
        """default toString method"""        
        result = ""
        for txInput in self.txInputList:
            result += str(txInput) + "\n"
        return result

    def __eq__ (self,other):
        return self.txInputList == other.txInputList

    def __copy__(self):
        return TxInputList(self.txInputList)

    def addEntry(self,txInput):
        """Add a txInput to the current list"""
        self.txInputList.append(copy.copy(txInput))

    def toList(self):
        """returns the underlying list of TxInput """
        return self.txInputList

    def toSum(self):
        """Computes the sum of Amounts in the list """
        result = 0
        for txInput in self.toList():
            result += txInput.getAmount()
        return result

    def toDictPublicKeyAmount(self):
        """ when checking that TxInputList can be deducted
            from an accountBalance
            it is not enough to check that each single item can be deducted
            since for the same sender several items might occur

            In order to check that the TxInputList can be deducted
            We first create an accountBalance containing for each user the
           sum of amounts to be deducted

           Then we can check whether each entry in the original accountBalance is
           greater the sum of items for each user to be deducted"""
        result = dict()
        for txInput in self.toList():
            if txInput.getSender() in result.keys():
                result[txInput.getSender()] += txInput.getAmount()
            else:
                result[txInput.getSender()]  = txInput.getAmount()
        return result


    #######################################################################
    #   Task 2
    #     Check the signatures of each element of the TxInputList is correct
    #     w.r.t. the TxOutputList given
    #     You can make use of the checkSignature method of individual txinputs 
    #     (elements of TxInput).
    #
    #     In order for the code to compile it has been defined as True
    #     but that should be adapted.
    #############################################################################
    
    def checkSignature(self,txOutputList):
        # this is not the correct value, only used here so that the code
        # compiles
        #signfalse = bool 
        #Input = TxInput()
        
        for txInput in self.toList():
            if (txInput.checkSignature(txOutputList)==0):
                return False
        return True
                
            
            

                               
    



    def str(self,publicKeyMap,word1="(Recipient: ", word2=", Amount:  ",
            word3=")"):
        """Print InputList in readable format in the form of a list of
           entries
           word1 <senderName> word2 <amount> word3
           where senderName is looked up from sender using
           publicKeyMap"""
        result = "["
        for txInput in self.toList():
            result += txInput.str(publicKeyMap,word1,word2,word3)
        result +="]"
        return result

    def testCase(self,header,pubKeyMap):
        print(header)
        print("keyNames=",pubKeyMap.getKeyNames())
        print("Sum of Amounts = ",self.toSum())
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
    TxInputList([TxInput(pubKeyA,10,signature1)]).testCase("Test Alice 10",pubKeyMap)
    TxInputList([TxInput(pubKeyB,20,signature2)]).testCase("Test Bob 20",pubKeyMap)
    l = TxInputList([TxInput(pubKeyA,10,signature1),TxInput(pubKeyA,10,signature2)])
    l.testCase("Alice twice 10",pubKeyMap)
    l = TxInputList([TxInput(pubKeyA,10,signature1),TxInput(pubKeyB,20,signature2)])
    l.testCase("Test Alice 10 and Bob  20",pubKeyMap)
    print("Same List but with words User and spends")   
    print(l.str(pubKeyMap,"(User "," spends ",")"))             


if __name__=="__main__":
    test()    
    
       

    
            
    

  

    

    
