from django.http.response import HttpResponseRedirect
from core.models import UserProperties


class TutorialRedirectDecorator():

    def __init__(self, function):
        self.function = function

    def __call__(self, request):
        tut_value = UserProperties.objects.get(user=request.user, key=UserProperties.TUTORIAL_STATE_KEY).value

        if tut_value == UserProperties.TUTORIAL_STEP_0:
            return HttpResponseRedirect("/tutorial/")
        else:
            return self.function(request)
