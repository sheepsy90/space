from core.content import Missions, MissionTags, MissionTagsToMission, Planets
from lib.setup.GeneralSetup import GeneralSetup


class MissionsSetup(GeneralSetup):
    """ Comment """

    def __init__(self):

        self.MT_ASTEROIDS = MissionTags.objects.get(key="ASTEROIDS")
        self.MT_MALFUNCTION = MissionTags.objects.get(key="MALFUNCTION")
        self.MT_SOLAR_STORM = MissionTags.objects.get(key="SOLAR_STORM")
        self.MT_INJURY = MissionTags.objects.get(key="INJURY")
        self.MT_PIRATES = MissionTags.objects.get(key="PIRATES")

        self.EARTH = Planets.objects.get(name="Earth")
        self.MOON = Planets.objects.get(name="Moon")
        self.MARS = Planets.objects.get(name="Mars")
        self.PLUTO = Planets.objects.get(name="Pluto")
        self.GLIESE581d = Planets.objects.get(name="Gliese 581d")

    def setup(self):
        print "Creating Missions..."
        self.MISSION1 = self.save_and_get(Missions(name="Polar Expedition", reward_money=350,
                                                   planet=self.EARTH, target_planet=None,
                                                   basic_time=30, reward_xp=30, need_xp=0))

        MissionTagsToMission(mission=self.MISSION1, mt=self.MT_MALFUNCTION, probability=1).save()
        MissionTagsToMission(mission=self.MISSION1, mt=self.MT_INJURY, probability=5).save()


        self.MISSION2 = self.save_and_get(Missions(name="Mars Mission", reward_money=250,
                                                   planet=self.EARTH, target_planet=self.MARS,
                                                   basic_time=180, reward_xp=150, need_xp=200))

        MissionTagsToMission(mission=self.MISSION2, mt=self.MT_SOLAR_STORM, probability=5).save()
        MissionTagsToMission(mission=self.MISSION2, mt=self.MT_MALFUNCTION, probability=2).save()


        self.MISSION5 = self.save_and_get(Missions(name="Back to Earth", reward_money=250,
                                                   planet=self.MARS, target_planet=self.EARTH,
                                                   basic_time=180, reward_xp=150, need_xp=0))

        MissionTagsToMission(mission=self.MISSION5, mt=self.MT_SOLAR_STORM, probability=5).save()
        MissionTagsToMission(mission=self.MISSION5, mt=self.MT_MALFUNCTION, probability=2).save()


        self.MISSION3 = self.save_and_get(Missions(name="Exploring Mars", reward_money=250,
                                                   planet=self.MARS, target_planet=self.MARS,
                                                   basic_time=180, reward_xp=150, need_xp=50))

        MissionTagsToMission(mission=self.MISSION3, mt=self.MT_INJURY, probability=5).save()
        MissionTagsToMission(mission=self.MISSION3, mt=self.MT_MALFUNCTION, probability=2).save()

        self.MISSION4 = self.save_and_get(Missions(name="Journey to Pluto", reward_money=250,
                                                   planet=self.MARS, target_planet=self.PLUTO,
                                                   basic_time=180, reward_xp=150, need_xp=500))

        MissionTagsToMission(mission=self.MISSION4, mt=self.MT_INJURY, probability=5).save()
        MissionTagsToMission(mission=self.MISSION4, mt=self.MT_MALFUNCTION, probability=2).save()

        self.MISSION6 = self.save_and_get(Missions(name="Drill on Asteroid", reward_money=250,
                                                   planet=self.PLUTO, target_planet=None,
                                                   basic_time=180, reward_xp=150, need_xp=600))

        MissionTagsToMission(mission=self.MISSION6, mt=self.MT_INJURY, probability=5).save()
        MissionTagsToMission(mission=self.MISSION6, mt=self.MT_MALFUNCTION, probability=2).save()


        self.MISSION7 = self.save_and_get(Missions(name="Energy Harvesting", reward_money=250,
                                                   planet=self.EARTH, target_planet=None,
                                                   basic_time=180, reward_xp=150, need_xp=600))

        MissionTagsToMission(mission=self.MISSION7, mt=self.MT_INJURY, probability=5).save()
        MissionTagsToMission(mission=self.MISSION7, mt=self.MT_MALFUNCTION, probability=2).save()

        self.MISSION8 = self.save_and_get(Missions(name="Support ISS", reward_money=20,
                                                   planet=self.EARTH, target_planet=None,
                                                   basic_time=30, reward_xp=20, need_xp=600))

        MissionTagsToMission(mission=self.MISSION8, mt=self.MT_INJURY, probability=5).save()
        MissionTagsToMission(mission=self.MISSION8, mt=self.MT_MALFUNCTION, probability=2).save()