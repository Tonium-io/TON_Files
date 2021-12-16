import tonos_ts4.ts4 as ts4
import unittest
import time
import math
import magic
import base64
from tonclient.client import TonClient
from tonclient.types import ParamsOfCompressZstd, ParamsOfDecompressZstd, ClientConfig, NetworkConfig
import time
mime = magic.Magic(mime=True)

file_name = "rust.so"
m = mime.from_file(file_name)

client = TonClient(config=ClientConfig(network=NetworkConfig(server_address='https://net.ton.dev')))

LEVELS = 21

class key:
    secret: str
    public: str

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
chunk_size = 15000

class TestPair(unittest.TestCase):
    secret = "bc891ad1f7dc0705db795a81761cf7ea0b74c9c2a93cbf9ac1bad8bd30c9b3b75a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    public = "0x5a4889716084010dd2d013e48b366424c8ba9d391c867e46adce51b18718eb67"
    def test_exchanger(self):
        zstd = False
        ts4.reset_all() # reset all data
        ts4.init('./', verbose = False )
        key1 = ts4.make_keypair()
        self.public1 = key1[1]
        self.secret1 = key1[0]

        with open(file_name,"rb") as f:
            temp = f.read()
        prev = time.time()
        t = client.utils.compress_zstd(ParamsOfCompressZstd(uncompressed=str(base64.b64encode(temp),"utf-8"),level=LEVELS))
        print(f"Encoding takes {time.time() - prev} seconds")
        print(f"Compressing in x{round(len(temp) / len(t.compressed),2)}")
        
        if len(t.compressed) < len(temp):
            temp =  base64.b64decode(t.compressed)
            zstd = True
        fileContract = ts4.BaseContract('file',dict(chunks_count=math.ceil(len(temp) / chunk_size),mime=m,extension=file_name.split(".")[-1],zstd_encoding=zstd),pubkey=self.public,private_key=self.secret,balance=150_000_000_000,nickname="FileContract")
        num = 0
        for i in list(chunks(temp, chunk_size)):
            fileContract.call_method('writeData',dict(index=num,chunk=i.hex()),private_key=self.secret) 
            num+= 1

        ts4.dispatch_messages()
        decode = fileContract.call_getter("getDetails")
        d = bytes.fromhex(''.join(decode[-2]))
        if decode[-1]:
            prev = time.time()
            t = client.utils.decompress_zstd(ParamsOfDecompressZstd(compressed=str(base64.b64encode(d),"utf-8")))
            print(f"Decoding takes {time.time() - prev} seconds")
            d = base64.b64decode(t.decompressed)
        with open("Output." + decode[4],"wb") as f:
            f.write(d)

if __name__ == '__main__':
    unittest.main()
