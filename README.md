# AVENUE

**Abstract**: *One key challenge in Adaptive Video Streaming is the ever-changing edge network conditions at the final mile of access networks. The edge environment is particularly dynamic, influenced by user locations, fluctuation on resource demands and resource capabilities, in contrast to traditional Content Delivery Network (CDN) setups, where content routing deci- sions are relatively known. To address the dynamism of edge computing environments and to enable applications to exploit edge-cloud computing resources better, this article focuses on content steering technology, a recent addition to adaptive video protocols like HLS and DASH. We present AVENUE as an architecture for Content Steering Service to orchestrate video delivery dynamically within the Edge-Cloud Continuum. This work designs the principles of the Content Steering Service to create a mechanism that involves two integral modules - monitoring and selector. The monitoring module captures real- time context metrics, and the selector module chooses an edge server according to the Select Server Algorithm. Our study addresses three steering algorithms with distinct performance profiles. Numerical results show that different configurations may present distinct network performance in terms of Quality of Experience (QoE), Cache hits, and Request loads. Moreover, a correct choice of heuristics in the Selector module may also result in large differences depending on the metric evaluated.*


## Parameters:
- `--seed`: Seed
- `--users`: Total number of users
- `--abr`: Target ABR decision logic in dash.js. 
- `--users_config`: Users config
- `--scenario_config`: Scenarios config
- `--endpoints`: endpoints which videos are availables

It is important to generate new images for the Users, Video Edge Nodes and CDNs with the Dockerfile from the directories.


## How to run
```shell
python mininet/icfec-scenario.py --seed=<number of seed> --users=<# users>
```

