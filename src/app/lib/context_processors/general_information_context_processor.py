from core.controller.login import login_controller
from core.models import UserSkills, UserProperties, UserLocation


def add_general_user_information(request):
    if login_controller.check_is_user_loggedin(request):
        data = {"username": request.user.username}

        data["action_points"] = [{"name": usk.skill_category.name[0:3], "amount": usk.amount} for usk in UserSkills.objects.filter(user=request.user)]

        data["level"] = UserProperties.objects.get(user=request.user, key=UserProperties.EXPERIENCE).value
        data["money"] = UserProperties.objects.get(user=request.user, key=UserProperties.MONEY).value
        data["sound_enabled"] = UserProperties.objects.get(user=request.user, key=UserProperties.SOUNDS).value == UserProperties.SOUND_ON

        data["location_name"] = UserLocation.objects.get(user=request.user).current.name

        return {'general_info': data}