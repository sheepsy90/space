from core.content import Planets, AcademyAnswer, AcademyQuestion, AcademyProgram, AcademyReward, SkillCategory
from lib.setup.GeneralSetup import GeneralSetup



class AcademySetup(GeneralSetup):
    """ Comment """

    def __init__(self, locations):
        self.locations = locations
        self.MEDICAL = SkillCategory.objects.get(name="MEDICAL")
        self.NAVIGATION = SkillCategory.objects.get(name="NAVIGATION")
        self.ENGINEERING = SkillCategory.objects.get(name="ENGINEERING")
        self.BIOLOGY = SkillCategory.objects.get(name="BIOLOGY")
        self.PHYSICS = SkillCategory.objects.get(name="PHYSICS")
        self.CHEMISTRY = SkillCategory.objects.get(name="CHEMISTRY")
        self.INFORMATICS = SkillCategory.objects.get(name="INFORMATICS")
        self.GEOLOGY = SkillCategory.objects.get(name="GEOLOGY")

    def setup_academy_question(self, question_text, correct_answer, answer2, answer3, answer4):
        aa1, aa2, aa3, aa4 = self.create_answers(correct_answer, answer2, answer3, answer4)
        ag1 = AcademyQuestion(question_text=question_text, correct=aa1.id)
        ag1.save()
        ag1.answers.add(aa1)
        ag1.answers.add(aa2)
        ag1.answers.add(aa3)
        ag1.answers.add(aa4)
        ag1.save()
        return ag1


    def setup(self):
        print "Creating AcademyStuff..."

        self.setup_engineering_101()
        self.setup_basic_science_101()
        self.setup_basic_solar_system()
        self.setup_basic_geology101()
        self.setup_basic_first_aid()
        self.setup_basic_chemistry()
        self.setup_basic_biology()

    def create_answers(self, text1, text2, text3, text4):
        aa1 = AcademyAnswer(answer_text=text1)
        aa1.save()
        aa2 = AcademyAnswer(answer_text=text2)
        aa2.save()
        aa3 = AcademyAnswer(answer_text=text3)
        aa3.save()
        aa4 = AcademyAnswer(answer_text=text4)
        aa4.save()
        return [aa1, aa2, aa3, aa4]

    def setup_engineering_101(self):
        aq1 = self.setup_academy_question("What tools use engineers?", "Science & Math", "Greek Mythology", "Needle's & IV-Bags", "Gene Sequencers")
        aq2 = self.setup_academy_question("What do engineers do?", "Solve problems!", "Clean wounds!", "Categorize Plants!", "Testing soil!")
        aq3 = self.setup_academy_question("What type of engineer does not exists?", "Flying Engineer!", "Software Engineer!", "Chemical Engineer!", "Mechanical Engineer!")


        ap = AcademyProgram(name="Engineering 101", desc="What is engineering?", cost=50, tutorial_text="""<center><iframe style="margin: 0 auto" width="560"
            height="315" src="//www.youtube.com/embed/bipTWWHya8A" frameborder="0" allowfullscreen></iframe></center>""")
        ap.save()
        ap.planets.add(self.locations.EARTH)
        ap.questions.add(aq1)
        ap.questions.add(aq2)
        ap.questions.add(aq3)
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.ENGINEERING)))
        ap.save()

    def setup_basic_solar_system(self):
        aq1 = self.setup_academy_question("What contributes to the flat solar system?", "Collisions!", "Cohesion!", "Adhesion!", "Vacuum!")
        aq2 = self.setup_academy_question("What contributes to the flat solar system?", "3D Space!", "Vacuum!", "Cohesion!", "Adhesion!")
        aq3 = self.setup_academy_question("What shape has our solar system?", "Flat", "Round", "Cylindrical", "Egg shaped")

        ap = AcademyProgram(name="Physics", desc="Why is the solar system flat?", cost=200, tutorial_text="""<center>
            <iframe width="560" height="315" src="//www.youtube.com/embed/tmNXKqeUtJM" frameborder="0"
            allowfullscreen></iframe></center>""")
        ap.save()
        ap.planets.add(self.locations.EARTH)
        ap.questions.add(aq1)
        ap.questions.add(aq2)
        ap.questions.add(aq3)
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=2, category=self.PHYSICS)))

        ap.save()


    def setup_basic_science_101(self):

        aq1 = self.setup_academy_question("What do scientist's not do?", "Make up data!", "Write publications!", "Make hypothesis!", "Present results!")
        aq2 = self.setup_academy_question("Science is a ______ process!", "non-linear", "linear", "obvious", "easy")
        aq3 = self.setup_academy_question("What do you need, to perform science?", "Nothing", "Be a doctor!", "Be a student!", "Be a professor!")

        ap = AcademyProgram(name="Science 101", desc="What is Science?", cost=150, tutorial_text="""<center>
            <iframe width="560" height="315" src="//www.youtube.com/embed/Jj9iNphbY88"
            frameborder="0" allowfullscreen></iframe></center>""")
        ap.save()
        ap.planets.add(self.locations.EARTH)
        ap.questions.add(aq1)
        ap.questions.add(aq2)
        ap.questions.add(aq3)
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.NAVIGATION)))
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.PHYSICS)))
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.MEDICAL)))
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.CHEMISTRY)))
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.BIOLOGY)))
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.ENGINEERING)))
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.INFORMATICS)))
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=1, category=self.GEOLOGY)))

        ap.save()


    def setup_basic_geology101(self):

        aq1 = self.setup_academy_question("What does calving mean?",  "Glaciers loose parts!", "Glaciers move!", "Glaciers go dark!", "Glaciers saving sun energy!")
        aq2 = self.setup_academy_question("What means less ice in the artic?", "Less sunlight reflection!", "More sunlight reflection!", "No change at all!", "Lower Sea levels!")
        aq3 = self.setup_academy_question("What country could suffer from rising sea levels?", "Bangladesh", "Peru", "Australia", "Switzerland")

        ap = AcademyProgram(name="Geology - Climate", desc="The arctic battleground!", cost=150, tutorial_text="""<center>
            <iframe width="560" height="315" src="//www.youtube.com/embed/ircJWRUdoeg" frameborder="0" allowfullscreen></iframe></center>""")
        ap.save()
        ap.planets.add(self.locations.EARTH)
        ap.questions.add(aq1)
        ap.questions.add(aq2)
        ap.questions.add(aq3)
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=2, category=self.GEOLOGY)))

        ap.save()

    def setup_basic_first_aid(self):

        aq1 = self.setup_academy_question("What colour should your medical bag be?",  "Orange", "Grey", "Black", "White")
        aq2 = self.setup_academy_question("What should be in the medical bag?", "Bandages", "Blanket", "Gun", "Candles")
        aq3 = self.setup_academy_question("What should you do next to having a medical bag?", "Take a medical course", "Play EMT", "Train CPR on your friend", "Take medicine")

        ap = AcademyProgram(name="Medical - Basic", desc="Basic first aid kit", cost=150, tutorial_text="""<center>
            <iframe width="560" height="315" src="//www.youtube.com/embed/5Oq4xnaET2Q" frameborder="0" allowfullscreen></iframe></center>""")
        ap.save()
        ap.planets.add(self.locations.EARTH)
        ap.questions.add(aq1)
        ap.questions.add(aq2)
        ap.questions.add(aq3)
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=2, category=self.MEDICAL)))

        ap.save()

    def setup_basic_biology(self):

        aq2 = self.setup_academy_question("What is an ecosystem?", "Group of organisms in a specific area and the non-living things", "Group of organisms with the same ancestor", "Group of land animals", "System of maximal three animals")
        aq3 = self.setup_academy_question("What is not a biome?", "Space", "Desert",  "City", "Grassland")
        aq4 = self.setup_academy_question("What is a category for factors that determine how a place looks like?", "Abiotic", "Probiotic", "Antibiotic", "Postbiotic")
        aq5 = self.setup_academy_question("What is a category for factors that determine how a place looks like?", "Biotic", "Probiotic", "Antibiotic", "Postbiotic")

        ap = AcademyProgram(name="Biology - Basic", desc="What is ecology?", cost=150, tutorial_text="""<center>
                   <iframe width="560" height="315" src="//www.youtube.com/embed/izRvPaAWgyw" frameborder="0" allowfullscreen></iframe></center>""")
        ap.save()
        ap.planets.add(self.locations.EARTH)
        ap.questions.add(aq2)
        ap.questions.add(aq3)
        ap.questions.add(aq4)
        ap.questions.add(aq5)
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=2, category=self.BIOLOGY)))

        ap.save()

    def setup_basic_chemistry(self):

        aq2 = self.setup_academy_question("What molecules define water?", "Hydrogen & Oxygen", "Carbon & Oxygen", "Sulfur & Hydrogen", "Only hydrogen")
        aq3 = self.setup_academy_question("How can you split water in it's elemental parts? ", "By electricity", "By temperature",  "By light", "By pressure")
        aq4 = self.setup_academy_question("Which melting point has water??", "0 Degree", "100 Degree", "42 Degree", "212 Degree")

        ap = AcademyProgram(name="Chemistry - Basic", desc="What is chemistry?", cost=150, tutorial_text="""<center>
                   <iframe width="420" height="315" src="//www.youtube.com/embed/5BrIZqyG6rA" frameborder="0" allowfullscreen></iframe></center>""")
        ap.save()
        ap.planets.add(self.locations.EARTH)
        ap.questions.add(aq2)
        ap.questions.add(aq3)
        ap.questions.add(aq4)
        ap.reward.add(self.save_and_get(AcademyReward(name="Lohn", desc="Lohn1", amount=2, category=self.CHEMISTRY)))

        ap.save()
