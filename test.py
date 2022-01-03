

class TreeNode:
    def __init__(self,val) -> None:
        self.val = val
        self.ltag = 0
        self.rtag = 0
        self.left = None
        self.right = None

test = TreeNode(1)
print(test.__dict__)
print('\n'.join(('%s:%s' % item for item in dic1.items())))
