
from loguru import logger

class Item:
    def __init__(self, item_id=None, frame=None, parts=None):
        self.item_id = item_id
        self.parts = {}
        self.frame = frame
    
    def get_part(self, part_id):
        self.assert_contains(part_id)
        return self.parts[part_id]

    def get_part_set(self):
        return set(self.parts)

    def assert_contains(self, part_id):
        if part_id not in self.parts:
            raise Exception("No part {} in item {}".format(part_id, self.item_id))
    
    def update(self, frame=dict(), parts=dict()):
        part_set = set(self.parts)
        new_part_set = set(part_set)
        part_set.update(new_part_set)
        self.part = dict(part_set)
        self.frame = frame

class ItemContainer:
    def __init__(self, name=None):
        self.name = name
        self.items = dict()
        self.step = "idle"
        self.recent_item_id = NotImplemented
        self.part_set_server_needs = set()
        self.part_id_set_server_needs = set()
        self.server_frame = dict()
        self.frame_server_needs = dict()

    def assert_server_needs_are_same(self, frame_server_needs):
        diff = set(self.frame_server_needs) ^ set(frame_server_needs)
        if len(diff) != 0:
            raise Exception("expected frame server needs are {}, but frame server needs are {}"
        .format(self.frame_server_needs, frame_server_needs))

    def assert_not_contains(self, item_id):
        if item_id in self.items:
            raise Exception("{} aleady have item {}".format(self.name, item_id))

    def assert_contains(self, item_id):
        if item_id not in self.items:
            raise Exception("{} does not have item {}".format(self.name, item_id))

    def add(self, item:Item):
        self.assert_not_contains(item.item_id)
        self.items[item.item_id] = item

    def update(self, item_id, frame=dict(), parts=dict()):
        item = self.get_item(item_id)
        item.update(frame=frame, parts=parts)

    def get_item(self, item_id):
        self.assert_contains(item_id)
        return self.items[item_id]

    def get_diff_parts_ids(self, item_id, frame=dict()):
        item = self.get_item(item_id)
        frame_diff_set = set(frame) - set(item.frame)
        return dict(frame_diff_set)
    
    def get_item_nodes(self, item_id):
        pass

    def update_step(self, step):
        self.step = step

    def get_parts(self, item_id, part_ids:set) -> set:
        item = self.get_item(item_id)
        parts = {}
        
        for part_id in part_ids:
            parts[part_id] = item.get_part(part_id)
        
        return set(parts)
        
    def assert_step(self, step):
        if step != self.step:
            raise Exception("{}'s expected step is {}, but current step is {}".format(self.name, step, self.step))



# note sync simulator
class Simulator:
    def __init__(self, event_folder_path):
        self.event_folder_path = event_folder_path
        self.server = ItemContainer(name="server")
        self.clients = {}

    def simulate(self):
        pass
    
    def get_client(self, client_id) -> ItemContainer:
        if client_id not in self.clients:
            self.clients[client_id] = ItemContainer(name=client_id)
        return self.clients[client_id]

    def simulate_request_create_note(self, client_id, item:Item):
        logger.info("simulate_request_create_note")
        client = self.get_client(client_id)
        client.assert_step("idle")
        client.update_step("request_create_note")
        client.add(item)
        self.server.add(item)

    def simulate_response_create_note(self, client_id, item_server_id=None):
        logger.info("simulate_response_create_note")
        client = self.get_client(client_id)
        client.assert_step("request_create_note")
        client.update_step("idle")

    def simulate_request_frame_server_needs(self, client_id, item_id, frame=dict()):
        logger.info("simulate_request_frame_server_needs")
        client = self.get_client(client_id)
        client.assert_step("idle")
        client.update_step("request_part_id_set_server_needs")

    def simulate_response_part_id_set_server_needs(self, client_id, item_id, part_id_set_server_needs):
        logger.info("simulate_response_part_id_set_server_needs")
        client = self.get_client(client_id)
        client.assert_step("request_part_id_set_server_needs")
        client.update_step("response_part_id_set_server_needs")
        client.assert_part_id_set_server_needs(part_id_set_server_needs)
    

    def simulate_upload_parts_server_needs(self, client_id, item_id, frame=dict(), parts=dict()):
        logger.info("simulate_upload_parts_server_needs")
        client = self.get_client(client_id)
        client.assert_step(client_id, "response_parts_id_set_server_needs")
        client.update_step(client_id, "upload_parts_server_needs")
        self.assert_parts_server_needs(parts)
        self.server.update(item_id, frame=frame, parts=parts)
        client.update_step("idle")

    def assert_parts_server_needs(self, parts):
        expected_part_set_server_needs = self.server.get_part_set(self.part_id_set_server_needs)
        diff = expected_part_set_server_needs ^ part_set_server_needs
        if 0 < len(diff):
            raise Exception("expected parts server needs are different, expected = {}, actual = {}".format(expected_part_set_server_needs, part_set_server_needs))


    def simulate_request_download_client_needs(self, client_id, item_id, part_id_set:set):
        logger.info("simulate_request_download_client_needs")
        client = self.get_client(client_id)
        client.assert_step("idle")
        client.update_step("request_download_client_needs")
        
    def simulate_response_download_client_needs(self, client_id, item_id, frame=None, part_set=None):
        logger.info("simulate_response_download_client_needs")
        client = self.get_client(client_id)
        client.assert_step("request_download_client_needs")
        client.update_step("response_download_client_needs")



# Debug required