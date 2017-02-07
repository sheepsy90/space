from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = 'sheepy'

@login_required(login_url='/index/')
def view_information(request):
    c = RequestContext(request, {})
    return render_to_response('general/information.html', c)
