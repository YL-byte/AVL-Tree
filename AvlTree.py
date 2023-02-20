from AvlNode import AvlNode
class AvlTree:
    @staticmethod
    def compare(nodeA, nodeB):
        if (nodeA.data < nodeB.data):
            return "SMALLER"
        elif (nodeA.data == nodeB.data):
            return "EQUAL"
        else:
            return "BIGGER"


    def __init__(self, compareFunction=None):
        self.size = 0
        self.root = None
        self.compareFunction = compareFunction
        if (compareFunction == None):
            self.compareFunction = AvlTree.compare


    def find(self, data):
        tempNode = AvlNode(data=data)
        currentNode = self.root
        while(currentNode != None):
            if (self.compareFunction(currentNode, tempNode) == "EQUAL"):
                return currentNode
            elif (self.compareFunction(currentNode, tempNode) == "SMALLER"):
                currentNode = currentNode.right
            else:
                currentNode = currentNode.left
        return None


    def findClosestFromAbove(self, data):
        tempNode = AvlNode(data=data)
        currentNode = self.root
        result = None
        while(currentNode != None):
            if (self.compareFunction(currentNode, tempNode) == "EQUAL"):
                return currentNode
            elif (self.compareFunction(currentNode, tempNode) == "SMALLER"):
                currentNode = currentNode.right
            else:
                result = currentNode
                currentNode = currentNode.left
        return result


    def findClosestFromBelow(self, data):
        tempNode = AvlNode(data=data)
        currentNode = self.root
        result = None
        while(currentNode != None):
            if (self.compareFunction(currentNode, tempNode) == "EQUAL"):
                return currentNode
            elif (self.compareFunction(currentNode, tempNode) == "SMALLER"):
                result = currentNode
                currentNode = currentNode.right
            else:
                currentNode = currentNode.left
        return result


    def add(self, data):
        if self.find(data) != None:
            return
        newNode = AvlNode(data=data)
        self.size += 1
        if self.root == None:
            self.root = newNode
            return
        currentNode = self.root
        while currentNode != None:
            AvlNode.setPrevNext(currentNode, newNode, self.compareFunction)
            if (self.compareFunction(currentNode, newNode) == "EQUAL"):
                raise Exception(f"Data {data} already exists and was somehow not found")
            elif (self.compareFunction(currentNode, newNode) == "SMALLER"):
                if(currentNode.right == None):
                    AvlNode.setParentSon(currentNode, newNode, False)
                    self._balanceUp(newNode)
                    return
                currentNode = currentNode.right
            else:
                if(currentNode.left == None):
                    AvlNode.setParentSon(currentNode, newNode, True)
                    self._balanceUp(newNode)
                    return
                currentNode = currentNode.left
        raise Exception("Was not suppose to get here")


    def remove(self, data):
        tempNode = AvlNode(data=data)
        currentNode = self.root
        while currentNode != None:
            if self.compareFunction(currentNode, tempNode) == "EQUAL":
                break
            elif self.compareFunction(currentNode, tempNode) == "SMALLER":
                currentNode = currentNode.right
            else:
                currentNode = currentNode.left
        if currentNode == None:
            return
        self.size -= 1
        if currentNode.next != None:
            currentNode.next.prev = currentNode.prev
        if currentNode.prev!= None:
            currentNode.prev.next = currentNode.next
        repeat = True
        while repeat:
            repeat = False
            if currentNode.left == None and currentNode.right == None:
                if currentNode.isRoot:
                    self.root = None
                elif currentNode.isLeft:
                    currentNode.parent.left = None
                    self._balanceUp(currentNode.parent)
                else:
                    currentNode.parent.right = None
                    self._balanceUp(currentNode.parent)
            elif currentNode.left != None and currentNode.right == None:
                if currentNode.isRoot:
                    self.root = currentNode.left
                elif currentNode.isLeft:
                    currentNode.parent.left = currentNode.left
                    self._balanceUp(currentNode.parent)
                else:
                    currentNode.parent.right = currentNode.left
                    self._balanceUp(currentNode.parent)
            elif currentNode.left == None and currentNode.right != None:
                if currentNode.isRoot:
                    self.root = currentNode.right
                elif currentNode.isLeft:
                    currentNode.parent.left = currentNode.right
                    self._balanceUp(currentNode.parent)
                else:
                    currentNode.parent.right = currentNode.right
                    self._balanceUp(currentNode.parent)
            elif currentNode.left != None and currentNode.right != None:
                replaceNode = currentNode.right
                while replaceNode.left != None:
                    replaceNode = replaceNode.left
                currentNode.data = replaceNode.data
                currentNode = replaceNode
                repeat = True


    @property
    def min(self):
        result = self.root
        while(result.left != None):
            result = result.left
        return result


    @property
    def max(self):
        result = self.root
        while (result.right != None):
            result = result.right
        return result


    def getIth(self, i):
        if (i < 0):
            raise Exception(f"{i} is smaller than 0")
        current = self.root
        while (current != None):
            if current.left == None and i == 0:
                return current
            elif current.left != None and current.left.nodesBelow == i:
                return current
            elif current.left != None and current.left.nodesBelow > i:
                current = current.left
            elif current.left != None and current.left.nodesBelow < i:
                i -= current.left.nodesBelow + 1
                current = current.right
            elif current.left == None and current.right != None:
                i -= 1
                current = current.right
            else:
                print(current, i)
        return None


    def _balanceUp(self, leafNode):
        currentNode = leafNode
        while currentNode != None:
            currentNode.updateNode()
            nextNode = currentNode.parent
            self._chooseRoll(currentNode)
            currentNode.updateNode()
            currentNode = nextNode


    def _chooseRoll(self, root):
        if root.imbalanceFactor > 2 or root.imbalanceFactor < -2:
            raise Exception(f"{root.data} has imbalanceFactor of {root.imbalanceFactor}")
        elif root.imbalanceFactor == 2 and (root.left == None or root.left.imbalanceFactor >= 0):
            self._rightRoll(root)
        elif root.imbalanceFactor == -2 and (root.right == None or root.right.imbalanceFactor <= 0):
            self._leftRoll(root)
        elif root.imbalanceFactor == 2 and root.left.imbalanceFactor == -1:
            self._leftRightRoll(root)
        elif root.imbalanceFactor == -2 and root.right.imbalanceFactor == 1:
            self._rightLeftRoll(root)


    def _leftRightRoll(self, root):
        if root == None:
            return
        self._leftRoll(root.left)
        self._rightRoll(root)


    def _rightLeftRoll(self, root):
        if root == None:
            return
        self._rightRoll(root.right)
        self._leftRoll(root)


    def _leftRoll(self, root):
        if root == None:
            return
        rootParent = root.parent
        isLeft = root.isLeft
        isRoot = root.isRoot
        rootRight = root.right
        if rootRight != None:
            rootRightLeft = rootRight.left
        else:
            rootRightLeft = None
        AvlNode.setParentSon(rootParent, rootRight, isLeft)
        AvlNode.setParentSon(rootRight, root, True)
        AvlNode.setParentSon(root, rootRightLeft, False)
        if isRoot:
            self.root = rootRight
        elif isLeft:
            AvlNode.setParentSon(rootParent, rootRight, True)
        else:
            AvlNode.setParentSon(rootParent, rootRight, False)
        root.updateNode()
        rootRight.updateNode()


    def _rightRoll(self, root):
        if root == None:
            return
        rootParent = root.parent
        isLeft = root.isLeft
        isRoot = root.isRoot
        rootLeft = root.left
        if rootLeft != None:
            rootLeftRight = rootLeft.right
        else:
            rootLeftRight = None
        AvlNode.setParentSon(rootParent, rootLeft, isLeft)
        AvlNode.setParentSon(rootLeft, root, False)
        AvlNode.setParentSon(root, rootLeftRight, True)
        if isRoot:
            self.root = rootLeft
        elif isLeft:
            AvlNode.setParentSon(rootParent, rootLeft, True)
        else:
            AvlNode.setParentSon(rootParent, rootLeft, False)
        root.updateNode()
        rootLeft.updateNode()