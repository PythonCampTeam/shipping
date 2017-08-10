from nameko.rpc import rpc


class Shipping(object):
    """ this class make shipping request to add cost to trash
    Args:
        name(str): The name shipping company
        aditional(dict): information about tovar
    Return:
        cost(int): total payement for dostavka
        """
    name = 'ShippingRPC'

    @rpc
    def service_state(self, **kwargs):
        doc_class = self.__dict__
        return {self.__class__.__name__: doc_class,
                'docs': self.__class__.__doc__}
