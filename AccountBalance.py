from SampleWallet import generateSampleWallet
from Message import Message
from TxInputList import TxInputList
from TxInput import TxInput, createTxInput
from TxOutputList import TxOutputList
from TxOutput import TxOutput
from Transaction import Transaction
from TxInputUnsigned import TxInputUnsigned
from PublicKeyMap import PublicKeyMap
from Wallet import Wallet
from PublicKey import PublicKey



class AccountBalance:
    """ AccountBalance defines an accountBalance 
        in the ledger model of bitcoins"""

    def __init__(self,accountBalanceBase = None):
        """Constructor, construct AccountBalance from accountBalanceBase
           which is a dictionary from publicKeys to the amount they have
           without arguments returns the empty AccountBalance"""
        self.publicKeyList = []
        self.accountBalanceBase = dict()
        if accountBalanceBase is not None:
            for keyName in accountBalanceBase.keys():
                self.addAccount(keyName,accountBalanceBase[keyName])

    def __repr__(self):
        """default toString method"""
        result = ""
        for publicKey in self.getPublicKeys():
            result = "(PublicKey = ",publicKey,\
                      " Amount = ",self.getBalance(publicKey)
        return result

    def __eq__ (self,other):
        return self.getAccountBalance() == other.getAccountBalance()

    def __copy__(self):
        return AccountBalance(self.getAccoutBalance())


    def addAccount(self,publicKey,balance):
        """Adds account given by publicKey with balance to the Balance
        """
        self.accountBalanceBase[publicKey] = balance
        if  publicKey not in self.publicKeyList:
            self.publicKeyList.append(publicKey)

    def hasPublicKey(self,publicKey):
        """Check whether there is an account with publicKey"""
        return (publicKey in self.getPublicKeys())

    def getPublicKeys(self):
        """get the list of Public Keys having accounts in AccountBalance
        """
        return self.getAccountBalanceBase().keys()


    def getAccountBalanceBase(self):
        """Return the underlying dictionary mapping
           publicKeys to balance"""
        return self.accountBalanceBase

    def hasAccount(self,publicKey):
        """Check whether there is an account for publicKey"""
        return publicKey in self.accountBalanceBase

    def getBalance(self,publicKey):
        """Get the balance in AccountBalance for publicKey
           if there is no account, return 0
        """
        if self.hasAccount(publicKey):
            return self.getAccountBalanceBase()[publicKey]
        else:
            return 0

    


    def setBalance(self,publicKey,balance):
        """Set the balance for publicKey to balance
           If account doesn't exist it is created with balance 
        """
        self.accountBalanceBase[publicKey] = balance
        if  publicKey not in self.publicKeyList:
            self.publicKeyList.append(publicKey)
    

    def addToBalance(self,publicKey, amount):
        """ Adds amount to balance for publicKey
           If account doesn't exist it is created with amount
        """ 
        self.setBalance(publicKey,self.getBalance(publicKey) + amount)

            
    def subtractFromBalance(self,publicKey, amount):
        """ Subtracts amount from balance for publicKey
            If account doesn't exist it is created with -amount
        """ 
        self.setBalance(publicKey,self.getBalance(publicKey) - amount)

    def checkBalance(self,publicKey,amount):
        """Checks whether the balance for publicKey is >= the amount.
           If account doesn't exist a balance of 0 is assumed 
        """
        return (self.getBalance(publicKey) >= amount)

    def checkDictPublicKeyAmountCanBeDeducted(self,dictPublicKeyAmount):
        """Check whether a map (a dictionary) from public keys to
           amounts can be deducted from AccountBalance
           This is an auxiliary function to define 
           checkTxInputListCanBeDeducted
        """
        for publicKey in dictPublicKeyAmount.keys():
            if not self.checkBalance(publicKey,dictPublicKeyAmount[publicKey]):
                return False

        return True

    def checkTxInputListCanBeDeducted(self,txInputList):
        """ Check that a list of publicKey amounts can be deducted from the 
             current accountBalance
            done by first converting the list of publicKey amounts into an 
              accountBalance
            and then checking that the resulting accountBalance can be deducted.
        """
        
        return self.checkDictPublicKeyAmountCanBeDeducted(txInputList.toDictPublicKeyAmount())

    def subtractTxInputList(self,txInputList):
        """ Subtract a list of TxInput from the accountBalance
            requires that the list to be deducted is deductable."""
        for txInput in txInputList.toList():
            self.subtractFromBalance(txInput.getSender(),txInput.getAmount())

    def addTxOutputList(self,txOutputList):
        """ Add a list of TxOutput to the accountBalance """
        for txOutput in txOutputList.toList():
            self.addToBalance(txOutput.getRecipient(),txOutput.getAmount())

    #################################################################
    #  Task 4 Check a transaction is valid.
    #
    #  this means that 
    #    the sum of outputs is less than or equal the sum of inputs
    #    all signatures are valid
    #    and the inputs can be deducted from the accountBalance.
    #
    #    This method has been set to true so that the code compiles - that should
    #    be changed
    ################################################################        

    def checkTransactionValid(self,Transaction,Tx):
        # this is not the correct value, only used here so that the code
        # compiles
        
        return Tx.checkSignatureValid() and Tx.checkTransactionAmountValid() and AccountBalance.checkTxInputListCanBeDeducted(TxInputList())
              

    def processTransaction(self,transaction):
        """ Process a transaction
            by first deducting all the inputs
            and then adding all the outputs.
        """
        self.subtractTxInputList(transaction.toTxInputList())
        self.addTxOutputList(transaction.toTxOutputList())

    def str(self,pubKeyMap):
        """String which shows the current state of the accountBalance
           using pubKeyMap for looking up keyNames for the publicKeys
        """
        result = ""
        for publicKey in self.getPublicKeys():
            balance = self.getBalance(publicKey)
            result += ("The balance for " +
                       pubKeyMap.getKeyName(publicKey) +
                       " is " +
                       str(self.getBalance(publicKey)) +
                       "\n")
        return result

    def print(self,pubKeyMap):
        """print the current state of the accountBalance
        """
        print(self.str(pubKeyMap))
    

def test():
    """Test cases """
    exampleWallet = generateSampleWallet(["Alice"])
    pubKeyMap = exampleWallet.toPublicKeyMap()
    exampleMessage = Message()
    exampleMessage.addInteger(15)
    exampleSignature = exampleWallet.signMessage(exampleMessage,"Alice")

    ##################################################################
    #  Task 5
    #   add  to the test case the test as described in the lab sheet
    #
    #   You can use the above exampleSignature, when a sample
    #      signature is needed, which cannot be computed from the data.
    #
    ##################################################################
    print(" 5.1 Create a sample wallet for Alice containing keys with names A1, A2, for Bob containing keynames B1, B2, for Carol containing keynames C1, C2, C3, and for David containing keyname D1 by using the method generate of SampleWallet")
    Alicewallet = Wallet()
    Bobwallet  =   Wallet()
    Carolwallet = Wallet()
    Davidwallet = Wallet()
    
    Alicewallet =generateSampleWallet(["A1","A2"])
    Bobwallet = generateSampleWallet(["B1","B2"])
    Carolwallet = generateSampleWallet(["C1","C2","C3"])
    Davidwallet = generateSampleWallet(["D1"])

    print("5.2 Compute the PublicKeyMap containing the public keys of all these wallets. The PublicKeyMap is for convenience, since comparing public keys is cumbersome.")
    
    
    pubKeyMapa=Alicewallet.toPublicKeyMap()
    pubKeyMapb=Bobwallet.toPublicKeyMap()
    pubKeyMapc=Carolwallet.toPublicKeyMap()
    pubKeyMapd=Davidwallet.toPublicKeyMap()

    pubKeyMapabcd = PublicKeyMap()
    pubKeyMapabcd.addPublicKeyMap(pubKeyMapa)
    pubKeyMapabcd.addPublicKeyMap(pubKeyMapb)
    pubKeyMapabcd.addPublicKeyMap(pubKeyMapc)
    pubKeyMapabcd.addPublicKeyMap(pubKeyMapd)


    pubKeyA1 = pubKeyMapabcd.getPublicKey("A1")
    pubKeyA2 = pubKeyMapabcd.getPublicKey("A2")
    pubKeyB1 = pubKeyMapabcd.getPublicKey("B1")
    pubKeyB2 = pubKeyMapabcd.getPublicKey("B2")
    pubKeyC1 = pubKeyMapabcd.getPublicKey("C1")
    pubKeyC2 = pubKeyMapabcd.getPublicKey("C2")
    pubKeyC3 = pubKeyMapabcd.getPublicKey("C3")
    pubKeyD1 =pubKeyMapabcd.getPublicKey("D1")
    print("– Create an empty AccountBalance and add to it the keynames of the wallets created before initialised with the amount 0 for each key")
    AccBal = AccountBalance()

    AccBal.addAccount(pubKeyA1,0)
    AccBal.addAccount(pubKeyA2,0)
    AccBal.addAccount(pubKeyB1,0)
    AccBal.addAccount(pubKeyB2,0)
    AccBal.addAccount(pubKeyC1,0)
    AccBal.addAccount(pubKeyC2,0)
    AccBal.addAccount(pubKeyC3,0)
    AccBal.addAccount(pubKeyD1,0)
    AccBal.print(pubKeyMapabcd)

    print("5.4Set the balance for A1 to 20")
    AccBal.setBalance(pubKeyA1,20)
    AccBal.print(pubKeyMapabcd)

    print("5.5 Add 15 to the balance for B1")
    AccBal.addToBalance(pubKeyB1,5)
    AccBal.print(pubKeyMapabcd)


    print("5.6 – Subtract 5 from the balance for B1")
    AccBal.subtractFromBalance(pubKeyB1,5)
    AccBal.print(pubKeyMapabcd)

    print("5.7 Set the balance for C1 to 10.")
    AccBal.setBalance(pubKeyC1, 10)
    AccBal.print(pubKeyMapabcd)

    print("5.8 Check whether the TxInputList txil1 giving A1 15 units, and B1 5 units (withsample signatures used) can be deducted.")
    txiL1=TxInputList()
    tx1 =(AccBal.checkTxInputListCanBeDeducted(txiL1))
    txiL1=TxInputList([TxInput(pubKeyA1,10,exampleSignature),TxInput(pubKeyB1,5,exampleSignature)])
    print("can txil1 be deducted?? : ",AccBal.checkTxInputListCanBeDeducted(txiL1))


    print("5.9 – Check whether the TxInputList txil2 giving A1 15 units, and giving A1 again15 units can be deducted.")
    txiL2=TxInputList()
    txiL2=TxInputList([TxInput(pubKeyA1,15,exampleSignature),TxInput(pubKeyA1,15,exampleSignature)])
    tx1 = (AccBal.checkTxInputListCanBeDeducted(txiL2))
    print("can txil1 be deducted?? : ", AccBal.checkTxInputListCanBeDeducted(txiL2))



    print("6.0 Deduct txil1 from the AccountBalance")
    AccBal.subtractTxInputList(txiL1)
    AccBal.print(pubKeyMapabcd)

    print("6.1Create a TxOutputList corresponding to txil2 which gives A1 twice 15 Units,and add it to the AccountBalance.")
    txoL2=TxOutputList()
    txoL2=TxOutputList([TxOutput(pubKeyA1,15),TxOutput(pubKeyA1,15)])
    AccBal.addTxOutputList(txoL2)
    AccBal.print(pubKeyMapabcd)


    print("6.2 Create a correctly signed input, where A1 is spending 30, referring to an outputlist giving B2 10 and C1 20 The output list is needed in order to create the message to be signed(consisting of A1 spending 30, B1 receiving 10 and C1receiving 20). Check whether the signature is valid for this signed input.")
    txoL3=TxOutputList()
    txoL3=TxOutputList([TxOutput(pubKeyB2,10),TxOutput(pubKeyC1,20)])
    TIU = TxInputUnsigned(pubKeyA1,30)
    message = TIU.getMessageToSign(txoL2)
    A1Signature = Alicewallet.signMessage(message,"A1") 
    txiL3=TxInputList()
    txiL3=TxInputList([createTxInput("A1",30,txoL3,Alicewallet)])	 
    valid =txiL3.checkSignature(txoL3)
    print("Is the signature valid for signed input?  : " ,valid);	


    print("6.3Create a wrongly signed input, which gives A1 30, and uses instead of the correctly created signature an example signature (example signatures are provided in thecode). Check whether the signature is valid for this signed input.")
    txisL4 =TxInputList()
    txisL4=TxInputList([TxInput(pubKeyA1,30,exampleSignature)])
    valid_check = txisL4.checkSignature(txoL3)
    print("Is the signature valid for signed input?  : "+str(valid_check))

    print("6.4 Create a transaction tx1 which takes as input for A1 35 units and gives B2 10, C2 10, and returns the change (whatever is left) to A2.")
    TxOuLi=TxOutputList([TxOutput(pubKeyB2,10),TxOutput(pubKeyC2,10),TxOutput(pubKeyA2,15)])
    Tiu1=TxInputList([createTxInput("A1",35,TxOuLi,Alicewallet)])
    #A1message = Tiu1.getMessageToSign(TxOuLi)
    #signA1 = Alicewallet.signMessage(A1message,"A1" )
    #txiL5 = TxInputList(pubKeyA1,35,signA1)
    tx1 =Transaction(Tiu1,TxOuLi)
    

    #AccBal.print(pubKeyMapabcd)



    print("6.5 Check whether the signature is approved for the transaction input, and whether the transaction is valid. Then update the AccountBalance using that transaction.")
     
    if  Tiu1.checkSignature(TxOuLi):
        print("signature is approved transaction input and the transaction is valid")
        AccBal.processTransaction(tx1)
        print("Account balance updated")
        AccBal.print(pubKeyMapabcd)
    else:
            print("Transaction is invalid")

    print("6.6 Create a transaction tx2 which takes as inputs from B2 10, C2 10, and as outputs given D1 15 and C3 the change (whatever is left) ")
    TxOuLi1=TxOutputList(pubKeyD1,15,pubKeyC3,5)
    Tiu2 = TxInputUnsigned(pubKeyB2,10)
    B2message=Tiu2.getMessageToSign(TxOuLi1)
    signB2 = Bobwallet.signMessage(B2message,"B2")
    Tiu3=TxInputUnsigned(pubKeyC2,10)
    C2message = Tiu3.getMessageToSign(TxOuLi1)
    signC2 = Carolwallet.signMessage(C2message,"C2" )
    txil6=TxInputList(pubKeyB2,10,signB2,pubKeyC2,10,signC2)
    trx=Transaction(txil6,TxOuLi1)
    AccBal.print(pubKeyMapabcd)

    print("6.7 Check whether the signature is approved for the transaction input, and whether the transaction is valid. Then update the AccountBalance using that transaction.")
    if  AccBal.checkTransactionValid(trx):
        print("signature is approved transaction input and the transaction is valid")
        AccBal.processTransaction(trx)
        print("Account balance updated")
        AccBal.print(pubKeyMapabcd)
        
    else:
        print("Transaction is invalid")

if __name__=="__main__":
    test()    
    
    

    
            

            


    
    
                

            


    

    
