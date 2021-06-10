import tonos_ts4.ts4 as ts4
import unittest
import time

EXCHANGER_COMMISSION = 3

class key:
    secret: str
    public: str
class TestPair(unittest.TestCase):
    secret = "bc891ad1f7dc0705db795a81761cf7ea0b74c9c2a93cbf9ac1bad8bd30c9b3b75a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    public = "0x5a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    def test_exchanger(self):
        ts4.reset_all() # reset all data
        ts4.init('./', verbose = True)
        key1 = ts4.make_keypair()
        self.public1 = key1[1]
        self.secret1 = key1[0]
        fileContract = ts4.BaseContract('file',dict(chunks_count=5),pubkey=self.public,private_key=self.secret,balance=150_000_000_000,nickname="FileContract")

        fileContract.call_method('writeData',dict(index=1,chunk=ts4.Bytes("5423")),private_key=self.secret) 
        fileContract.call_method('writeData',dict(index=0,chunk=ts4.Bytes("5423")),private_key=self.secret) 

        ts4.dispatch_messages()
        print(fileContract.call_getter("getDetails"))
        print(fileContract.call_getter("getData",dict(index=1)))
    # def test_exchanger1(self):
    #     ts4.reset_all() # reset all data
    #     ts4.init('./', verbose = True)
    #     key1 = ts4.make_keypair()
    #     self.public1 = key1[1]
    #     self.secret1 = key1[0]
    #     fileContract = ts4.BaseContract('14_CustomReplayProtection',dict(),pubkey=self.public,private_key=self.secret,balance=150_000_000_000,nickname="FileContract")

    #     fileContract.call_method('storeValue',dict(new_value=1),private_key=self.secret) 

    #     ts4.dispatch_messages()
    #     #print(fileContract.call_getter("getDetails"))
    #     print(fileContract.call_getter("getData",dict(index=1)))
if __name__ == '__main__':
    unittest.main()
