def main():
    MOVIE_FILE = 'watching_list.txt'
    if yes('Would you like to load a watching list from a file?'):
        treeFile = open(MOVIE_FILE, 'r')
        MovieTree = loadTree(treeFile)
        treeFile.close()
    else:
        MovieTree = BinarySearchTree()

class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        if isinstance(val, list):
            self.val = val
        else:
            self.val = [val]
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self,key,value,lc,rc):
        self.key = key
        self.val = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
        elif key == currentNode.key:
            currentNode.val.append(val)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.val
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)


traverse_list = []
def traverse(root):
    if not root:
        return
    traverse_list.append(root.val)
    traverse(root.leftChild)
    traverse(root.rightChild)
    return traverse_list


def loadTree(treeFile):
    newtree = BinarySearchTree()
    while True:
        line = treeFile.readline().strip()
        if line == '':
            break
        elif line.isdigit():
            int(line)
            key = int(line)
            # movie_json_list = []
        else:
            # line = line.replace('\'', '\"')
            movie = json.loads(json.dumps(eval(line)))
            newtree.put(key, movie)
    # print(newtree.root.val)
    return newtree


def yes(prompt):
    answer = input(prompt)
    if answer in ['yes', 'y']:
        return True
    elif answer in ['no', 'n']:
        return False


if __name__ == '__main__':
    main()
