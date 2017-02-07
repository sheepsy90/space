import random
from django.db import transaction
from core.content import AcademyProgram
from core.models import UserLocation, UserOnAcademyProgram, UserSkills, UserFinishedAcademyProgram
from lib.api.academy.AcademyProgramAO import AcademyProgramsAO
from lib.api.academy.AcademyQuestionAO import AcademyQuestionAO
from lib.api.academy.FinishProgramAO import FinishProgramAO
from lib.api.user import userAPI


def get_academy_programs_for_user(user):
    """ This method returns all the available academy programs for a specific user """
    #  Get the location of the user and according to that the academy programs on that location
    ul = UserLocation.objects.get(user=user)
    aps = AcademyProgram.objects.filter(planets=ul.current)

    # Get the Academy Programs the user already made
    fin_program = UserFinishedAcademyProgram.objects.filter(user=user)
    fin_program_id = [a.program.id for a in fin_program]

    # Filter those out
    result = aps.exclude(id__in=fin_program_id)

    return AcademyProgramsAO(result)


def is_user_in_program(user):
    return UserOnAcademyProgram.objects.filter(user=user).exists()


def put_user_in_program(user, program_id):
    """ This method puts a user in a specific program """
    ufap = UserFinishedAcademyProgram.objects.filter(user=user, program__id=program_id)
    if not ufap.exists():
        ap = AcademyProgram.objects.get(id=program_id)
        if ap.cost <= userAPI.get_money_amount_for_user(user):
            userAPI.delta_money_amount_for_user(user, -ap.cost)
            uoap = UserOnAcademyProgram(user=user, program=ap)
            uoap.save()
            return True
    return False


def user_still_in_tutorial(user):
    uoap = UserOnAcademyProgram.objects.filter(user=user)
    return uoap.exists() and not uoap[0].tutorial_done


def get_tutorial_text(user):
    uoap = UserOnAcademyProgram.objects.get(user=user)
    return uoap.program.tutorial_text



def get_random_question_for_current_user_academy_program(user):
    uoap = UserOnAcademyProgram.objects.get(user=user)
    allquestions = [[u] for u in uoap.program.questions.all()]
    random.shuffle(allquestions)
    return AcademyQuestionAO(allquestions[0][0])


def finish_tutorial_for_user(user):
    uoap = UserOnAcademyProgram.objects.get(user=user)
    uoap.tutorial_done = True
    uoap.save()

@transaction.commit_on_success
def answer_question(user, question_id, answer_id):
    uoap = UserOnAcademyProgram.objects.get(user=user)
    qqs = uoap.program.questions.filter(id=question_id)
    if qqs.exists() and qqs.count() == 1:
        question = qqs[0]
        if question.correct == int(answer_id):
            uoap.questions_correct += 1
            uoap.save()
            return True
        else:
            return False
    raise Exception("AcademyAPI", "Something went wrong")


def is_program_finished(user):
    uoap = UserOnAcademyProgram.objects.get(user=user)
    print uoap.questions_correct
    return uoap.questions_correct >= 3




def user_on_academy_program(user):
    uoap = UserOnAcademyProgram.objects.filter(user=user)
    return uoap.exists()

@transaction.commit_on_success
def set_program_finished(user):
    finishProgramAO = FinishProgramAO()

    uoap = UserOnAcademyProgram.objects.get(user=user)
    rewards = uoap.program.reward.all()
    finishProgramAO.set_description(uoap.program.desc)
    for reward in rewards:
        us = UserSkills.objects.get(skill_category=reward.category, user=user)
        us.amount += reward.amount
        us.save()
        finishProgramAO.add_reward(reward)

    ufap = UserFinishedAcademyProgram(user=user, program=uoap.program)
    print "Finishing Programm: ", ufap.program.id
    ufap.save()
    uoap.delete()

    return finishProgramAO


def user_can_join_program(user, academy_id):
    print academy_id
    ap = AcademyProgram.objects.get(id=academy_id)
    value = userAPI.get_money_amount_for_user(user) >= ap.cost
    print value
    return value

