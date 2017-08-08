from nameko.rpc import rpc


class GreetingService(object):
    name = 'greeting_service'

    @rpc
    def hello(self, name):
        return 'Hello {}!!!! from class {}'.format(name,
                                                   self.__class__.__name__)
