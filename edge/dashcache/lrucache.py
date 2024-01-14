import shutil
from collections import deque
from collections import OrderedDict

from cachecontrol.caches import FileCache


class LRUCache(object):

    def __init__(self, capacity: int, filecache: FileCache):
        self.capacity = capacity
        self.current_cap = 0
        self.container = deque()
        self.map = OrderedDict()
        self.item = str()

        self.filecache: FileCache = filecache

    def filecache_current_size(self) -> int:
        return len(self.map)

    def filecache_is_full(self) -> bool:
        return len(self.map) >= self.capacity
    
    def filecache_is_empty(self) -> bool:
        return len(self.map) == 0
    
    def filecache_pop(self) -> str:
        self.item, size = self.map.popitem(last=False)
        self.filecache.delete(self.item)
        self.current_cap -= size
        return "Removed:" + self.item

    def filecache_contains(self, item):
        return item in self.map

    def filecache_store_request(self, url: str, size: int, cache: bool) -> bool:
        self.current_cap += size if url not in self.map else 0
        self.map[url] = size
        self.map.move_to_end(url)

        while self.current_cap > self.capacity:
            self.item, size = self.map.popitem(last=False)
            self.current_cap -= size

            self.filecache.delete(self.item)

        return True
        
    def filecache_capacity(self, capacity: int) -> None:
        self.capacity = capacity

    def get_last_item(self) -> str:
        return self.item

    def close(self, name) -> None:
        print("Closing cache")
        shutil.rmtree(name)
