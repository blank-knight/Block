from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
 
# 生成ECC密钥对
key = ECC.generate(curve='P-256')
ke = key.public_key()
# print("key:",key)

# 待签名内容(发送的文本内容)
message = 'I am MKing Hello Everyone'
 
# 签名
signer = DSS.new(key, 'fips-186-3') # 第二个参数代表生成模式，fips-186-3表示签名生成是随机的,用DSS生成签名对象,签名对象本人可进行签名
hasher = SHA256.new(message.encode()) # 对文本进行Hash，提取内容摘要
sign_obj = signer.sign(hasher)     #用私钥对消息签名
 

# print('签名后:', sign_obj)
# print('签名者:', signer)
# print('公钥:', key.public_key())
# print('私钥:', key.has_private())
# print('export_key:', key)

 
# 将签名写入文件，模拟发送（同时还发送了文本内容，为了方便，不写文件，后面直接引用）
with open('sign.bin', 'wb') as f:
    f.write(sign_obj)
 
# 读取签名内容，模拟接收
with open('sign.bin', 'rb') as f:
    sign_new = bytearray(f.read())  # 签名内容(二进制)，并转成bytearray，bytearray是可变数组,将数据进行encode编码,可通过decode解码,
                                    # 相当于b'str',但b'str'是不可变的,这里变为可变的是方便后面模拟错误签名
 
# sign_new.append(0x32)  # 模拟错误的签名
print('错误签名:', sign_new)
 
# 验证签名
print("sign_obj:",sign_obj)
verifer = DSS.new(key.public_key(), 'fips-186-3') # 使用公钥创建校验对象
hasher = SHA256.new(message.encode()) # 对收到的消息文本提取摘要
print('hasher:', hasher)
try:
    verifer.verify(hasher,sign_new) # 校验摘要（本来的样子）和收到并解密的签名是否一致
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is not valid.")