from nameko.rpc import rpc


class GreetingService2(object):
    name = 'greeting_service2'

    @rpc
    def hello(self, name):

        return 'Hello {}!!!! from class {}'.format(name,
                                                   self.__class__.__name__)
