import requests
import logging
import re

class PrefetchingManager(object):
    log = logging.getLogger("PrefetchingManagerImpl")

    def __init__(self, cache):
        self.cache = cache

    def extractUrlInfo(self, url: str):
        # Extracting the resolution using regular expression
        resolution_match = re.search(r'(\d+x\d+)', url)
        resolution = resolution_match.group(1) if resolution_match else None

        # Extracting the representation using regular expression
        representation_match = re.search(r'_(\d+k)', url)
        representation = representation_match.group(1) if representation_match else None

        # Extracting the segment number using regular expression
        segment_match = re.search(r'_(\d+)\.', url)
        segment_number = segment_match.group(1) if segment_match else None

        return resolution, representation, int(segment_number)

    def changeSegmentNumber(self, string, new_segment_number):
        pattern = r'(?<=_)\d+(?=\.)'
        return re.sub(pattern, str(new_segment_number), string)

    def PrefetchingProblem(self, url: str, path: str):
        resolution, representation, segment_number = self.extractUrlInfo(url)

        print(resolution, representation, segment_number)
        self.LastSegmentQuality(path, segment_number+1)

    def LastSegmentQuality(self, path: str, segment_number: int):
        new_path = self.changeSegmentNumber(path, segment_number)

        if self.cacheCtrl.filecache_contains(new_path):
            return

        cloud_url = '{}{}'.format(self.endpoint, path)

        try:
            print(cloud_url)
            response = self.sessCtrl.get(cloud_url)

            if response.status_code == 200:
                self.cacheCtrl.filecache_store_request(new_path, len(response.content))

            print(self.cacheCtrl.filecache_contains(new_path))
        except Exception as e:
            print(e)



    def LastSegmentQualityPlus(self, resolution, representation, segment_number):
        index = representations.index(r'{resolution}_{representation}')

    def AllSegmentQuality(self, resolution, representation, segment_number):
        pass

    def update_buffer(self, position: float) -> None:
        pass
