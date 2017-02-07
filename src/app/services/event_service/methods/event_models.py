class Event(object):

    def __init__(self, id, name, desc, occurrence, act_time, reward):
        self.id = id
        self.name = name
        self.desc = desc
        self.occurrence = occurrence
        self.act_time = act_time
        self.event_prevented = False
        self.consequences = []
        self.needs = []
        self.reward = reward

    def add_consequence(self, consequence):
        self.consequences.append(consequence)

    def add_need(self, need):
        self.needs.append(need)

    def __str__(self):
        return self.name + str(self.occurrence)


class EventNeed(object):
    ENGINEERING = 1
    MEDICAL = 2
    NAVIGATION = 3
    BIOLOGY = 4
    PHYSICS = 5
    CHEMISTRY = 6
    INFORMATICS = 7
    GEOLOGY = 8

    def __init__(self, category_id, amount):
        self.category_id = category_id
        self.amount = amount


class EventConsequence():
    SHIP_DAMAGE = '0'
    CREW_DAMAGE = '1'

    def __init__(self, consequence_type, amount):
        self.consequence_type = consequence_type
        self.amount = amount

class EventReward(object):
    XP = "experience"
    MONEY = "money"

    def __init__(self, reward_type, reward_amount):
        self.reward_type = reward_type
        self.reward_amount = reward_amount
