
class min_heap():
    def __init__(self):
        self.heap = []
        self.map = {}
        self.size = 0

    def parent(self,i):
        return (i-1)//2
    
    def left_child(self,i):
        return 2*i + 1
    
    def right_child(self,i):
        return 2*i + 2
    
    def swap(self, i, j):
        aux = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = aux

        self.map[self.heap[i][1]] = i
        self.map[self.heap[i][1]] = j

    def min_heapify(self, node) -> None:
        l = self.left_child(node)
        r = self.right_child(node)

        if l >= self.size:
            return

        if r < self.size and self.heap[r] < self.heap[l]:
            smallest = r
        else:
            smallest = l
        
        if self.heap[smallest] < self.heap[node]:
            self.swap(node, smallest)
            self.min_heapify(smallest)
        
    def insert(self, element):
        print("element")
        print(element[1])
        self.heap.append(element)
        self.size += 1
        self.map[element[1]] = self.size - 1
        self.swap(self.size - 1, 0)

        self.min_heapify(0)

    def pop(self):
        print("pop")
        top = self.heap[0]
        
        if self.size > 1:
            self.heap[0] = self.heap.pop()
            self.map[self.heap[0][1]] = 0
        else:
            self.heap.pop()
        
        self.size -= 1
        self.map.pop(top[1])
        

        self.min_heapify(0)

        return top
    
    def decrease_key(self, element_rad, new_key):
        node = self.map[element_rad]
        if self.heap[node][0] > new_key:
            self.heap[node] = (new_key, element_rad)
            while node > 0 and self.heap[node] > self.heap[self.parent(node)]:
                self.swap(node, self.parent(node))

    def is_in(self, element_rad):
        return element_rad in self.map
