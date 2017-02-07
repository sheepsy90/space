from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

from services.mission_service.methods.MissionCache import MissionCache


class MissionService():

    def __init__(self, host, port):
        srv = SimpleJSONRPCServer((host, port))
        srv.register_introspection_functions()
        srv.register_function(self.ping)

        mc = MissionCache()
        srv.register_instance(mc)

        print "[GameServerService] Up and running!"
        srv.serve_forever()

    def ping(self, msg):
        """Simply returns the args passed to it as a string"""
        return str(msg)


