class FinishProgramAO():

    def __init__(self):
        self.list_of_rewards = []

    def add_reward(self, reward):
        self.list_of_rewards.append(reward)

    def set_description(self, desc):
        self.description = desc
