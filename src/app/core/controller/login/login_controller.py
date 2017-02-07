from django.core.context_processors import csrf
from django.template.context import RequestContext
from lib.context_processors import tracking_context_processor
import lib.log.logger as _logger

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from lib.validator.LoginValidator import LoginValidator
from lib.Configuration import Configuration

_configuration = Configuration()
_loggerinstance = _logger.getInstance()

def index(request):
    if check_is_user_loggedin(request):
        _loggerinstance.log("Logged in user accessed Index-Page - (%s)" % request.user.username, "INFO")
        return HttpResponseRedirect("/planet")
    else:
        _loggerinstance.log("Anonymous user accessed Index-Page", "INFO")

    c = {}
    c.update(tracking_context_processor.add_tracking_code(request))
    c.update(csrf(request))
    return render_to_response('landingpage/index.html', c)

@LoginValidator
def login_user(request):
    """ This is the Login request for logging in a user """
    username = request.POST['user']
    password = request.POST['password']
    return login_user_and_redirect_to_welcomepage(request, username, password)

    
def login_user_and_redirect_to_welcomepage(request, username, password):
    """ This Method logs a user with his username and password in """
    user = authenticate(username=username, password=password)        
    error_cause = "User doesn't exists."
    if (user is not None):
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect("/planet")
        else:
            error_cause = "User is not Active"
    return render_to_response('general/error.html', {"cause": error_cause})


@login_required(login_url='/index/')
def logoutpage(request):
    logout(request)
    return HttpResponseRedirect("/index")


def check_is_user_loggedin(request):
    return "AnonymousUser" != request.user.__str__()