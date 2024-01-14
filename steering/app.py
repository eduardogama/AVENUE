#!/usr/bin/python3
# -*- coding: utf-8 -*-


########################################################################
# IMPORTS                                                             ##
########################################################################
import randomname
import logging
import json
import os

from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from kubernetes import client
from flask_cors import CORS, cross_origin
from prometheus_client import generate_latest
from timeit import default_timer as timer


from builder import Builder
from planner import Planner
from selector import Selector

from time import sleep

# DEFINES
########################################################################
STEERING_ADDR = os.environ.get('STEERING_ADDR')
STEERING_PORT = int(os.environ.get('STEERING_PORT'))
CONTENT_TYPE_LATEST = os.environ.get('CONTENT_TYPE_LATEST')



# Initialize Orchestrator and ServerSelector
_selector = Selector()
_planner = Planner(_selector)
_builder = Builder()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CLASSES.

class Main:

    def __init__(self):
        """
        """
        self.app = Flask(__name__)
        CORS(self.app)

        self.users = {}
        self.timer_req = 0.0
        self.timer_cnt = 0 
        self.message = {}
        self.message['VERSION'] = 1
        self.message['TTL'] = 10
        base_uri = f'http://{STEERING_ADDR}:{STEERING_PORT}'


        @self.app.route('/steering/<name>')
        @cross_origin()
        def do_remote_steering(name):                       
            uid = request.args.get('_DASH_uid', default=randomname.get_name(), type=str)
            vid = request.args.get('video', default='', type=str)

            uri = f'{base_uri}{request.path}?video={vid}&_DASH_uid={uid}'

            kwargs = {
                'uid': uid,
                'vid': vid,
                'add': request.remote_addr,
            }

            start = timer()
            edge = _selector.RequestRoutingProblem(uid, **kwargs)
            self.timer_req += timer() - start
            self.timer_cnt += 1

            data = _builder.build(self.message, edge, uri, uid)
            return jsonify(data)

            
        @self.app.route("/statistics")
        def requests_statistics_lo() -> Response:
        
            round = request.args.get('round', default='0', type=int)
        
            statistics = "timestamp\n"
            statistics += self.timer_req/self.timer_cnt
            
            return Response(statistics, mimetype=CONTENT_TYPE_LATEST)

        
        @self.app.route('/releaseServers')
        def do_releaseServers():
            _selector.release_requests()
            logger.info('Released servers')
            return Response(
                "ok",
                status=200
            )


        @self.app.route('/collect/handover', methods=['POST'])
        def do_handover_info():
            params = request.get_json()
            
            user = {
                'userName': params['userName'],
                'bsName': params['bsName'],
                'ip': params['ip'],
                'rssi': params['rssi'],
            }

            _selector.usersMap[params['ip']] = user

            return Response(
                "ok", 
                status=200,
                headers={
                    'Access-Control-Allow-Origin': '*',
                }
            )
        

        @self.app.route('/trigger/<trigger>', methods=['POST'])
        def get_trigger(trigger):
            
            params = request.get_json()
            logger.info(f'Received trigger {trigger} request with params: {params}')
            return Response(status=204)

        @self.app.route('/metrics', methods=['GET'])
        def do_metric():
            return Response("", mimetype=CONTENT_TYPE_LATEST)


    def run(self):
        self.app.run(host=STEERING_ADDR, port=STEERING_PORT, debug=True)

# END CLASS.


# MAIN
#################################################
if __name__ == '__main__':
    main = Main()
    main.run()
# EOF
