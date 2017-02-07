from core.content import Planets
from lib.setup.GeneralSetup import GeneralSetup



class PlanetSetup(GeneralSetup):
    """ Comment """
    
    def setup(self):
        print "Creating Locations..."
        self.EARTH = Planets.objects.get(name="Earth")
        self.MOON = Planets.objects.get(name="Moon")
        self.MARS = Planets.objects.get(name="Mars")
        self.PLUTO = Planets.objects.get(name="Pluto")
        self.GLIESE581d = Planets.objects.get(name="Gliese 581d")


