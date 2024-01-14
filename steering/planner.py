from selector import Selector


# CLASSES
###############################################################################
class Planner:

    """
    """

    def __init__(self, selector):
        
        self.selector = selector
    
        self.selector.add_cluster('k8s-configs/single-node')
        
        # Add edge servers with specific capacities
        self.selector.add_server_to_cluster(0, 50, 'http://10.0.1.1:30001')
        self.selector.add_server_to_cluster(0, 50, 'http://10.0.1.2:30001')
        self.selector.add_server_to_cluster(0, 50, 'http://10.0.1.3:30001')


    
# END CLASS.

