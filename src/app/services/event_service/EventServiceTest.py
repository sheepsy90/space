import unittest
import thread
import time
from services.event_service.EventService import EventService
from services.event_service.EventServiceClient import EventServiceClient
from services.event_service.methods.event_models import Event, EventConsequence

service = None

class EventMethodInjector():

    def __init__(self):
        pass

    def inject(self, obj):
        self.obj = obj

    def get_obj(self):
        return self.obj


emi = EventMethodInjector()


class EventServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        thread.start_new_thread(EventService, ("localhost", 55555, True, emi))
        time.sleep(1)

    def test_returns_right_consequences(self):
        ### Setup
        event_list = []
        e1 = Event(1, "Event 1", "Description", 5, 5, None)
        e2 = Event(1, "Event 1", "Description", 5, 5, None)
        e3 = Event(1, "Event 1", "Description", 5, 5, None)
        e1.add_consequence(EventConsequence(EventConsequence.SHIP_DAMAGE, 5))
        e1.add_consequence(EventConsequence(EventConsequence.SHIP_DAMAGE, 5))
        e2.add_consequence(EventConsequence(EventConsequence.CREW_DAMAGE, 5))
        e3.add_consequence(EventConsequence(EventConsequence.CREW_DAMAGE, 10))
        event_list.append(e1)
        event_list.append(e2)
        event_list.append(e3)
        emi.get_obj().storage[2] = {
            "events": event_list,
            "event_mapping": {e.id: e for e in event_list},
            "start_time": 0,
            "duration": 20
        }

        gsc = EventServiceClient("localhost", 55555)

        result = gsc.get_summed_up_event_consequences(2, 15)

        print result

        self.assertEqual(10, result[EventConsequence.SHIP_DAMAGE])
        self.assertEqual(15, result[EventConsequence.CREW_DAMAGE])

        del emi.get_obj().storage[2]

        self.assertEquals(0, gsc.get_number_missions())