from edge_server import EdgeCluster, EdgeServer
from numpy import random


mapRegion = {
    'e1': 'http://10.0.1.1:30001',
    'e2': 'http://10.0.1.1:30001',
    'e3': 'http://10.0.1.1:30001',
    'e4': 'http://10.0.1.1:30001',
    'e5': 'http://10.0.1.2:30001',
    'e6': 'http://10.0.1.2:30001',
    'e7': 'http://10.0.1.2:30001',
    'e8': 'http://10.0.1.2:30001',
    'e9': 'http://10.0.1.3:30001',
    'e10': 'http://10.0.1.3:30001',
    'e11': 'http://10.0.1.3:30001',
    'e12': 'http://10.0.1.3:30001',
}
    

class Selector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.clusters = []
            cls._instance.sessions = {}
            cls._instance.videosMap = {}
            cls._instance.usersMap = {}
            
        return cls._instance


    def add_cluster(self, kubeconfig):
        cluster = EdgeCluster(kubeconfig)
        self.clusters.append(cluster)
        

    def add_server_to_cluster(self, cluster_index, capacity, uri, weight=1):
        if cluster_index < len(self.clusters):
            self.clusters[cluster_index].add_server(capacity, uri, weight)


    def add_server(self, capacity, uri, weight=1):
        server = EdgeServer(capacity, uri)
        server.weight = weight
        self.servers.append(server)


    def get_next_available_server(self, cluster):
        num_servers = len(cluster.servers)
        total_weight = sum(server.weight for server in cluster.servers)
        
        current_server_index = cluster.current_server_index
        
        for _ in range(num_servers):
            server = cluster.servers[current_server_index]
            
            if server.is_available():
                cluster.current_server_index = current_server_index
                
                return server
                
            current_server_index = (current_server_index + 1) % num_servers
        
        return None


    def RequestRoutingProblem(self, userid, **kwargs):
        if userid in self.sessions:
            return self.sessions[userid]
                
        server = self.RegionAware(**kwargs)

        server.serve_request()
        self.sessions[userid] = server

        return server


    def SingleServer(self):
        return self.clusters.servers[0]


    def FirstFitProblem(self) -> object:
        for cluster in self.clusters:
            server = self.get_next_available_server(cluster)
            if server:
                return server
        
        return None

    def RegionAware(self, **kwargs) -> object:
        if kwargs['add'] not in self.usersMap:
            return self.ContentAwareRoundRobinBalancer(**kwargs)
            
        region_edge_server = mapRegion[self.usersMap[kwargs['add']]['bsName']]

        print(region_edge_server)

        for cluster in self.clusters:

            num_servers = len(cluster.servers)
            
            for i in range(num_servers):
                if cluster.servers[i].uri == region_edge_server and cluster.servers[i].is_available():
                    return cluster.servers[i]
        
        return None


    def ContentAwareRoundRobinBalancer(self, **kwargs) -> object:
        
        if kwargs['vid'] in self.videosMap:
            return self.videosMap[kwargs['vid']]

        for cluster in self.clusters:

            num_servers = len(cluster.servers)
            current_server_index = cluster.current_server_index
            
            for _ in range(num_servers):
                server = cluster.servers[current_server_index]
                current_server_index = (current_server_index + 1) % num_servers

                if server.is_available():
                    cluster.current_server_index = current_server_index
                    self.videosMap[kwargs['vid']] = server
                    return server
        
        return None


    def RoundRobinProblem(self, **kwargs) -> object:
        for cluster in self.clusters:

            num_servers = len(cluster.servers)
            current_server_index = cluster.current_server_index
            
            for _ in range(num_servers):
                server = cluster.servers[current_server_index]        
                current_server_index = (current_server_index + 1) % num_servers

                if server.is_available():
                    cluster.current_server_index = current_server_index
                    return server
        
        return None


    def RandomProblem(self, **kwargs) -> object:
        for cluster in self.clusters:
            return random.choice(cluster.servers)
        
        return None


    def release_request(self, server):
        server.release_request()


    def release_requests(self):
        for cluster in self.clusters:
            for server in cluster.servers:
                server.current_load = 0

            cluster.current_server_index = 0
            
        self.sessions.clear()
