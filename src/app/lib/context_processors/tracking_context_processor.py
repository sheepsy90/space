from lib.Configuration import Configuration

c = Configuration()


def add_tracking_code(request):
    if c.is_tracking_active():
        return {"tracking_code": c.get_tracking_code()}
    else:
        return {}