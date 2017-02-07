from core.controller.login import login_controller
from core.models import UserProperties

__author__ = 'sheepy'


def add_tutorial_state(request):
    if login_controller.check_is_user_loggedin(request):
        is_in_state_1 = UserProperties.objects.get(user=request.user, key=UserProperties.TUTORIAL_STATE_KEY).value == UserProperties.TUTORIAL_STEP_1
        return {"tutorial_state_1": is_in_state_1}