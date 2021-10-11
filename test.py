import tonos_ts4.ts4 as ts4
import unittest
import time
import math
import magic
mime = magic.Magic(mime=True)
m = mime.from_file("Black_triangle.svg")

EXCHANGER_COMMISSION = 3

class key:
    secret: str
    public: str

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
chunk_size = 10000
file_name = "Black_triangle.svg"
class TestPair(unittest.TestCase):
    secret = "bc891ad1f7dc0705db795a81761cf7ea0b74c9c2a93cbf9ac1bad8bd30c9b3b75a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    public = "0x5a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    def test_exchanger(self):
        ts4.reset_all() # reset all data
        ts4.init('./', verbose = True)
        key1 = ts4.make_keypair()
        self.public1 = key1[1]
        self.secret1 = key1[0]

        with open(file_name,"rb") as f:
            temp = f.read()
        fileContract = ts4.BaseContract('file',dict(chunks_count=math.ceil(len(temp) / chunk_size),mime=m,extension=file_name.split(".")[-1]),pubkey=self.public,private_key=self.secret,balance=150_000_000_000,nickname="FileContract")
        num = 0
        for i in list(chunks(temp, chunk_size)):
            print(i)
            fileContract.call_method('writeData',dict(index=num,chunk=i.hex()),private_key=self.secret) 
            num+= 1

        ts4.dispatch_messages()
        decode = fileContract.call_getter("getDetails")
        print(decode)
        with open("Output." + decode[4],"wb") as f:
            for i in decode[-1]:
                f.write(bytes.fromhex(i))
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
