class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class StudyQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.count = 0

    def enqueue(self, subj, mins):
        node = Node({"subject": subj, "minutes": mins})
        if self.rear is not None:
            self.rear.next = node
        else:
            self.front = node
        self.rear = node
        self.count +=1


    def dequeue(self):
        if self.front is None:
            return None
        
        node = self.front
        self.front = node.next
        if self.front is None:
            self.rear = None
        self.count -= 1
        return node.data

    def to_list(self):
        items, current = [], self.front
        while current:
            items.append(current.data)
            current = current.next
        return items

def from_list(saved):
    q = StudyQueue()
    for item in saved:
        q.enqueue(item["subject"], item["minutes"])
    return q


def with_schedule(items):
    total = 0
    result = []
    for item in items:
        result.append({**item, "starts_in": total})
        total += item["minutes"]
    return result, total