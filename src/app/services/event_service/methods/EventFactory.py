import random
import unittest
from services.event_service.methods.event_models import Event, EventReward, EventNeed, EventConsequence

RANDOM_EVENT_FACTOR = 0.05


class EventFactory():

    def __init__(self):
        self.dispatch_event_method = {
            1: self.generate_asteroid_event,
            2: self.generate_malfunction_event,
            3: self.generate_solarstorm_event,
            4: self.generate_injury_event,
            5: self.generate_pirates_event
        }
        self.event_tag_word_mapping = {
            1: ["Asteroid", "Comet", "Unknown Object"],
            2: ["Broken Generator", "Damaged Engine", "Leaky Oxygen Tank"],
            3: ["Electromagnetic Storm", "Gamma Ray", "Solar Storm"],
            4: ["Wound", "Broken Leg", "Cut", "Infection"],
            5: ["Pirates"]
        }
        self.event_difficulty_mapping = {
            1: ["Minor", "Light"],
            2: ["Medium", "Unusual"],
            3: ["Major", "Superior"]
        }

        self.event_nr = 0

    def get_and_raise_event_nr(self):
        a = self.event_nr
        self.event_nr += 1
        return a

    def generate_events(self, start, duration, tags, probabilities, difficulty):

        # First Part - Determine Number of Events
        fix_number = int(duration / 10)
        random_number = int(duration*RANDOM_EVENT_FACTOR*random.random())

        # The number of events
        number_of_events = fix_number + random_number

        # Calculate tag probabilities
        complete_probability = sum(probabilities)
        partial_probabilities = [(float(p)/complete_probability) for p in probabilities]

        # List of final events
        final_events = []

        # Cumulative Probability
        for index in range(number_of_events):
            index = self.get_index_for_cumulative_probability_list(partial_probabilities)
            tag_to_use = tags[index]
            final_events.append(self.generate_single_event_for_tag(tag_to_use, start, duration, difficulty))

        print final_events

        return final_events


    def get_index_for_cumulative_probability_list(self, lst):
        assert 1 - sum(lst) < 10E-5
        rand_nr = random.random()
        for i in range(len(lst)):
            rand_nr = rand_nr - lst[i]
            if rand_nr < 0:
                return i
        return len(lst)-1

    def generate_single_event_for_tag(self, tag_to_use, start, duration, difficulty):
        return self.dispatch_event_method[tag_to_use](tag_to_use, start, duration, difficulty)

    def get_occurrence_time(self, start, duration):
        return start + int(random.random()*duration*0.8 + duration*0.1)

    def get_description_string(self, difficulty, tag_to_use):
        word_list = self.event_tag_word_mapping[tag_to_use]
        difficulty = self.event_difficulty_mapping[difficulty]
        description = "%s %s" % (random.choice(difficulty), random.choice(word_list))
        return description

    def generate_asteroid_event(self, tag_to_use, start, duration, difficulty):
        occurrence = self.get_occurrence_time(start, duration)
        rew = EventReward(EventReward.XP, 5)
        description = self.get_description_string(difficulty, tag_to_use)

        e = Event(self.get_and_raise_event_nr(), "Asteroid Event", description, occurrence, 10, rew)
        e.add_need(EventNeed(EventNeed.NAVIGATION, 1))
        e.add_need(EventNeed(EventNeed.PHYSICS, 1))
        e.add_consequence(EventConsequence(EventConsequence.SHIP_DAMAGE, 5))
        e.add_consequence(EventConsequence(EventConsequence.CREW_DAMAGE, 5))
        return e

    def generate_malfunction_event(self, tag_to_use, start, duration, difficulty):
        occurrence = self.get_occurrence_time(start, duration)
        rew = EventReward(EventReward.XP, 5)
        description = self.get_description_string(difficulty, tag_to_use)

        e = Event(self.get_and_raise_event_nr(), "Malfunction Event", description, occurrence, 5, rew)
        e.add_need(EventNeed(EventNeed.ENGINEERING, 1))
        e.add_need(EventNeed(EventNeed.INFORMATICS, 1))
        e.add_consequence(EventConsequence(EventConsequence.SHIP_DAMAGE, 5))
        e.add_consequence(EventConsequence(EventConsequence.CREW_DAMAGE, 5))
        return e

    def generate_solarstorm_event(self, tag_to_use, start, duration, difficulty):
        occurrence = self.get_occurrence_time(start, duration)
        rew = EventReward(EventReward.XP, 5)
        description = self.get_description_string(difficulty, tag_to_use)

        e = Event(self.get_and_raise_event_nr(), "Solar Storm Event", description, occurrence, 7, rew)
        e.add_need(EventNeed(EventNeed.INFORMATICS, 1))
        e.add_need(EventNeed(EventNeed.ENGINEERING, 1))
        e.add_consequence(EventConsequence(EventConsequence.SHIP_DAMAGE, 5))
        e.add_consequence(EventConsequence(EventConsequence.CREW_DAMAGE, 5))
        return e

    def generate_injury_event(self, tag_to_use, start, duration, difficulty):
        occurrence = self.get_occurrence_time(start, duration)
        rew = EventReward(EventReward.XP, 5)
        description = self.get_description_string(difficulty, tag_to_use)

        e = Event(self.get_and_raise_event_nr(), "Injury Event", description, occurrence, 6, rew)
        e.add_need(EventNeed(EventNeed.MEDICAL, 1))
        e.add_need(EventNeed(EventNeed.BIOLOGY, 1))
        e.add_consequence(EventConsequence(EventConsequence.SHIP_DAMAGE, 5))
        e.add_consequence(EventConsequence(EventConsequence.CREW_DAMAGE, 5))
        return e

    def generate_pirates_event(self, tag_to_use, start, duration, difficulty):
        occurrence = self.get_occurrence_time(start, duration)
        rew = EventReward(EventReward.XP, 5)
        description = self.get_description_string(difficulty, tag_to_use)

        e = Event(self.get_and_raise_event_nr(), "Pirates Event", description, occurrence, 5, rew)
        e.add_need(EventNeed(EventNeed.NAVIGATION, 1))
        e.add_need(EventNeed(EventNeed.ENGINEERING, 1))
        e.add_consequence(EventConsequence(EventConsequence.SHIP_DAMAGE, 5))
        e.add_consequence(EventConsequence(EventConsequence.CREW_DAMAGE, 5))
        e.add_need(EventNeed(EventNeed.CHEMISTRY, 1))
        return e

class EventFactoryTest(unittest.TestCase):

    def test_index_for_cumulative_list_works(self):
        ef = EventFactory()

        lst = [0.1, 0.2, 0.3, 0.4]
        res = [0, 0, 0, 0]
        for i in range(10000):
            j = ef.get_index_for_cumulative_probability_list(lst)
            res[j] += 1
        print res