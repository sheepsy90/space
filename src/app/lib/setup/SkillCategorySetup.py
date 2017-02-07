from core.content import SkillCategory
from lib.setup.GeneralSetup import GeneralSetup


class SkillCategorySetup(GeneralSetup):
    """ Comment """
    
    def setup(self):
        print "Creating Skill Categories..."
        self.MEDICAL = SkillCategory.objects.get(name="MEDICAL")
        self.NAVIGATION = SkillCategory.objects.get(name="NAVIGATION")
        self.ENGINEERING = SkillCategory.objects.get(name="ENGINEERING")
        self.BIOLOGY = SkillCategory.objects.get(name="BIOLOGY")
        self.PHYSICS = SkillCategory.objects.get(name="PHYSICS")
        self.CHEMISTRY = SkillCategory.objects.get(name="CHEMISTRY")
        self.INFORMATICS = SkillCategory.objects.get(name="INFORMATICS")
        self.GEOLOGY = SkillCategory.objects.get(name="GEOLOGY")



