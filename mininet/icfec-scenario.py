#!/usr/bin/python

"""Setting the position of nodes and providing mobility"""

from pyvirtualdisplay import Display

import yaml
import random
import argparse
import threading

from mininet.node import Controller, OVSKernelSwitch, Host
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.term import makeTerm
from mininet.util import irange, quietRun
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import OVSKernelAP

from yaml.loader import SafeLoader
from typing import Dict, Union
from time import sleep

from utils import zipf_selection  
from monitoring import Monitoring


def create_parser():
    arg_parser = argparse.ArgumentParser(description="Simulation")

    arg_parser.add_argument("--seed", type=int, default=0)
    arg_parser.add_argument("--users", type=int, default=0)
    arg_parser.add_argument("--abr", type=str, default="abrDynamic")
    arg_parser.add_argument("--edge_config", type=str, default="edge-nodes/edge_nodes_config.yml")
    arg_parser.add_argument("--users_config", type=str, default="users/end_users_config.yml")
    arg_parser.add_argument("--scenario_config", type=str, default="icc_scenario_config.yml")
    arg_parser.add_argument("--endpoints", type=str, default="143.106.73.17:30001,143.106.73.50:30002")

    return arg_parser


def validate_args(arguments: Dict[str, Union[int, str, None]]) -> bool:
    raise NotImplemented("Function not implementesd yet")


def thread_function(sta, args, v, b):
    sta.cmd(f'python users/run-player-icc.py --abr={args.abr} --user={sta.name} --video={v} --bitratemax={b} --seed={args.seed}')


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    rep = [
        3000,
        5800,
        7500,
        12000,
        17000,
        22000,
        25000
    ]

    sts = []
    bts = []
    svs = []
    sws = []
    links = []
    
    """Create a network."""
    # Select TCP Reno
    output = quietRun( 'sysctl -w net.ipv4.tcp_congestion_control=reno' )
    assert 'reno' in output
    
    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/16',
                       ac_method='ssf')


    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6653)

    with open(args.scenario_config) as f:
        topology = yaml.load(f, Loader=SafeLoader)

        info("*** Creating nodes topology\n")
        kwargs = {'mode': 'g', 'failMode': 'standalone', 'channel': '1'}

        svs.extend([ net.addHost(cls=Host, **edge) for edge in topology['servers'] ])
        bts.extend([ net.addAccessPoint(cls=OVSKernelAP, **{**bt, **kwargs}) for bt in topology['base_stations'] ])
        sws.extend([ net.addSwitch(f'sw{i}', cls=OVSKernelSwitch) for i in range(1, len(bts)+1) ])

        info('*** Configuring Users Stations\n')
        positions = [ 
            f'{random.randint(250,1750)},{random.randint(300,1750)},0' for _ in range(args.users)
         ]
        
        users = [{
            'name': 'sta%d' % i,
            'mac' : '00:00:00:00:00:%02d' % i,
            'ip'  : '10.0.0.%d/16' % i,
            'position': pos
        } for i, pos in enumerate(positions, 1)]
        
        sts.extend([ net.addStation(**user) for user in users ])


    info('*** Configuring Content Steering Service\n')
    steering = net.addHost('steering',  cls=Host, ip='10.0.1.50/16')


    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.6)


    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()


    info('*** Configuring Links\n')
    net.addLink(steering, sws[0])

    links.extend([ net.addLink(sw, sv) for sw, sv in zip(sws, svs) ])
    links.extend([ net.addLink(sw, bt) for sw, bt in zip(sws, bts) ])

    last = None
    for sw in sws:
        if last: net.addLink(last, sw, cls=TCLink)
        last = sw


    net.plotGraph(max_x=2000, max_y=2000)

    info( '*** Starting network\n')
    net.build()
    net.addNAT().configDefault()
    
    c0.start()
    for bt in bts: bt.start([ c0 ])
    for sw in sws: sw.start([ c0 ])

    makeTerm(steering, cmd='python steering/app.py')
    # for svr in svs:
    #     makeTerm(svr, cmd=f'python edge-nodes/cache-service/app.py --name={svr.name}')

    mon = Monitoring(net.stations, args.seed)
    mon.start()

    # Example usage
    bitrate = [random.choice(rep) for _ in range(len(sts))]
    videos = [ i for i in range(1, 11) ]
    random.shuffle(videos)
    random.shuffle(sts)

    alpha = 0.7  # Adjust this parameter to control the skewness of the Zipf distribution
    elements = zipf_selection(videos, alpha, len(sts))


    for sta, v, b in zip(sts, elements, bitrate):
        sleep(2)
        makeTerm(sta, cmd=f'python users/run-player-icfec.py --abr={args.abr} --user={sta.name} --video={v} --bitratemax={b} --seed={args.seed}')



    # mon.join()
     CLI(net)

    info("*** Stopping network\n")
    net.stop()
    mon.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()


