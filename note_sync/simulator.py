
class Server:
    def __init__(self):
        self.items = {}

class Client:
    def __init__(self):
        self.items = {}h

# note sync simulator
class Simulator:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.server = Server()
        self.clients = {}
    
    def simulate(self):
        pass

    def simulate_create_note(self, client_id, doc_info):
        
        pass

    def simulate_upload_partial_items(self, client_id, partial_items):
        pass

    def simulate_download_partial_items(self, clinet_id, partial_items):
        pass

    def simulate_ask_server_needs(self, client_id, client_frame):
        pass        