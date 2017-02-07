import random


class AcademyQuestionAO():

    def __init__(self, academy_question):
        self.question_text = academy_question.question_text

        answer_lst = [[a] for a in academy_question.answers.all()]
        random.shuffle(answer_lst)

        self.answer_1 = answer_lst[0][0].answer_text
        self.answer_2 = answer_lst[1][0].answer_text
        self.answer_3 = answer_lst[2][0].answer_text
        self.answer_4 = answer_lst[3][0].answer_text

        self.answer_1_id = answer_lst[0][0].id
        self.answer_2_id = answer_lst[1][0].id
        self.answer_3_id = answer_lst[2][0].id
        self.answer_4_id = answer_lst[3][0].id

        self.question_id = academy_question.id