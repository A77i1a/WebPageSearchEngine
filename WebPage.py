class AVLnode:

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.height = None


class AVLtree:

    def __init__(self):

        self.root = None

    def get(self, data):

        a = self.search(data, self.root)

        if a is False:
            return []

        elif a is not None:
            return a.value

    def search(self, data, cur_node):
        if cur_node is None:
            return False

        elif data == cur_node.key:
            return cur_node

        if data < cur_node.key:
            return self.search(data, cur_node.left)
        elif data > cur_node.key:
            return self.search(data, cur_node.right)
        else:
            return False

    def put(self, data, value=None):
        # print("Add-" + str(data) + '-' + str(value))
        data = AVLnode(data, value)
        y = None
        x = self.root

        while x is not None:
            y = x
            if data.key < x.key:
                x = x.left
            else:
                x = x.right

        data.parent = y

        if y == None:
            self.root = data

        elif data.key < y.key:
            y.left = data
        else:
            y.right = data

        self.setHeight(data, data.key)

    def setHeight(self, node, newInsert=None):
        newInsert = newInsert
        node.height = self._setHeight(node)

        if newInsert != None:
            self.unbalanceDetector(node, newInsert)

        if node.parent != None:
            self.setHeight(node.parent, newInsert)

    def _setHeight(self, node):

        if node == None:
            return 0
        left = self._setHeight(node.left)
        right = self._setHeight(node.right)
        return max(left, right) + 1

    def __setHeight(self, node):

        if node != None:
            node.height = self._setHeight(node)
            self.__setHeight(node.left)
            self.__setHeight(node.right)

    def unbalanceDetector(self, node, newInsert):

        root = node
        if root.left != None:
            leftH = root.left.height

        else:
            leftH = 0

        if root.right != None:
            rightH = root.right.height
        else:
            rightH = 0

        bHeight = leftH - rightH

        if bHeight < -1 or bHeight > 1:
            # print("the node %s is unblanced" % (node.key))
            # print("the new insert value %s" % (newInsert))
            self.directionDetector(node, bHeight, newInsert)

    def directionDetector(self, node, bfctor, newInsert):

        if bfctor > 1 and newInsert < node.left.key:
            # print("LL case")
            self.leftRoation(node)

        elif bfctor < -1 and newInsert > node.right.key:
            # print("RR case")
            self.rightRoation(node)

        elif bfctor > 1 and newInsert > node.left.key:
            # print("LR case")
            self.rightRoation(node.left)
            self.leftRoation(node)

        elif bfctor < -1 and newInsert < node.right.key:
            # print("RL case")
            self.leftRoation(node.right)
            self.rightRoation(node)

    def leftRoation(self, node):

        root = node
        pivot = node.left  # find the pivot in left side

        root.left = pivot.right  # move the right child of pivot to root
        # FIX2: add parent reset
        if pivot.right != None:
            pivot.right.parent = root
        pivot.right = root  # then pivot has right child root

        # reset their parent
        pivot.parent = root.parent
        root.parent = pivot

        # if the pivot has parent
        if pivot.parent != None:

            # depends if pivot is in his parent left or right
            # according to the postion, insert pivot as child to his parent
            # FIX1: need to check if pivot.parent.left exists or not
            if pivot.parent.left != None:
                if pivot.parent.left.key == root.key:
                    pivot.parent.left = pivot
                else:
                    pivot.parent.right = pivot
            else:
                pivot.parent.right = pivot

            # reset the height for parent above
            self.setHeight(pivot.parent)
        else:
            self.root = pivot

        # reset the height for pivot
        self.__setHeight(pivot)

    def rightRoation(self, node):

        root = node
        pivot = node.right

        root.right = pivot.left
        # FIX2: add parent reset
        if pivot.left != None:
            pivot.left.parent = root
        pivot.left = root

        pivot.parent = root.parent
        root.parent = pivot

        if pivot.parent != None:
            # FIXED: need to check if pivot.parent.left exists or not
            if pivot.parent.left != None:
                if pivot.parent.left.key == root.key:
                    pivot.parent.left = pivot
                else:
                    pivot.parent.right = pivot
            else:
                pivot.parent.right = pivot

            self.setHeight(pivot.parent)
        else:
            self.root = pivot
        self.__setHeight(pivot)

    # Printing the tree
    def printTree(self):
        # print("new tree:")
        self.__printTree(self.root)

    def __printTree(self, node, level=0):
        if node is None:
            return
        if node.value != None:
            self.__printTree(node.left, level + 1)
            # print(' ' * 4 * level + '->', str(node.key) + "," + str(node.value) + "," + str(node.height))
            self.__printTree(node.right, level + 1)


class WebPageIndex:
    """Class creates index representation of webpage
    using AVLTreeMap """
    def __init__(self, file):
        """Function initializes each instance of
        WebPageIndex from a txt file."""
        self.file = file  # Holds inputted file
        self.tree = AVLtree()  # Calls AVLTree object
        f = open("/Users/attilatavakolli/Desktop/data/" + file, 'r')  # insert file path in " "
        f1 = f.read().lower().replace("\n", " ").replace(".", "") \
            .replace(",", "").replace("(", "").replace(")", "") \
            .replace(":", "").split(" ")  # Reads file and separates words
        for i in range(len(f1)):
            wordList = []  # Initializing index list
            for j in range(len(f1)):
                if f1[j] == f1[i]:
                    wordList.append(1)
                else:
                    wordList.append(0)
            if self.tree.search(f1[i], self.tree.root) is False:
                self.tree.put(f1[i], wordList)
        f.close()

    def getCount(self, s):
        """Function returns number of times a word
        has appeared on the page"""
        val = self.tree.get(s)
        count = val.count(1)  # Counts appearances of the word in list
        return count

    def getFile(self):
        """Function returns file name"""
        return self.file


class WebpagePriorityQueue:
    """Class contains array based list(maxheap) that
    holds the highest priority value web pages based
    on specific query. """
    def __init__(self, query, set):
        """Function takes in query and set of
        WebpageIndex instances and creates max heap."""
        self.query = query  # Inputted query
        self.set = set  # Set of WebPageIndexes
        self.maxHeap = []  # Initializes max heap
        for instance in set:
            # print(instance)
            self.maxHeap.append(instance)  # Adds each instance to heap

        for i in range(len(self.maxHeap) - 1, -1, -1):  # Begins from last value
            if i != 0:
                self.heapSortUp(self.maxHeap, i)  # Raising highest priority node up

        for i in range(len(self.maxHeap) - 1):  # Begins from first value
            self.heapSortDown(self.maxHeap, i)  # Sifting down

    def heapSortUp(self, heap, i):
        """Function brings the highest priority node
        to the root of the tree. """
        priority = self.getPriorityParent(heap, i)  # Returns list of priority of node and parent
        if priority[0] > priority[1]:  # If node has higher priority than parent, swap values
            temp = heap[(i - 1) // 2]
            heap[(i - 1) // 2] = heap[i]
            heap[i] = temp  #
            return heap  # Returns new heap
        else:
            return heap  # Returns same heap

    def heapSortDown(self, heap, i):
        """Function sorts the heap by priority
        and going down the tree."""
        p = self.getPriorityChildren(heap, i)  # Returns list of priority of node and children
        if p[0] < p[1] or p[0] < p[2]:  # If nodes priority is less than either child
            if p[1] < p[2]:  # If right child priority is more than left, swap node with right
                temp = heap[i]
                heap[i] = heap[2 * i + 2]
                heap[2 * i + 2] = temp
                return heap
            else:  # Swap node with left child
                temp = heap[i]
                heap[i] = heap[2 * i + 1]
                heap[2 * i + 1] = temp
                return heap
        else:  # No swaps
            return heap

    def getPriorityParent(self, heap, i):
        """Function compares appearances of query
        in node and parent and returns priority list."""
        queries = self.query.lower().strip("\n").replace(".", "").replace(",", "").replace("(", "").replace(")", "") \
            .split(" ")  # Creates list for each word in query
        qCount = 0  # Initializes query counter for node
        qCountParent = 0  # Initializes query counter for parent
        for word in queries:  # For each individual word in user query input
            qCount += heap[i].getCount(word)  # Check number of appearances in node
            qCountParent += heap[(i - 1) // 2].getCount(word)  # Check number of appearances in parent
        pList = [qCount, qCountParent]  # List containing priority for node and parent
        return pList

    def getPriorityChildren(self, heap, i):
        """Function compares appearances of query in
        node and children and returns priority list."""
        queries = self.query.lower().strip("\n").replace(".", "").replace(",", "").replace("(", "").replace(")", "") \
            .split(" ")
        qCount = 0
        qCountLeftChild = 0  # Initializes query counter for left child
        qCountRightChild = 0  # Initializes query counter for right child
        for word in queries:
            qCount += heap[i].getCount(word)
            if (2 * i + 1) <= len(self.maxHeap) - 1:  # If left child exists
                qCountLeftChild += heap[2 * i + 1].getCount(word)  # Checks number of appearances in left child
            if (2 * i + 2) <= len(self.maxHeap) - 1:  # If right child exists
                qCountRightChild += heap[2 * i + 2].getCount(word)  # Check number of appearances in right child
        pList = [qCount, qCountLeftChild, qCountRightChild]  # List containing priority for node and children
        return pList

    def peek(self):
        """Function returns the WebpageIndex with
        the highest priority in the maxheap."""
        return self.maxHeap[0]  # Root node is the highest priority

    def poll(self):
        """Function removes and returns the WebpageIndex
        with the highest priority in the maxheap."""
        if len(self.maxHeap) == 0:  # If maxheap is empty return error
            print("Error: Heap is Empty.")

        elif len(self.maxHeap) == 1:  # If maxheap len = 1 delete root and return value
            val = self.maxHeap[0]
            del self.maxHeap[0]
            return val

        else:
            val = self.maxHeap[0]  # Holds value of root
            self.maxHeap[0] = self.maxHeap[-1]  # Swap bottom most node with root
            del self.maxHeap[-1]  # Delete bottom most node
            for i in range(len(self.maxHeap) - 1):  # For each index value in list
                self.heapSortDown(self.maxHeap, i)  # Sifting down
            return val  # Return highest priority value

    def reheap(self, query):
        """Function takes a new query as input and reheaps
        priority values based on new query."""
        self.query = query  # New query
        for i in range(len(self.maxHeap) - 1, -1, -1):  # Begins from the last value
            if i != 0:
                self.heapSortUp(self.maxHeap, i)  # Raising highest priority node up

        for i in range(len(self.maxHeap) - 1):  # Begins from the first value
            self.heapSortDown(self.maxHeap, i)  # Sifting down

    def printHeap(self):
        """Function prints filename of each node in
        the maxheap that matches query."""
        order = []
        for i in range(len(self.maxHeap) - 1):  # Begins from the first value
            p = self.getPriorityChildren(self.maxHeap, i)  # Checks priority level
            if p[0] > 0:  # If query appears more than 0 times
                order.append(p[0])  # Appending priority value to list
                order.append(self.maxHeap[i].getFile())  # Appending file name
        for i in range(0, len(order)-1, 2):  # Checking ever priority value
            for j in range(len(order)-1):
                if i+(2*j) <= len(order)-1:  # If value is not out of range
                    if order[i] < order[i+(2*j)]:  # Swaps in order from most to least
                        temp = order[i+(2*j)]
                        order[i+(2*j)] = order[i]
                        order[i] = temp
                        temp0 = order[i + (2 * j)+1] # Swaps file names in order
                        order[i + (2 * j)+1] = order[i+1]
                        order[i+1] = temp0

        for i in range(len(order)-1): # Printing matching files in order
            print(order[i])
        print(order[-1])





