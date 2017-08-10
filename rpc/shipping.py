import json
from nameko.rpc import rpc
import shippo


class ShippingRPC(object):
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
        address1 = shippo.Address.create(
            name='John Smith',
            street1='6512 Greene Rd.',
            street2='',
            company='Initech',
            phone='+1 234 346 7333',
            city='Woodridge',
            state='IL',
            zip='60517',
            country='US',
            metadata='Customer ID 123456'
        )
        return json.dumps(address1)
