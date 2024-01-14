class Builder:
    def __init__(self):
        self.build_obj = None

        self.edge_nodes = {
            'http://10.0.1.1:30001': 'edge1',
            'http://10.0.1.2:30001': 'edge2',
            'http://10.0.1.3:30001': 'edge3',
            'http://143.106.73.50:30002': 'cloud'
        }


    def build(self, message, servers, uri, uid):
        
        json_data = message
        json_data["PATHWAY-PRIORITY"] = [self.edge_nodes[servers.uri]]
        json_data['RELOAD-URI'] = uri
#        json_data['PATHWAY-CLONES'] = [ 
#            {
#                'BASE-ID': 'edge1',
#                'ID': 'edge1-clone',
#                'URI-REPLACEMENT': {
#                    'HOST': 'http://127.0.0.1:30001',
#                    'PARAMS': {
#                        'ap1': '3.71',
#                        'ap2': '5'
#                    }
#                }
#            }
#        ]

        return json_data

