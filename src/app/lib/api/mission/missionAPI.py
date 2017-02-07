import time
from django.core.signals import request_started
from django.db import transaction
from core.content import Missions, MissionTagsToMission
from core.models import UserLocation, OpenMissions, MissionInstances, UserSkills, UserProperties
from lib.api.mission.CompleteMissionAO import CompleteMissionAO
from lib.api.user import userAPI
from services.event_service.EventServiceClient import EventServiceClient
from services.mission_service.MissionServiceClient import MissionServiceClient

__author__ = 'sheepy'

missionCache = MissionServiceClient("localhost", [8011])
eventService = EventServiceClient("localhost", 8001)


def get_possible_missions_for_player(user):

    user_planet = UserLocation.objects.get(user=user).current

    missions = [{"mission": m, "precondition_xp": can_user_join_mission(user, m) ,"tags": MissionTagsToMission.objects.filter(mission=m)} for m in Missions.objects.filter(planet=user_planet)]
    return missions


def user_participates_in_mission(user):
    return OpenMissions.objects.filter(user=user).exists()


def prepare_mission(user, mission_id):
    m = Missions.objects.get(id=mission_id)
    if can_user_join_mission(user, m):
        mi = MissionInstances(referenced_mission=m)
        mi.save()
        om = OpenMissions(user=user, mission_instance=mi, leader=True)
        om.save()


def user_leaves_mission(user):
    om = OpenMissions.objects.get(user=user)
    if om.leader:
        mi = om.mission_instance
        aom = OpenMissions.objects.filter(mission_instance=om.mission_instance)
        aom.delete()
        mi.delete()
    else:
        om.delete()


def get_open_missions_on_planet(user):
    user_planet = UserLocation.objects.get(user=user).current
    mi = MissionInstances.objects.filter(referenced_mission__planet=user_planet, started=None)
    return [{"id": mi_current.id, "name": mi_current.referenced_mission.name, "player_count": OpenMissions.objects.filter(mission_instance=mi_current).count()} for mi_current in mi]


def join_mission(user, mission_instance_id):
    mi = MissionInstances.objects.get(id=mission_instance_id)
    if can_user_join_mission(user, mi.referenced_mission):
        if not mi.started:
            om = OpenMissions(user=user, mission_instance=mi)
            om.save()
            return True
    return False

def get_mission_details(user):
    result = {}
    om = OpenMissions.objects.get(user=user)
    aom = OpenMissions.objects.filter(mission_instance=om.mission_instance)
    result["open_mission_elements"] = aom
    result["mission_instance"] = om.mission_instance
    return result


def is_user_leader(user):
    om = OpenMissions.objects.get(user=user)
    return om.leader


def start_mission(user):
    """ This method is there to calculate all the things and start the mission -
     it sets up the events and data necessary"""
    mission_instance = OpenMissions.objects.get(user=user).mission_instance
    # Set the mission to started
    mission_instance.started = True
    start_time = time.time()

    mission_instance.start_time = start_time

    missionCache.add_mission(mission_instance.id)

    mttm = MissionTagsToMission.objects.filter(mission=mission_instance.referenced_mission)
    tag_ids = [e.mt.id for e in mttm]
    probabilities = [e.probability for e in mttm]

    eventService.prepare_mission_events(mission_instance.id, tag_ids, probabilities, mission_instance.referenced_mission.basic_time, 1)

    omo = OpenMissions.objects.filter(mission_instance=mission_instance)

    users = [o.user for o in omo]

    def parse_user_skills(us):
        return {str(s.skill_category.id): s.amount for s in us}


    user_skills = [parse_user_skills(UserSkills.objects.filter(user=u)) for u in users]
    user_ids = [u.id for u in users]

    for i in range(len(users)):
        missionCache.put_user_with_skills_to_mission(mission_instance.id, user_ids[i], user_skills[i])

    print "Started at", start_time

    mission_instance.save()


def get_events_up_to_this_point(user):
    mi = OpenMissions.objects.get(user=user).mission_instance
    up_to_this_point = eventService.get_events_up_to_this_point(mi.id)
    if up_to_this_point is False:
        remove_user_from_mission_hard(user)
        raise Exception("MissionAPI", 1)
    return up_to_this_point


def remaining_mission_time(user):
    mi = OpenMissions.objects.get(user=user).mission_instance
    return int((mi.start_time + mi.referenced_mission.basic_time) - time.time())


def remove_user_from_mission_hard(user):
    """ Extra Gateway to make it clearer """
    user_leaves_mission(user)

@transaction.commit_on_success
def complete_mission_for_user(user, is_death):
    # Get the Open Mission Object from the Player
    om = OpenMissions.objects.get(user=user)
    # Get the Mission Instance
    mi = om.mission_instance

    if not is_death:
        # Get, Check and Move if the target planet of the mission was not 0
        target_planet = mi.referenced_mission.target_planet

        if target_planet is not None:
            ul = UserLocation.objects.get(user=user)
            ul.current = target_planet
            ul.save()

    # Delete the OpenMissionObject
    om.delete()

    if not is_death:
        rewards = eventService.get_rewards_for_mission(mi.id)

        # Get the Rewards from teh Mission and add them to the user
        reward_money = mi.referenced_mission.reward_money + rewards["money"]
        reward_xp = mi.referenced_mission.reward_xp + rewards["xp"]

        userAPI.delta_experience_amount_for_user(user, reward_xp)
        userAPI.delta_money_amount_for_user(user, reward_money)

        # Create AnswerObject for the Rendering of the Reward Page
        cmAO = CompleteMissionAO(mi, "You get a basic reward of %i experience and %i $." %
                                     (mi.referenced_mission.reward_money, mi.referenced_mission.reward_xp))

        cmAO.add_event_reward_list(eventService.get_events_with_rewards(mi.id))
    else:
        cmAO = CompleteMissionAO(mi, "Your mission failed! Your clone has been activated!", death=True)

    # Try to get all remaining OpenMissionObject
    remaining_oms = OpenMissions.objects.filter(mission_instance=mi)

    # If there are no more OpenMissionObjects - Remove the MissionInstance from all Services and delete it from DB
    if remaining_oms.count() == 0:
        missionCache.remove_mission(mi.id)
        eventService.remove_mission(mi.id)
        mi.delete()

    return cmAO


def get_users_leftovers(user):
    mi = OpenMissions.objects.get(user=user).mission_instance
    if mi.started:
        result = missionCache.get_remaining_action_points_for_user(mi.id, user.id)
        return result
    return {}

@transaction.commit_on_success
def handle_event(user, event_id):
    mi = OpenMissions.objects.get(user=user).mission_instance

    if eventService.is_event_prevented(mi.id, int(event_id)):
        return missionCache.get_remaining_action_points_for_user(mi.id, user.id)

    # (ID, amount) - pairs
    needs = eventService.get_event_needs(mi.id, int(event_id))

    #TODO This only ches for the first need right now
    if missionCache.has_user_enough_action_points(mi.id, user.id, needs):
        missionCache.reduce_users_action_points(mi.id, user.id, needs)
        eventService.set_event_prevented(mi.id, int(event_id))

    return missionCache.get_remaining_action_points_for_user(mi.id, user.id)


def get_ship_and_crew_status(user):
    mi = OpenMissions.objects.get(user=user).mission_instance
    return eventService.get_summed_up_event_consequences(mi.id, time.time())


def is_mission_failed_by_death(user):
    return get_ship_and_crew_status(user)["death"]


def get_party_members(user):
    mi = OpenMissions.objects.get(user=user).mission_instance
    all_users = [{"id": om.user.id, "name": om.user.username} for om in OpenMissions.objects.filter(mission_instance=mi)]
    return all_users


def is_mission_started(user):
    return OpenMissions.objects.get(user=user).mission_instance.started is not None


def can_user_join_mission(user, mission):
    current_xp_value = userAPI.get_experience_amount_for_user(user)
    return current_xp_value >= mission.need_xp
