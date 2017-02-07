import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from core.content import SkillCategory
from core.controller.tutorial.TutorialRedirectDecorator import TutorialRedirectDecorator
from lib.api.mission import missionAPI
from lib.api.user import userAPI

import lib.log.logger as _logger

_loggerinstance = _logger.getInstance()

from lib.Configuration import Configuration

_configuration = Configuration()


@login_required(login_url='/index/')
@TutorialRedirectDecorator
def view_planet(request):
    if missionAPI.user_participates_in_mission(request.user):
        return HttpResponseRedirect("/current_mission/")
    mission = missionAPI.get_possible_missions_for_player(request.user)
    c = RequestContext(request, {"missions": mission})
    return render_to_response('mission/planet.html', c)



@login_required(login_url='/index/')
def prepare_mission(request, mission_id):
    """ Method for starting a mission """
    if missionAPI.user_participates_in_mission(request.user):
        return HttpResponseRedirect("/current_mission/")
    else:
        missionAPI.prepare_mission(request.user, mission_id)
        return HttpResponseRedirect("/current_mission/")

@login_required(login_url='/index/')
def current_mission(request):
    if not missionAPI.user_participates_in_mission(request.user):
        return HttpResponseRedirect("/planet/")
    mission_details = missionAPI.get_mission_details(request.user)
    is_leader = missionAPI.is_user_leader(request.user)
    skill_categories = SkillCategory.objects.all()
    c = RequestContext(request, {"mission_details": mission_details,
                                 "is_leader": is_leader,
                                 "skill_categories": skill_categories})
    return render_to_response('mission/current_mission.html', c)


@login_required(login_url='/index/')
def leave_mission(request):
    if missionAPI.user_participates_in_mission(request.user):
        missionAPI.user_leaves_mission(request.user)
        return HttpResponseRedirect("/planet")
    else:
        return HttpResponseRedirect("/planet")

@login_required(login_url='/index/')
def join_mission(request, mission_instance_id):
    if missionAPI.user_participates_in_mission(request.user):
        return HttpResponseRedirect("/current_mission/")
    else:
        missionAPI.join_mission(request.user, mission_instance_id)
        return HttpResponseRedirect("/current_mission/")

@login_required(login_url='/index/')
def start_mission(request):
    if missionAPI.is_user_leader(request.user):
        missionAPI.start_mission(request.user)
        return HttpResponseRedirect("/current_mission/")


@login_required(login_url='/index/')
def poll_events(request):
    if missionAPI.user_participates_in_mission(request.user):
        try:
            events_up_to_this_time = missionAPI.get_events_up_to_this_point(request.user)
        except Exception as e:
            print e
            events_up_to_this_time = []
        status = missionAPI.get_ship_and_crew_status(request.user)
        user_leftovers = missionAPI.get_users_leftovers(request.user)
        print events_up_to_this_time
        remaining = missionAPI.remaining_mission_time(request.user)
        c = {"success": True, "data": events_up_to_this_time, "finished": remaining < 0, "time_left": remaining,
             "user_leftovers": user_leftovers, "status": status}
        return HttpResponse(json.dumps(c), mimetype="application/json")
    return HttpResponseRedirect("/planet/")

@login_required(login_url='/index/')
def complete_mission(request):
    if missionAPI.user_participates_in_mission(request.user):
        remaining = missionAPI.remaining_mission_time(request.user)
        is_death = missionAPI.is_mission_failed_by_death(request.user)
        if remaining < 0 or is_death:
            completeMissionAO = missionAPI.complete_mission_for_user(request.user, is_death)
            c = RequestContext(request, {"complete_mission_ao": completeMissionAO})
            return render_to_response("mission/complete_mission.html", c)
        else:
            return HttpResponseRedirect("/current_mission/")
    return HttpResponseRedirect("/planet/")

@login_required(login_url='/index/')
def handle_event(request, event_id):
    try:
        if missionAPI.user_participates_in_mission(request.user):
            user_leftovers = missionAPI.handle_event(request.user, event_id)
            return HttpResponse(json.dumps({"success": True, "leftovers": user_leftovers}), mimetype="application/json")
        else:
            return HttpResponse(json.dumps({"success": False}), mimetype="application/json")
    except:
        return HttpResponse(json.dumps({"success": False}), mimetype="application/json")


@login_required(login_url='/index/')
def poll_available_missions(request):
    result = missionAPI.get_open_missions_on_planet(request.user)
    return HttpResponse(json.dumps({"success": True, "data": result}), mimetype="application/json")

@login_required(login_url='/index/')
def poll_party_members(request):
    result = missionAPI.get_party_members(request.user)
    game_started = missionAPI.is_mission_started(request.user)
    return HttpResponse(json.dumps({"success": True, "data": result, "game_started": game_started}), mimetype="application/json")