from TxOutput import TxOutput
from SampleWallet import generateSampleWallet
import copy 

class TxOutputList:
    """List of TxOutputs of a transaction """

    def __init__(self,txOutputList = None):
        """Constructor, construts txOutputList from a list of TxOutput
           without arguments returns the empty txOutputList"""
        self.txOutputList = []
        if txOutputList is not None:
            for txOutput in txOutputList:
                self.addEntry(txOutput)

    def __repr__(self):
        """to String method"""        
        result = ""
        for txOutput in self.txOutputList:
            result += str(txOutput) + "\n"
        return result

    def __eq__ (self,other):
        return self.txOutputList == other.txOutputList

    def __copy__(self):
        return TxOutputList(self.txOutputList)

    def addEntry(self,txOutput):
        """Add a txOutput to the current list"""
        self.txOutputList.append(copy.copy(txOutput))

    def toList(self):
        """returns the underlying list of TxOutput """
        return self.txOutputList

    def toSum(self):
        """Computes the sum of Amounts in the list """
        result = 0
        for txOutput in self.toList():
            result += txOutput.getAmount()
        return result

    def str(self,publicKeyMap,word1="(Recipient: ", word2=", Amount:  ",
            word3=")"):
        """Print OutputList in readable format in the form of a list of
           entries
           word1 <recipientName> word2 <amount> word3
           where recipientName is looked up from recipient using
           publicKeyMap"""
        result = "["
        for txOutput in self.toList():
            result += txOutput.str(publicKeyMap,word1,word2,word3)
        result +="]"
        return result

    def testCase(self,header,pubKeyMap):
        print(header)
        print(pubKeyMap)
        print("Sum of Amounts = ",self.toSum())
        print()

def test():
    """Test cases """
    wallet = generateSampleWallet(["Alice","Bob","Bob","David"])
    pubKeyMap = wallet.toPublicKeyMap()
    pubKeyA = pubKeyMap.getPublicKey("Alice")
    pubKeyB = pubKeyMap.getPublicKey("Bob")    
    (TxOutputList([TxOutput(pubKeyA,10)]).testCase("Test Alice 10",pubKeyMap))
    (TxOutputList([TxOutput(pubKeyB,20)]).testCase("Test Bob 20",pubKeyMap))
    (TxOutputList([TxOutput(pubKeyA,10),TxOutput(pubKeyA,10)]).testCase("Alice twice 10",pubKeyMap))
    l = TxOutputList([TxOutput(pubKeyA,10),TxOutput(pubKeyB,20)])
    l.testCase("Test Alice 10 and Bob  20",pubKeyMap)
    print("Same List but with words User and spends")	
    print(l.str(pubKeyMap,"(User "," spends ",")"))		


if __name__=="__main__":
    test()    
    
       

    
            
    

  

    

    
