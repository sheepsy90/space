from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from core.controller.login.login_controller import login_user_and_redirect_to_welcomepage, check_is_user_loggedin
from lib.api.user import userAPI
from lib.context_processors import tracking_context_processor
from lib.validator.RegistrationValidator import RegistrationValidator

import lib.log.logger as _logger
from lib.Configuration import Configuration

_configuration = Configuration()
_loggerinstance = _logger.getInstance()

def view_registration_page(request):
    if check_is_user_loggedin(request):
        _loggerinstance.log("Logged in user accessed Registration-Page - (%s)"  % request.user.username, "INFO")
        return HttpResponseRedirect("/planet")
    else:
        _loggerinstance.log("Anonymous user accessed Registration-Page", "INFO")
    c = {}
    c.update(tracking_context_processor.add_tracking_code(request))
    c.update(csrf(request))
    return render_to_response('registration/registration.html', c)



@RegistrationValidator
def send_registration(request):
    # Get the Username
    username = request.POST["user"]
    # Check if username is empty
    if (len(username) == 0 or username == "AnonymousUser"):
            return render_to_response('general/error.html',  {"cause": "Username isn't allowed to be empty."})
    # Check if it doesn't exists already
    if (len(User.objects.filter(username__exact=username)) == 0):
        # Get the both passwords
        pw_initial = request.POST["password_first"]
        pw_again = request.POST["password_again"]
        # Compare them if they are equals
        if (pw_initial == pw_again):
            # Create a new user using the userAPI
            userAPI.create_new_user_return_id(username, str(username) + "@email.de", pw_initial)
            _loggerinstance.log("User registered (%s)!" % str(username), "INFO")
            # log him in and return welcomepage
            return login_user_and_redirect_to_welcomepage(request, username, pw_initial)
        else:
            return render_to_response('general/error.html', {"cause": "Passwords doesn't match."})
    else:
        return render_to_response('general/error.html', {"cause": "Username already exists."})
