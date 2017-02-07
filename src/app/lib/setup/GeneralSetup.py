__author__ = 'sheepy'


class GeneralSetup():

    def save_and_get(self, obj):
        obj.save()
        return obj