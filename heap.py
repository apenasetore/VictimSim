
class min_heap():
    def __init__(self):
        self.heap = []
        self.map = {}
        self.size = 0

    def parent(i):
        return (i-1)//2
    
    def left_child(i):
        return 2*i + 1
    
    def right_child(i):
        return 2*i + 2
    
    def swap(self, i, j):
        aux = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = aux

        self.map[self.heap[i][:-1]] = i
        self.map[self.heap[i][:-1]] = j

    def min_heapify(self, node) -> None:
        l = self.left_child(node)
        r = self.right_child(node)

        if l < self.size:
            return

        if r < self.size and self.heap[r] < self.heap[l]:
            smallest = r
        else:
            smallest = l
        
        if self.heap[smallest] < self.heap[node]:
            self.swap(node, smallest)
            self.min_heapify(smallest)
        
    def insert(self, element):
        self.heap.append(element)
        self.size += 1
        self.map[element[:-1]] = self.size - 1
        self.swap(self.size - 1, 0)

        self.min_heapify(0)

    def pop(self):
        top = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.size -= 1
        self.map.pop(top[:-1])
        self.map[self.heap[0][:-1]] = 0

        self.min_heapify(0)

        return top
    
    def decrease_key(self, element_rad, new_key):
        node = self.map[element_rad]

        self.heap[node] = (new_key) + element_rad

        while node > 0 and self.heap[node] > self.heap[self.parent(node)]:
            self.swap(node, self.parent(node))
    
    def is_in(self, element_rad):
        return element_rad in self.map
