import threading
import jsonrpclib


class EventServiceClient(object):

    def __init__(self, host, port):
        # Build up the connection
        self.service = jsonrpclib.Server('http://%s:%i' % (host, port))
        self.lock = threading.Lock()
        # Test with a Ping
        result = self.service.ping("1")
        # Check if this works
        if result != '1':
            exit(1)
        # Logging that we are up and running
        print "[GameServerClient] Up and running!"

    def prepare_mission_events(self,  mission_id, tags, probabilities, duration, difficulty):
        self.lock.acquire()
        result = self.service.prepare_mission_events(mission_id, tags, probabilities, duration, difficulty)
        self.lock.release()
        return result

    def get_events_up_to_this_point(self, mission_id):
        self.lock.acquire()
        result = self.service.get_events_up_to_this_point(mission_id)
        self.lock.release()
        return result

    def is_event_prevented(self, mission_id, event_id):
        self.lock.acquire()
        result = self.service.is_event_prevented(mission_id, event_id)
        self.lock.release()
        return result

    def set_event_prevented(self, mission_id, event_id):
        self.lock.acquire()
        result = self.service.set_event_prevented(mission_id, event_id)
        self.lock.release()
        return result

    def get_event_needs(self, mission_id, event_id):
        self.lock.acquire()
        result = self.service.get_event_needs(mission_id, event_id)
        self.lock.release()
        return result

    def remove_mission(self, mission_id):
        self.lock.acquire()
        result = self.service.remove_mission(mission_id)
        self.lock.release()
        return result

    def get_rewards_for_mission(self, mission_id):
        self.lock.acquire()
        result = self.service.get_rewards_for_mission(mission_id)
        self.lock.release()
        return result

    def get_events_with_rewards(self, mission_id):
        self.lock.acquire()
        result = self.service.get_events_with_rewards(mission_id)
        self.lock.release()
        return result

    def get_summed_up_event_consequences(self, mission_id, timestamp):
        self.lock.acquire()
        result = self.service.get_summed_up_event_consequences(mission_id, timestamp)
        self.lock.release()
        return result

    def get_number_missions(self):
        self.lock.acquire()
        result = self.service.get_number_missions()
        self.lock.release()
        return result