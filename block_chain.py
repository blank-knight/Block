import hashlib
import datetime

class block:
    def __init__(self,data,pre_hash) -> None:
        self.loc = 1
        self.data = data  
        self.pre_hahs = pre_hash
        self.hash = self.com_hash(pre_hash)
        self.nex_block = None

    def com_hash(self,pre_hash):
        val = self.data+pre_hash
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

class chain:
    def __init__(self) -> None:
        self.first_block = self.fir_block()
        self.length = 1

    def fir_block(self):
        f_blcok = block("I am first blcok","")
        return f_blcok
    
    def find_cur_block(self):
        if self.length == 2:
            return self.first_block.nex_block
        self.cur_block = self.first_block.nex_block
        for i in range(self.length-2):
            self.cur_block = self.cur_block.nex_block
        return self.cur_block

    def output_chain_info(self):
        self.cur_block = self.first_block
        for i in range(self.length):
            dic1 = self.cur_block.__dict__
            print('\n'.join(('%s:%s' % item for item in dic1.items())))
            self.cur_block = self.cur_block.nex_block

    # 我这里是通过指针连接的,也可以使用堆栈进行顺序连接
    # 添加区块的方式1:直接添加数据
    def add_block_1(self,data):
        if self.length == 1:
            self.first_block.nex_block = block(data,self.first_block.hash)
            self.first_block.nex_block.loc += 1
            self.length += 1
        else:
            self.cur_block = self.find_cur_block()
            self.cur_block.nex_block = block(data,self.cur_block.hash)
            self.cur_block.nex_block.loc += self.cur_block.loc
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
        if self.first_block.hash != self.first_block.com_hash(""): # 验证创世区块
            print("数据被篡改了")
            return 0
        self.pre_block = self.first_block
        self.cur_block = self.first_block.nex_block # 从创世区块之后开始挨着验证
        for i in range(1,self.length):
            # 判断当前区块是否被篡改,由于我这里com_hash的计算同时用了账本data和前一区块的hash,所以这里只用一个验证即可,只要其中
            #一个改了,当前区块的hash就会对不上
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
    chain_test.add_block_1("给赵文韬转账1000元")
    chain_test.add_block_1("给赵文韬转账20000元")
    chain_test.add_block_1("给赵文韬转账30000000元")
    chain_test.output_chain_info()

    # 测试修改账本
    block2 = chain_test.get_block(2)
    print(block2.__dict__)
    block2.data = "我不转钱了"
    chain_test.validation()
    block1 = chain_test.get_block(1)
    block1.data = "我是魔神区块"
    chain_test.validation()

    # 测试修改hash
    block2 = chain_test.get_block(2)
    val = "jojojojo"
    hh = hashlib.sha256(val.encode('utf-8')).hexdigest()
    block2.hash = hh
    chain_test.validation()
    print(block2.__dict__)
    print(hh)