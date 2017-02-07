from django.http import HttpResponse

########################
### Catch All clause ###
########################
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def view_imprint(request):
    c = RequestContext(request, {})
    return render_to_response("general/imprint.html", c)

def catch_all(request, url):
    return HttpResponse("Sorry - this site is not available for you. <a href=\"/index\">Index</a>")
