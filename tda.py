class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def remove(self, data):
        current = self.head
        previous = None
        while current is not None:
            if current.data == data:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                self._size -= 1
                return True
            previous = current
            current = current.next
        return False

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return temp.data

    def peek(self):
        return self.front.data if self.front else None

    def is_empty(self):
        return self.front is None

    def __iter__(self):
        current = self.front
        while current:
            yield current.data
            current = current.next

    def size(self):
        return self._size