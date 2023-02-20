class AvlNode:
    def __init__(self, data=None, parent=None, left=None, right=None, next=None, prev=None):
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 1
        self.next = next
        self.prev = prev
        self.nodesBelow = 1


    @property
    def imbalanceFactor(self):
        if self.left == None and self.right == None:
            return 0
        elif self.left == None and self.right != None:
            return self.right.height * -1
        elif self.left != None and self.right == None:
            return self.left.height
        else:
            return self.left.height - self.right.height


    @property
    def isLeft(self):
        if self.parent == None:
            return False
        return self.parent.left == self


    @property
    def isRoot(self):
        return self.parent == None


    def updateNode(self):
        if self.left == None and self.right == None:
            self.height = 1
            self.nodesBelow = 1
        elif self.left == None and self.right != None:
            self.height = self.right.height + 1
            self.nodesBelow = self.right.nodesBelow + 1
        elif self.left != None and self.right == None:
            self.height = self.left.height + 1
            self.nodesBelow = self.left.nodesBelow + 1
        else:
            self.height = max(self.left.height, self.right.height) + 1
            self.nodesBelow = self.right.nodesBelow + self.left.nodesBelow + 1


    @staticmethod
    def setParentSon(parent, son, isLeft):
        if isLeft == True and parent != None:
            parent.left = son
        elif parent != None:
            parent.right = son
        if son != None:
            son.parent = parent


    @staticmethod
    def setPrevNext(nodeA, nodeB, compareFunction):
        if nodeA.next == None and compareFunction(nodeA, nodeB) == "SMALLER":
            nodeA.next = nodeB
            nodeB.prev = nodeA
        elif nodeA.next != None and compareFunction(nodeA, nodeB) == "SMALLER" and compareFunction(nodeB, nodeA.next) == "SMALLER":
            nodeC = nodeA.next
            nodeC.prev = nodeB
            nodeB.next = nodeC
            nodeA.next = nodeB
            nodeB.prev = nodeA
        elif nodeA.prev == None and compareFunction(nodeA, nodeB) == "BIGGER":
            nodeA.prev = nodeB
            nodeB.next = nodeA
        elif nodeA.prev != None and compareFunction(nodeA, nodeB) == "BIGGER" and compareFunction(nodeB, nodeA.prev) == "BIGGER":
            nodeC = nodeA.prev
            nodeA.prev = nodeB
            nodeB.next = nodeA
            nodeC.next = nodeB
            nodeB.prev = nodeC


    def __str__(self):
        return f"{self.data}"