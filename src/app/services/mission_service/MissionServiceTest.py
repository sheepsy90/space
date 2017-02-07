import unittest
import thread
import time

from services.mission_service.MissionServiceClient import MissionServiceClient
from services.mission_service.MissionService import MissionService

service = None


class MissionServiceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        thread.start_new_thread(MissionService, ("localhost", 55555))
        time.sleep(1)

    def test_at_three_added_mission_ids_available_missions_list_length_is_three(self):
        gsc = MissionServiceClient("localhost", [55555])
        gsc.add_mission(1)
        gsc.add_mission(2)
        gsc.add_mission(3)

        present_missions = gsc.services[0].get_available_mission()

        self.assertEqual(len(present_missions), 3)
