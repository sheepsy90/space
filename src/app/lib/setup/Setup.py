from lib.setup.PlanetSetup import PlanetSetup
from lib.setup.MissionsSetup import MissionsSetup
from lib.setup.AcademySetup import AcademySetup
from lib.setup.SkillCategorySetup import SkillCategorySetup


__author__ = 'sheepy'




class Setup():

    def __init__(self):

        ### Step 1 - Independent things ###

        # Initialize the Locations
        locations = PlanetSetup()
        locations.setup()

        skill_category = SkillCategorySetup()
        skill_category.setup()

        academy = AcademySetup(locations)
        academy.setup()

        missions = MissionsSetup()
        missions.setup()