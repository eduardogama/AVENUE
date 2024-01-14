class EdgeCluster:
    
    def __init__(self, kubeconfig, weight=1):
        self.name = ""
        self.kubeconfig = kubeconfig
        self.servers = []
        self.current_server_index = 0

    def add_server(self, capacity, uri, weight=1):
        server = EdgeServer(capacity, uri)
        server.weight = weight
        
        self.servers.append(server)


class EdgeServer:
    def __init__(self, capacity, uri, weight=1):
        self.uri = uri
        self.weight = weight
        self.capacity = capacity
        self.current_load = 0
        
    def is_available(self):
        return self.current_load < self.capacity

    def serve_request(self):
        if self.is_available():
            self.current_load += 1
            return True
        else:
            return False

