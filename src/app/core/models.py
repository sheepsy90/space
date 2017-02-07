from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.forms.models import BaseModelFormSet
from core.content import Planets, AcademyProgram, SkillCategory, Missions


#########################################
### Relational Things within the Core ###
#########################################

class UserProperties(models.Model):
    EXPERIENCE = 1
    MONEY = 2
    SOUNDS = 3
    SOUND_ON = "on"
    SOUND_OFF = "off"
    TUTORIAL_STATE_KEY = 4
    TUTORIAL_STEP_0 = "0"
    TUTORIAL_STEP_1 = "1"
    TUTORIAL_STEP_FIN = "finished"

    """ The User Properties that each user have """
    user = models.ForeignKey(User)
    key = models.IntegerField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return "User %s with key %s has value of %s" % (self.user.username, self.key, self.value)


class UserLocation(models.Model):
    user = models.ForeignKey(User)
    current = models.ForeignKey(Planets)


class UserSkills(models.Model):
    user = models.ForeignKey(User)
    skill_category = models.ForeignKey(SkillCategory)
    amount = models.IntegerField(default=2)


class UserOnAcademyProgram(models.Model):
    user = models.ForeignKey(User)
    program = models.ForeignKey(AcademyProgram)
    tutorial_done = models.BooleanField(default=False)
    questions_correct = models.IntegerField(default=0)


class UserFinishedAcademyProgram(models.Model):
    user = models.ForeignKey(User)
    program = models.ForeignKey(AcademyProgram)


class MissionInstances(models.Model):
    referenced_mission = models.ForeignKey(Missions)
    started = models.IntegerField(null=True)
    start_time = models.IntegerField(null=True)


class OpenMissions(models.Model):
    user = models.ForeignKey(User)
    mission_instance = models.ForeignKey(MissionInstances)
    leader = models.BooleanField(default=False)

