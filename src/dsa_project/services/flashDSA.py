class CardNode:
    def __init__(self, front, back):
        self.front = front
        self.back = back
        self.prev = None
        self.next = None

class Deck:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def node_at(self, index):
        current = self.head
        for _ in range(index):
            if not current:
                return None
            current = current.next
        return current

    def add_end(self, front, back):
        node = CardNode(front, back)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
        else:
            self.head = node
        self.tail = node
        self.count += 1

    def insert_after(self, index, front, back):
        current = self.node_at(index)
        if current is None:                      
            self.add_end(front, back)
            return
        
        node = CardNode(front, back)
        node.prev = current
        node.next = current.next

        if current.next:
            current.next.prev = node
        else:
            self.tail = node
        current.next = node
        self.count += 1

    def delete(self, index):
        current = self.node_at(index)

        if current is None:
            return
        
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next

        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
        self.count -= 1

    def to_list(self):
        items, current = [], self.head
        while current:
            items.append({"front": current.front, "back": current.back})
            current = current.next
        return items

def from_list(saved):
    deck = Deck()
    for c in saved:
        deck.add_end(c["front"], c["back"])
    return deck

def step(deck, index, direction):
    current = deck.node_at(index)
    if current is None:
        return 0
    if direction == "next" and current.next:
        return index + 1
    if direction == "prev" and current.prev:
        return index - 1
    return index