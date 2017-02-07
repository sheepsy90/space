class CompleteMissionAO():

    def __init__(self, mission_instance, basic_reward_text, death=False):
        self.mission_name = mission_instance.referenced_mission.name
        self.basic_reward_text = basic_reward_text
        self.death = death

    def add_event_reward_list(self, lst):
        self.event_reward_list = lst