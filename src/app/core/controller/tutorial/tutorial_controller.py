import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from core.controller.academy.academy_controller import enter_program
from core.models import UserProperties
from lib.api.user import userAPI


@login_required(login_url='/index/')
def view_tutorial_page(request):
    if userAPI.is_tutorial_in_state_0(request.user):
        c = RequestContext(request, {})
        return render_to_response('tutorial/tutorial_page_one.html', c)
    return HttpResponseRedirect("/planet/")


def determine_academy_program_for_tutorial(chosen_program):
    return 1


@login_required(login_url='/index/')
def choose_academy_program_in_tutorial(request):
    if request.POST:
        if "program" in request.POST:
            chosen_program = request.POST["program"]
            tutorial_program_id = determine_academy_program_for_tutorial(chosen_program)
            finish_first_program_tutorial(request.user)
            return enter_program(request, tutorial_program_id)
    return render_to_response('tutorial/tutorial_page_one.html')


@login_required(login_url='/index/')
def confirm_tutorial_science_letter(request):
    finish_second_step_tutorial(request.user)
    return HttpResponse()


def finish_second_step_tutorial(user):
    up = UserProperties.objects.get(user=user, key=UserProperties.TUTORIAL_STATE_KEY)
    up.value = UserProperties.TUTORIAL_STEP_FIN
    up.save()

def finish_first_program_tutorial(user):
    up = UserProperties.objects.get(user=user, key=UserProperties.TUTORIAL_STATE_KEY)
    up.value = UserProperties.TUTORIAL_STEP_1
    up.save()
