"""
标题: LRU 缓存
描述: 请你设计并实现一个满足 LRU (最近最少使用) 缓存 约束的数据结构。
"""
class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dummy = Node()
        self.dummy.next = self.dummy
        self.dummy.prev = self.dummy
        self.map = {}

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._move_to_head(node)
        else:
            new_node = Node(key, value)
            self.map[key] = new_node
            self._add_to_head(new_node)
            if len(self.map) > self.capacity:
                removed = self._remove_tail()
                del self.map[removed.key]

    def _add_to_head(self, node):
        node.next = self.dummy.next
        node.prev = self.dummy
        self.dummy.next.prev = node
        self.dummy.next = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_head(self, node):
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self):
        node = self.dummy.prev
        self._remove_node(node)
        return node

if __name__ == "__main__":
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(lru.get(1))  # 1
    lru.put(3, 3)
    print(lru.get(2))  # -1
