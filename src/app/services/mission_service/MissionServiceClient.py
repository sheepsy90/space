import threading
import jsonrpclib


class MissionServiceClient(object):

    def __init__(self, host, port_list):
        print "CONNECTING"
        # Build up the connection
        self.services = [jsonrpclib.Server('http://%s:%i' % (host, port)) for port in port_list]
        # Test with a Ping
        self.locks = [threading.Lock() for i in range(len(self.services))]

        for service in self.services:
            result = service.ping("1")
            # Check if this works
            if result != '1':
                exit(1)
        # Logging that we are up and running
        print "[GameServerClient] Up and running!"

    def determine_service_and_lock(self, mission_id):
        length = len(self.services)
        index = mission_id % length
        return self.services[index], self.locks[index]

    def add_mission(self, mission_id):
        service, lock = self.determine_service_and_lock(mission_id)
        lock.acquire()
        result = service.add_mission(mission_id)
        lock.release()
        return result

    def put_user_with_skills_to_mission(self, mission_id, user_ids, user_skills):
        service, lock = self.determine_service_and_lock(mission_id)
        lock.acquire()
        result = service.put_user_with_skills_to_mission(mission_id, user_ids, user_skills)
        lock.release()
        return result

    def get_remaining_action_points_for_user(self, mission_id, user_id):
        service, lock = self.determine_service_and_lock(mission_id)
        lock.acquire()
        result = service.get_remaining_action_points_for_user(mission_id, user_id)
        lock.release()
        return result

    def has_user_enough_action_points(self, mission_id, user_id, need_pairs):
        service, lock = self.determine_service_and_lock(mission_id)
        lock.acquire()
        result = service.has_user_enough_action_points(mission_id, user_id, need_pairs)
        lock.release()
        return result

    def reduce_users_action_points(self, mission_id, user_id, need_pairs):
        service, lock = self.determine_service_and_lock(mission_id)
        lock.acquire()
        result = service.reduce_users_action_points(mission_id, user_id, need_pairs)
        lock.release()
        return result

    def remove_mission(self, mission_id):
        service, lock = self.determine_service_and_lock(mission_id)
        lock.acquire()
        result = service.remove_mission(mission_id)
        lock.release()
        return result

