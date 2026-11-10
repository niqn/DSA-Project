class Node():
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.left = None
        self.right = None

#not done
def add(*args):
    if len(args) != 2:
        return "Input must be in the format of 'position', 'data'."
    
    parent, data = args
    #parent is a Node
    if parent.left != None and parent.right != None:
        node = Node(data, data)
    if parent.left == None:
        parent.left = node
    elif parent.right == None:
        parent.right = node
    else:
        return "A node can only have two children."

def delete():
    pass

def traverse():
    pass