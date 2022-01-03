import hashlib
# string1 = "thisismytest"
# out1 = hashlib.sha256(string1.encode('utf-8')).hexdigest()
# # print(out1)
'''
    对于不同的输入，哪怕只是一个很微小的改动，输出的结果都是很不一样的。
    对于同一个输入，输出结果是一样  
    我现在需要得到 一个 开头值为0的哈希值。请告诉我X是多少
    我现在需要得到 一个 开头值前4位全为0的哈希值。请告诉我X是多少
'''
def POW(data,diff):
    x = 0
    while(True):
        pass