from django.db import models

###########################################################################################################
### The Content that is independent of a user and can be stand alone (maybe they depend on each other)  ###
###########################################################################################################


class Planets(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SkillCategory(models.Model):
    name = models.CharField(max_length=100)


class AcademyAnswer(models.Model):
    answer_text = models.CharField(max_length=100)


class AcademyQuestion(models.Model):
    question_text = models.CharField(max_length=100)
    answers = models.ManyToManyField(AcademyAnswer)
    correct = models.IntegerField()


class AcademyReward(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    amount = models.IntegerField()
    category = models.ForeignKey(SkillCategory)


class AcademyProgram(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    cost = models.IntegerField()
    tutorial_text = models.CharField(max_length=1000)
    planets = models.ManyToManyField(Planets)
    questions = models.ManyToManyField(AcademyQuestion)
    reward = models.ManyToManyField(AcademyReward)

    def get_reward_list(self):
        return [{"name": r.category.name, "amount": r.amount} for r in self.reward.all()]

class MissionTags(models.Model):
    key = models.CharField(max_length=50)
    visible = models.BooleanField(default=False)


class Missions(models.Model):
    name = models.CharField(max_length=100)
    planet = models.ForeignKey(Planets)
    target_planet = models.ForeignKey(Planets, null=True, related_name="target_planet")
    basic_time = models.IntegerField()
    reward_xp = models.IntegerField()
    reward_money = models.IntegerField()
    need_xp = models.IntegerField()


class MissionTagsToMission(models.Model):
    mt = models.ForeignKey(MissionTags)
    mission = models.ForeignKey(Missions)
    probability = models.IntegerField()