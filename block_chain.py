import hashlib
import datetime
import os
from sys import int_info
from Crypto import PublicKey
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC

def diffculty(diff):
    res = ""
    for i in range(diff):
        res += "0"
    return res

# 公私钥的生成和签名对象的生成(模拟钱包节点)
class wallet:
    def __init__(self) -> None:
        self.key = ECC.generate(curve='P-256') # 生成ECC密钥对
        self.signer = DSS.new(self.key, 'fips-186-3') # 生成签名对象

    def __repr__(self) -> str:
        # 钱包地址是对公钥进行hash生成的
        # 不直接用公钥做地址是为了安全起见
        return "Wallet_address:"+SHA256.new((self.key.public_key()).encode()).hexdigest()

class block:
    # 交易信息,前一个区块的hash,矿工地址,交易发起者(交易签名者)
    def __init__(self,transaction,pre_hash,wallet="",miner_address="赵文韬") -> None:
        self.loc = 1
        self.diff = 1 # 当前区块的挖矿难度(前面要求几个0)
        self.pre_hash = pre_hash
        self.timestamp = datetime.datetime.now()
        self.hash = None
        self.reward = 10 # 挖矿成功的奖励,由当前区块发放
        self.wallet = wallet
        self.transaction = transaction
        self.miner_reward = self.mine(transaction,miner_address) # 开始挖矿
        self.nex_block = None
        

    def __repr__(self) -> str:
        return "loc = "+str(self.loc)+"\ntime = "+str(self.timestamp)+"\ntransaction = "\
            +self.transaction+"\nminer_reward="+self.miner_reward+"\npre_hash = "+self.pre_hash+"\nhash = "+self.hash+"\n"
        
    def com_hash(self,transaction):
        sig_hash = SHA256.new((transaction+self.pre_hash).encode()).hexdigest()
        val = sig_hash+str(self.nonce)+str(self.timestamp)
        return hashlib.sha256(val.encode('utf-8')).hexdigest()


    # 挖矿
    def mine(self,transaction,miner_address):
        res = self.validation() if self.wallet != "" else "" # 开始验证是否是有效的交易
        if res == 0:
            return 0
        self.nonce = 1
        pre_string = diffculty(self.diff)
        while(True):
            if self.com_hash(transaction)[0:self.diff] != pre_string[0:self.diff]:
                self.nonce += 1
                continue
            else:
                self.hash = self.com_hash(transaction)
                return self.hash+" "+miner_address+" "+str(self.reward)

    # 模拟发送,接受和验证
    def validation(self):
        self.tra_hash = SHA256.new((self.transaction+self.pre_hash).encode()) # 对交易信息和前一个区块的hash再进行hash
        self.sign_obj = wallet.signer.sign(self.tra_hash) if wallet!="" else self.transaction # 对得到的hash进行签名
        with open('sign.bin', 'wb') as f: # 将签名写入文件，模拟发送（同时还发送了文本内容，为了方便，不写文件，后面直接引用）
            f.write(self.sign_obj)
        with open('sign.bin', 'rb') as f: # 读取签名内容，模拟接收
            sign_new = f.read()
            # sign_new = bytearray(f.read())  改为可修改的二进制数组,但这里有问题,不能用这个
        # 接受者对象
        '''
            测试修改二进制文件,看是否能发现
        '''
        # a=123
        # b=a.to_bytes(1,'big')
        # sign_new += b
        verifer = DSS.new(self.wallet.key.public_key(), 'fips-186-3') 
        hasher = SHA256.new((self.transaction+self.pre_hash).encode()) # 对收到的文件进行hash
        try:
            verifer.verify(hasher,sign_new) # 校验摘要（本来的样子）和收到并解密的签名是否一致
            # print("签名有效")
        except:
            print("签名无效,停止挖矿")
            return 0


class chain:
    def __init__(self) -> None:
        self.first_block = self.fir_block()
        self.length = 1
        self.transactionPool = []

    # fro为发送者公钥,to为接受这公钥,amount为交易具体信息
    # signer 为签名对象
    def add_Transaction(self,fro,to,amount):
        if len(fro.strip()) == 0 or len(fro.strip()) == 0: # 交易地址不能为空和空格
            print("交易地址错误,请重新输入")
            return 0
        if amount <= 0:
            print("无效的交易金额,请重新输入") # 交易金额不能为负或者0
            return 0
        string = fro+" "+to+" "+str(amount)
        # 交易信息直接公开,可以先不用签名.
        self.transactionPool.append(string) # 有效的交易加入交易池等待矿工来挖矿

    def fir_block(self):
        f_blcok = block("I am first blcok","") 
        return f_blcok
    
    def find_pre_block(self):
        if self.length == 2:
            return self.first_block.nex_block
        self.pre_block = self.first_block.nex_block
        for i in range(self.length-2):
            self.pre_block = self.pre_block.nex_block
        return self.pre_block

    # 输出区块链的信息
    def output_chain_info(self):
        self.cur_block = self.first_block
        for i in range(self.length):
            print(self.cur_block)
            # dic1 = self.cur_block.__dict__
            # print('\n'.join(('%s:%s' % item for item in dic1.items())))
            self.cur_block = self.cur_block.nex_block

    # 我这里是通过指针连接的,也可以使用堆栈进行顺序连接
    def add_block(self,wallet,transaction=None):
        transaction = self.transactionPool.pop(0)
        if self.length == 1:
            # print(type(transaction))
            # print(type(self.first_block.hash))
            self.first_block.nex_block = block(transaction,self.first_block.hash,wallet)
            self.first_block.nex_block.loc += 1
            self.length += 1
        else:
            self.pre_block = self.find_pre_block()
            self.pre_block.nex_block = block(transaction,self.pre_block.hash,wallet)
            self.pre_block.nex_block.loc += self.pre_block.loc
            self.length += 1

    # 获取一个区块
    def get_block(self,num):
        if num == 1:
            return self.first_block
        for i in range(num):
            self.cur_block = self.first_block.nex_block
        return self.cur_block

    def __len__(self):
        return self.length

    def validation(self):
        if self.first_block.hash != self.first_block.com_hash("I am first blcok"): # 验证创世区块
            print("数据被篡改了")
            return 0
        self.pre_block = self.first_block
        self.cur_block = self.first_block.nex_block # 从创世区块之后开始挨着验证
        for i in range(1,self.length):
            # 判断当前区块是否被篡改,由于我这里com_hash的计算同时用了账本transaction和前一区块的hash,所以这里只用一个验证即可,只要其中
            #一个改了,当前区块的hash就会对不上.改hash,左边的会变,改transaction,右边的会变,直接一个验证即可
            if self.cur_block.hash !=  self.cur_block.com_hash(self.pre_block.hash): 
                print("数据被篡改了")
                return 0
            # elif self.pre_block.hash != self.cur_block.hash: # 判断区块间的hash能否对上
            #     print("前后hash对不上,区块链断裂")
            #     return 0
        print("区块链一切正常")
        

if __name__ == "__main__":
    # 测试添加区块
    chain_test = chain()
    wallet = wallet()
    # print(wallet)
    chain_test.validation()
    chain_test.add_Transaction("赵文甲","赵文乙",1000)
    chain_test.add_Transaction("赵文丙","赵文丁",2000)
    chain_test.add_Transaction("赵文帅","赵文韬",3000)
    # signer = wallet.signer
    # a = "fafa"
    # tra_hash = hashlib.sha256(a.encode('utf-8')).hexdigest() # 对交易信息和前一个区块的hash再进行hash
    # sign_obj = signer.sign(tra_hash) if signer!="" else 141 # 对得到的hash进行签名
    chain_test.add_block(wallet)
    chain_test.add_block(wallet)
    chain_test.add_block(wallet)
    # chain_test.add_block("给赵文韬转账20000元")
    # chain_test.add_block("给赵文韬转账30000000元")
    chain_test.output_chain_info()
    # input("请按任意键继续")

    # 测试修改区块
    block2 = chain_test.get_block(2)
    print(block2)
    block2.transaction = "我不转钱了"
    chain_test.validation()
    # chain_test.output_chain_info()

    # print("____________________________________")
    # # # 测试修改hash
    block3 = chain_test.get_block(3)
    val = "jojojojo"
    hh = hashlib.sha256(val.encode('utf-8')).hexdigest()
    block2.hash = hh
    chain_test.validation()