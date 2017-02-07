import time
from services.event_service.methods.EventFactory import EventFactory
from services.event_service.methods.event_models import EventConsequence


class EventServiceMethods():

    def __init__(self):
        self.storage = {}
        self.event_factory = EventFactory()

    def log(self, msg):
        print "[EventServiceMethods] " + msg

    def get_number_missions(self):
        return len(self.storage)

    def prepare_mission_events(self, mission_id, tags, probabilities, duration, difficulty):
        """ This method is callable via the JSON RPC """
        assert difficulty in [1, 2, 3]
        assert len(probabilities) == len(tags)
        assert duration > 0

        self.log("Mission Started - Id: " + str(mission_id))

        start_time = time.time()
        event_list = self.event_factory.generate_events(start_time, duration, tags, probabilities, difficulty)

        self.storage[mission_id] = {"events": event_list, "event_mapping": {e.id: e for e in event_list}, "start_time": start_time, "duration": duration}
        return True

    def remove_mission(self, mission_id):
        """ Service Method """
        assert mission_id in self.storage
        del self.storage[mission_id]
        return True

    def get_events_up_to_this_point(self, mission_id):
        current_time = time.time()
        return self.get_events_up_to_this_point_with_current_time(mission_id, current_time)

    def get_events_up_to_this_point_with_current_time(self, mission_id, current_time):
        if mission_id not in self.storage:
            return False
        start_time = self.storage[mission_id]["start_time"]
        # Filter out events that are not occurred by now
        # TODO - Filter out those that are no longer needed
        events = [e for e in self.storage[mission_id]["events"] if e.occurrence <= current_time]
        print "Would give", events
        return [{"id": e.id,
                 "name": e.name,
                 "desc": e.desc,
                 "act_time": e.act_time,
                 "event_happened": current_time > (e.act_time + e.occurrence),
                 "event_prevented": e.event_prevented,
                 "event_remain_time": max(0, int((e.act_time + e.occurrence) - current_time)),
                 "occurred": (e.occurrence - start_time),
                 "needs": [{"id": need.category_id, "amount": need.amount} for need in e.needs]
                    } for e in events]


    def is_event_prevented(self, mission_id, event_id):
        """ Service Method """
        return self.storage[mission_id]["event_mapping"][event_id].event_prevented

    def set_event_prevented(self, mission_id, event_id):
        """ Service Method """
        self.storage[mission_id]["event_mapping"][event_id].event_prevented = True
        return True

    def get_event_needs(self, mission_id, event_id):
        """ Service Method """
        event = self.storage[mission_id]["event_mapping"][event_id]
        return [[en.category_id, en.amount] for en in event.needs]

    def get_rewards_for_mission(self, mission_id):
        """ Service Method """
        money = 0
        xp = 0

        for e in self.storage[mission_id]["events"]:
            if e.reward.reward_type == "money":
                money += e.reward.reward_amount
            elif e.reward.reward_type == "xp":
                xp += e.reward.reward_amount

        return {"money": money, "xp": xp}

    def get_events_with_rewards(self, mission_id):
        """ Service Method """
        ev_wt_rew = [{"name": e.name, "reward_amount": e.reward.reward_amount, "achieved": e.event_prevented, "reward_type": e.reward.reward_type, "reward_text": "You got extra money!"} for e in self.storage[mission_id]["events"]]
        return ev_wt_rew


    def get_summed_up_event_consequences(self, mission_id, current_time):
        events = [e for e in self.storage[mission_id]["events"] if e.occurrence <= current_time and not e.event_prevented]
        event_consequence = {}
        for e in events:
            for k in e.consequences:
                if k.consequence_type not in event_consequence:
                    event_consequence[k.consequence_type] = 0
                event_consequence[k.consequence_type] += k.amount

        death = False
        death = death or (EventConsequence.CREW_DAMAGE in event_consequence and event_consequence[EventConsequence.CREW_DAMAGE] >= 100)
        death = death or (EventConsequence.SHIP_DAMAGE in event_consequence and event_consequence[EventConsequence.SHIP_DAMAGE] >= 100)
        event_consequence["death"] = death

        return event_consequence