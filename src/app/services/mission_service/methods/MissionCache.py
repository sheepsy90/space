__author__ = 'sheepy'


class MissionCache():

    def __init__(self):
        self.mission_cache = {}

    def add_mission(self, mission_id):
        self.mission_cache[mission_id] = {}
        print "Added Mission with id %i" % mission_id
        return True

    def get_available_mission(self):
        return self.mission_cache.keys()

    def remove_mission(self, mission_id):
        del self.mission_cache[mission_id]
        return True

    def put_user_with_skills_to_mission(self, mission_id, user_id, initial_skills):
        """ This method is sued to put the skills at mission start in """
        assert mission_id in self.mission_cache
        assert user_id not in self.mission_cache[mission_id]

        self.mission_cache[mission_id][user_id] = initial_skills
        print "Put into mission " + str(mission_id) + " user with id " + str(user_id) + " and skills " + str(initial_skills)
        return True

    def get_remaining_action_points_for_user(self, mission_id, user_id):
        print "Returning Remaining action Points for " + str(mission_id) + " on user " + str(user_id)
        assert mission_id in self.mission_cache
        assert user_id in self.mission_cache[mission_id]
        result = self.mission_cache[mission_id][user_id]
        return result

    def has_user_enough_action_points(self, mission_id, user_id, need_pairs):
        assert mission_id in self.mission_cache
        assert user_id in self.mission_cache[mission_id]
        for element in need_pairs:
            skill_id, amount = element
            skill_id = str(skill_id)
            assert skill_id in self.mission_cache[mission_id][user_id]
            if self.mission_cache[mission_id][user_id][skill_id] < amount:
                return False
        return True

    def reduce_users_action_points(self, mission_id, user_id, need_pairs):
        assert mission_id in self.mission_cache
        assert user_id in self.mission_cache[mission_id]
        for element in need_pairs:
            skill_id, amount = element
            skill_id = str(skill_id)
            assert skill_id in self.mission_cache[mission_id][user_id]
            self.mission_cache[mission_id][user_id][skill_id] -= amount
        return True