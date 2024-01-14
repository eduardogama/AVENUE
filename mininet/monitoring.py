import threading
import requests
import logging

import numpy as np

from time import sleep
from mininet.log import info


class Monitoring(threading.Thread):
    def __init__(self, stas, seed=0, round=200) -> None:
        super().__init__()
        
        self.seed = seed
        self.buffer = "{"
        self.round = round
        self.stas = stas
        self.exit_event = threading.Event()


    # Monitor the connectivity of the station
    def run(self):
        prev_ap = np.array([ None for i in enumerate(self.stas) ])
        
        for k in range(self.round):
            if self.exit_event.is_set():
                return
            
            for i, sta in enumerate(self.stas):
                conn_ap = sta.wintfs[0].ssid

                if conn_ap != prev_ap[i]:

                    user_data = {
                        "userName": sta.name,
                        "bsName": conn_ap,
                        "ip": sta.wintfs[0].ip,
                        "rssi": sta.wintfs[0].rssi
                    }
                    
                    res = requests.post('http://143.106.73.50:30700/collect/handover', json=user_data)
                    info(f'*** {res.status_code}, {user_data}\n')
                    self.buffer += f'{user_data},\n'
                    prev_ap[i] = conn_ap
                
            # print(2*k, end=' ', flush=True)
            sleep(2)

        self.buffer += "}"

        f = open(f'logs/{self.seed}/handover.log', "w")
        f.write(self.buffer)
        f.close()


    def stop(self):
        self.exit_event.set()