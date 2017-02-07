from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from services.event_service.methods.EventServiceMethods import EventServiceMethods


class EventService():

    def __init__(self, host, port, testing=False, injector=None):
        srv = SimpleJSONRPCServer((host, port))
        srv.register_introspection_functions()
        srv.register_function(self.ping)

        mc = EventServiceMethods()
        srv.register_instance(mc)

        if testing and injector is not None:
            injector.inject(mc)

        print "[GameServerService] Up and running!"
        srv.serve_forever()

    def ping(self, msg):
        """Simply returns the args passed to it as a string"""
        return str(msg)


