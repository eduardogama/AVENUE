import os
import logging

from argparse import Namespace
from argparse import ArgumentParser
from multiprocessing import Pool

from flask import Flask
from flask import Response
from flask import request

from DiskLRUCache import DiskLRUCache
from prometheus_client import generate_latest, Gauge


# DEFINES
########################################################################
CACHE_ADDR = os.environ.get('CACHE_ADDR')
CACHE_PORT = int(os.environ.get('CACHE_PORT'))
CACHE_SIZE = 20000000 #int(os.environ.get('CACHE_SIZE'))
CONTENT_TYPE_LATEST = os.environ.get('CONTENT_TYPE_LATEST')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

#_pool: Pool = Pool(processes=1)

class Main:
    def __init__(self):
        """
        """
        parser = self.create_parser()
        args = parser.parse_args()
        
        self.name = args.name
        self.buffer = ''
        self.hit = [0, 0]
        self.cache = DiskLRUCache(max_size=CACHE_SIZE)
        
        self.app = Flask(__name__)
        
        @self.app.route('/<path:video>/<path:path>')
        def get_endpoint(video, path) -> Response:
            response, hit, status = self.cache.get(f'{video}/{path}', video)
            
            self.hit[hit] += 1
            self.buffer += f'{video}/{path}\n'

            return Response(
                response,
                status=status,
                headers={
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization'
                }
            )

        @self.app.route("/statistics")
        def requests_statistics() -> Response:
            statistics = "miss hit\n"
            statistics += f"{self.hit[0]} {self.hit[1]}\n"
            
            self.hit[0] = 0
            self.hit[1] = 0
            
            return Response(statistics, mimetype=CONTENT_TYPE_LATEST)
            
        @self.app.route("/statistics_lo")
        def requests_statistics_lo() -> Response:
        
            round = request.args.get('round', default='0', type=int)
        
            statistics = "miss hit\n"
            statistics += f"{self.hit[0]} {self.hit[1]}\n"
            
            statistics += self.buffer
            
            f = open(f'logs/{round}/{self.name}', 'a')
            f.write(statistics)
            f.close()

            self.hit[0] = 0
            self.hit[1] = 0
            
            self.buffer = ''
            
            return Response('OK', mimetype=CONTENT_TYPE_LATEST)

        @self.app.route("/metrics")
        def request_metrics() -> Response:
            return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
        
        @self.app.route("/reset")
        def reset_metrics() -> Response:
            res = ''
            while not self.cache.filecache_is_empty():
                res += f'{self.cache.filecache_pop()}\n'

            capacity = request.args.get('capacity', default=CACHE_SIZE, type=int)
            self.cache.filecache_capacity(capacity)

            res += f'Current capacity = {self.cache.max_size}\n'
            res += f'New Capacity = {capacity}\n'
            res += f'Current capacity = {self.cache.cur_size}\n'
            
            for key in self.buffer:
                res += f'{self.buffer} {self.buffer[key]}'
            
            self.buffer = ''
            self.cache.cur_size = 0
            
            return Response(res, mimetype=CONTENT_TYPE_LATEST)


    def run(self) -> None:
        self.app.run(host=CACHE_ADDR, port=CACHE_PORT, debug=True)


    def create_parser(self) -> Namespace:
        arg_parser = ArgumentParser(description="Cache Params")

        arg_parser.add_argument("--name", type=str, default="webcache")
        arg_parser.add_argument("--endpoint", type=str, default="143.106.73.50:30002")

        return arg_parser

# END CLASS.


# MAIN
#################################################
if __name__ == "__main__":
    main = Main()
    main.run()

# EOF

