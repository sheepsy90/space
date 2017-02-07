from django.contrib.auth.models import User

from django.db import transaction
from core.content import Planets, SkillCategory
from core.models import UserProperties, UserLocation, UserSkills



import lib.log.logger as _logger

_loggerinstance = _logger.getInstance()


def check_double_email(email):
    try:
        if User.objects.filter(email=email).exists():
            raise Exception("UserAPI", "Multiple Email!")
    except User.DoesNotExist:
        pass


def set_default_user_properties(user):
    UserProperties(user=user, key=UserProperties.EXPERIENCE, value=0).save()
    UserProperties(user=user, key=UserProperties.MONEY, value=200).save()
    UserProperties(user=user, key=UserProperties.SOUNDS, value=1).save()
    UserProperties(user=user, key=UserProperties.TUTORIAL_STATE_KEY, value=UserProperties.TUTORIAL_STEP_0).save()


def set_default_location(user):
    defaultLocation = Planets.objects.get(id=1)
    userlocation = UserLocation(user=user, current=defaultLocation)
    userlocation.save()


def get_money_amount_for_user(user):
    return int(UserProperties.objects.get(user=user, key=UserProperties.MONEY).value)


def delta_money_amount_for_user(user, amount):
    up = UserProperties.objects.get(user=user, key=UserProperties.MONEY)
    up.value = str(int(up.value) + amount)
    up.save()


def get_experience_amount_for_user(user):
    return int(UserProperties.objects.get(user=user, key=UserProperties.EXPERIENCE).value)


def delta_experience_amount_for_user(user, amount):
    up = UserProperties.objects.get(user=user, key=UserProperties.EXPERIENCE)
    up.value = str(int(up.value) + amount)
    up.save()


@transaction.commit_on_success
def create_new_user_return_object(username, email, password, blank=False):
    """ This creates a new basic user with an empty backpack """
    # First check for double email
    check_double_email(email)
    # First create the User
    user = User.objects.create_user(username, email, password)
    user.save()

    # Create User Properties
    set_default_user_properties(user)

    # Set the user to a specific Location
    set_default_location(user)

    # Create Basic Skills
    create_basic_skills(user)

    # Return the id of the created user
    return user

@transaction.commit_on_success
def create_basic_skills(user):
    for sk in SkillCategory.objects.all():
        us = UserSkills(skill_category=sk, user=user)
        us.save()


@transaction.commit_on_success
def create_new_user_return_id(username, email, password, blank=False):
    """ This creates a new basic user with an empty backpack and returns the id """
    return create_new_user_return_object(username, email, password, blank=blank).id


def is_tutorial_in_state_0(user):
    return UserProperties.objects.get(user=user, key=UserProperties.TUTORIAL_STATE_KEY).value == UserProperties.TUTORIAL_STEP_0
