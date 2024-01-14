import cachetools
import threading
import requests


_cdnMap = {
    '3DMark_Night_Raid': '143.106.73.44',
    '3DMark_Vantage': '143.106.73.44',
    'Ancient_Thought': '143.106.73.44',
    'Eldorado': '143.106.73.44',
    'Indoor_Soccer': '143.106.73.44',
    'Lifting_Off': '143.106.73.33',
    'Moment_of_Intensity': '143.106.73.33',
    'Seconds_That_Count': '143.106.73.33',
    'Skateboarding': '143.106.73.33',
    'Unspoken_Friend': '143.106.73.33',
}

class DiskLRUCache:
    def __init__(self, max_size=1000, cache_dir='./cache'):
        self.cur_size = 0
        self.max_size = max_size
        self.cache = cachetools.LRUCache(maxsize=self.max_size)
        self.lock = threading.Lock()

        self.session = requests.Session()

    def get(self, key, video):
        try:
            return self.cache[key], True, 200
        except KeyError:
            response = self.session.get(f'http://{_cdnMap[video]}:30001/{key}')
            self.put(key, response.content)

            return response.content, False, 200

    def put(self, key, value):
        self.cache[key] = value
        self.cur_size += len(value)

        if self.cur_size > self.max_size:
            self._spill_to_disk()

    def _spill_to_disk(self):
        while self.cur_size > self.max_size:
            key, value = self.cache.popitem()                
            self.cur_size -= len(value)

    def clear(self):
        self.cache.clear()
        self.cur_size = 0

    def filecache_capacity(self, capacity: int) -> None:
        self.max_size = capacity

    def filecache_is_empty(self):
        return len(self.cache) == 0
    
    def filecache_pop(self) -> str:
        key, value = self.cache.popitem()
        self.cur_size -= len(value)
        return "Removed:" + key
    
