import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.models import UserProperties

__author__ = 'sheepy'

@login_required(login_url='/index/')
def view_settings(request):
    status = UserProperties.objects.get(user=request.user, key=UserProperties.SOUNDS).value == UserProperties.SOUND_ON
    c = RequestContext(request, {"sound_status": status})
    return render_to_response('general/settings.html', c)


@login_required(login_url='/index/')
def switch_sound_setting_state(request):
    up = UserProperties.objects.get(user=request.user, key=UserProperties.SOUNDS)
    if up.value == UserProperties.SOUND_ON:
        up.value = UserProperties.SOUND_OFF
    else:
        up.value = UserProperties.SOUND_ON
    up.save()

    new_state = up.value == UserProperties.SOUND_ON

    return HttpResponse(json.dumps({"success": True, "new_state": new_state}), mimetype="application/json")