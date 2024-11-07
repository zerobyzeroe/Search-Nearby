class Node:
    def __init__(self, point):
        self.point = tuple(point)
        self.leftChild = None
        self.rightChild = None
        self.associatedStructure = None


class PointDatabase:
    def __init__(self, pointlist):
        pointlist_x = sorted(pointlist)
        pointlist_y = sorted(pointlist, key=lambda y: y[1])
        self.root = self.RangeTree(pointlist_x, pointlist_y)

    
    def RangeTree(self, pointlist_x, pointlist_y):
        if not pointlist_x:
            return None
        
        #Partition points around median x-coordinate
        medianIdx = (len(pointlist_x)-1)//2
        median = pointlist_x[medianIdx][0]
        pointlist_x_l = pointlist_x[:medianIdx]
        pointlist_x_r = pointlist_x[medianIdx+1:]

        # split list in Linear Time while maintaing ordering w.r.t. y
        pointlist_y_l = [y for y in pointlist_y if y[0] < median]
        pointlist_y_r = [y for y in pointlist_y if y[0] > median]

        #recurse on partitions
        leftChild = self.RangeTree(pointlist_x_l, pointlist_y_l)
        rightChild = self.RangeTree(pointlist_x_r, pointlist_y_r)

        root = Node(pointlist_x[medianIdx])
        root.leftChild = leftChild
        root.rightChild = rightChild
        root.associatedStructure = pointlist_y # Store a list of points in subtree sorted by y coordinate at each node
        return root

    #check whether the given node falls within desired range
    def within_bounds(self, node, q, d):
        x, y = node.point
        return max(abs(x-q[0]), abs(y-q[1])) < d

    #Binary search the least value greater than or equal to v in sorted pointlist
    def upper_bound(self, l, v):
        lo, hi = 0, len(l) - 1
        while lo <= hi:
            mid = (lo+hi)//2
            if l[mid][1] < v:
                lo = mid+1
            else:
                hi = mid-1
        return lo

    #Filter the list to contain all points satisfying ymin <= y < ymax
    def filter_list(self, l, q, d):
        ymin = q[1]-d
        ymax = q[1]+d
        return l[self.upper_bound(l, ymin):self.upper_bound(l, ymax)]
        
    #Main function for range queries
    def search_tree(self, node, q, d, lbound = float('-inf'), rbound = float('inf')):
        #Base case
        if not node:
            return []
        xmin, xmax = q[0]-d, q[0]+d
        x, y = node.point
        # print("Node", node.point, '\n', xmin, xmax, lbound, rbound)
        #If node's bounds lie within desired range, filter directly on y
        if lbound > xmin and rbound < xmax:
            # print("case 1\n")
            return self.filter_list(node.associatedStructure, q, d)
        #Go right
        elif x < xmin:
            # print("case 2\n")
            #Right subtree cannot contain points to the left of parent
            return self.search_tree(node.rightChild, q, d, x, rbound)
        #Go left
        elif x > xmax:
            # print("case 3\n")
            #Left subtree cannot contain points to the right of parent
            return self.search_tree(node.leftChild, q, d, lbound, x)
        #Must recurse on both subtrees
        else:
            # print("case 4\n")
            #Check whether parent lies in desired range
            points = [node.point] if self.within_bounds(node, q, d) else []
            points.extend(self.search_tree(node.leftChild, q, d, lbound, x))
            points.extend(self.search_tree(node.rightChild, q, d, x, rbound))
            return points

    #Search within whole tree
    def searchNearby(self, q, d):
        return self.search_tree(self.root, q, d) 

    
    # test
    # def inorder(self, root, list1):
    #     if root == None:
    #         return 
    #     self.inorder(root.leftChild, list1)
    #     list1.append([root.point])
    #     self.inorder(root.rightChild, list1)

    # def preorder(self, root, list1):
        
    #     if root == None:
    #         return 
    #     list1.append([root.point])
    #     self.preorder(root.leftChild, list1)
    #     self.preorder(root.rightChild, list1)




if __name__ == '__main__':
    obj =  PointDatabase([[1,6], [2,4], [3,7], [4,9], [5,1],  [7,8], [8,10], [9,2], [10,5],[10,12],[4,1],[9,4],[8,3]])
    # list1 = []
    # obj.inorder(obj.root, list1)
    # print(list1)

    # list1 = []
    # obj.preorder(obj.root, list1)
    # print(list1)
    print(obj.searchNearby((9,6), 3.5))