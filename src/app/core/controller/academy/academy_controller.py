import json
from django.template import RequestContext
from core.controller.tutorial.TutorialRedirectDecorator import TutorialRedirectDecorator
import lib.log.logger as _logger

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

from lib.api.academy import academyAPI
from lib.api.mission import missionAPI


_loggerinstance = _logger.getInstance()

@login_required(login_url='/index/')
@TutorialRedirectDecorator
def view_academy(request):
    if missionAPI.user_participates_in_mission(request.user):
        return HttpResponseRedirect("/current_mission")
    if academyAPI.user_on_academy_program(request.user):
        return HttpResponseRedirect("/ongoing_program")
    academyProgramsAO = academyAPI.get_academy_programs_for_user(request.user)
    c = RequestContext(request, {"academy_offers": academyProgramsAO.get_offers()})
    return render_to_response('academy/academy.html', c)


@login_required(login_url='/index/')
def enter_program(request, program_id):
    if academyAPI.is_user_in_program(request.user):
        return HttpResponseRedirect('/ongoing_program')
    else:
        if academyAPI.put_user_in_program(request.user, program_id):
            return HttpResponseRedirect('/ongoing_program')
        else:
            return HttpResponseRedirect('/academy')


@login_required(login_url='/index/')
def can_join_program(request):
    if request.POST:
        assert "academy_program_id" in request.POST
        can_join = academyAPI.user_can_join_program(request.user, request.POST["academy_program_id"])
        c = {"success": True, "can_join": can_join}
        return HttpResponse(json.dumps(c), mimetype="application/json")
    c = {"success": False, "message": "Some Error!"}
    return HttpResponse(json.dumps(c), mimetype="application/json")


@login_required(login_url='/index/')
def ongoing_program(request):
    # Check if user is on program at all
    if not academyAPI.user_on_academy_program(request.user):
        return HttpResponseRedirect("/academy/")
    # Check if the program is finished
    if academyAPI.is_program_finished(request.user):
        finishProgramAO = academyAPI.set_program_finished(request.user)
        return render_to_response("academy/finish_program.html", {"finishProgramAO": finishProgramAO})
    c = {}
    c["tutorial"] = True

    if academyAPI.user_still_in_tutorial(request.user):
        c["tutorial_text"] = academyAPI.get_tutorial_text(request.user)
    else:
        c["tutorial"] = False
        c["random_question"] = academyAPI.get_random_question_for_current_user_academy_program(request.user)
    c = RequestContext(request, c)
    return render_to_response('academy/ongoing_program.html', c)


@login_required(login_url='/index/')
def finish_tutorial(request):
    if academyAPI.is_user_in_program(request.user):
        academyAPI.finish_tutorial_for_user(request.user)
        return HttpResponseRedirect('/ongoing_program')
    else:
        return render_to_response('general/error.html')


@login_required(login_url='/index/')
def answer_question(request):
    if request.POST:
        assert "question_id" in request.POST
        assert "answer_id" in request.POST

        answer_correct = academyAPI.answer_question(request.user, request.POST["question_id"], request.POST["answer_id"])
        program_finished = academyAPI.is_program_finished(request.user)

        c = {"success": True, "answer_correct": answer_correct, "program_finished": program_finished}
        return HttpResponse(json.dumps(c), mimetype="application/json")

    c = {"success": False, "message": "Some Error!"}
    return HttpResponse(json.dumps(c), mimetype="application/json")