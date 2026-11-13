
from collections import deque


class Node:
    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.left: Node | None = None
        self.right: Node | None = None


class BinaryTree:
    def __init__(self):
        self.root = None
        self.nodes = {}
        self.parents = {}
        self.next_id = 0

    def create_root(self, data):
        if self.root is not None:
            return "Tree already has a root."

        node = Node(self.next_id, data)

        self.root = node
        self.nodes[node.id] = node
        self.next_id += 1

        return node

    def add(self, parent_id, data, side):
        parent = self.nodes.get(parent_id)

        if parent is None:
            return "Parent node does not exist."
        if side not in ("left", "right"):
            return "Invalid side."
        if getattr(parent, side) is not None:
            return f"The {side} child already exists."

        node = Node(self.next_id, data)

        setattr(parent, side, node)

        self.nodes[node.id] = node
        self.parents[node.id] = parent_id

        self.next_id += 1

        return node

    def delete(self, node_id):
        node = self.nodes.get(node_id)

        if node is None:
            return "Node does not exist."

        if node is self.root:
            self.root = None
            self.nodes.clear()
            self.parents.clear()
            self.next_id = 0
            return True

        parent = self.nodes[self.parents[node_id]]

        if parent.left is node:
            parent.left = None
        else:
            parent.right = None

        def remove_subtree(current):
            if current is None:
                return

            remove_subtree(current.left)
            remove_subtree(current.right)

            self.nodes.pop(current.id, None)
            self.parents.pop(current.id, None)

        remove_subtree(node)

        return True

    def traverse(self, method="inorder"):
        result = []

        def visit(node):
            result.append({
                "id": node.id,
                "data": node.data
            })

        def inorder(node):
            if node is None:
                return

            inorder(node.left)
            visit(node)
            inorder(node.right)

        def preorder(node):
            if node is None:
                return

            visit(node)
            preorder(node.left)
            preorder(node.right)

        def postorder(node):
            if node is None:
                return

            postorder(node.left)
            postorder(node.right)
            visit(node)

        methods = {
            "inorder": inorder,
            "preorder": preorder,
            "postorder": postorder,
        }

        if method not in methods:
            return "Invalid traversal method."

        methods[method](self.root)

        return result

    #turn into dict to send to js
    def to_dict(self):
        def serialize(node):
            if node is None:
                return None

            return {
                "id": node.id,
                "data": node.data,
                "left": serialize(node.left),
                "right": serialize(node.right)
            }

        return serialize(self.root)

    def to_state(self):
        return {
            "root": self.to_dict(),
            "next_id": self.next_id
        }

    #from website to python
    @classmethod
    def from_state(cls, state):
        tree = cls()

        if not state:
            return tree

        tree.next_id = state.get("next_id", 0)

        def deserialize(data, parent_id=None):
            if data is None:
                return None

            node = Node(data["id"], data["data"])

            tree.nodes[node.id] = node

            if parent_id is not None:
                tree.parents[node.id] = parent_id

            node.left = deserialize(data["left"], node.id)
            node.right = deserialize(data["right"], node.id)

            return node

        tree.root = deserialize(state.get("root"))

        return tree
