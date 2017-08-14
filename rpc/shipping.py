import json
from nameko.rpc import rpc


class ShippingRPC(object):
    """ this class make shipping request to add cost to trash
    Args:
        shipments(dict): information about address of the shipment
        parcel(dict): information about products
    Return:
        cost(int): total payment for shipping
        """
    name = 'ShippingRPC'

    @rpc
    def service_state(self, **kwargs):
        return json.dumps({'id': 42})

    @rpc
    def shipping_add(self, **kwargs):
        shipments = json.loads(kwargs.get('address_to'))
        parcel = json.loads(kwargs.get('parcel'))

        schema_shipments = {'name': {'type': 'string'},
                            'street1': {'type': 'string'},
                            'city': {'type': 'string'},
                            'state': {'type': 'string'},
                            'zip': {'type': 'string'},
                            'country': {'type': 'string'},
                            'phone': {'type': 'string'}
                            }
        schema_parcel = {'length': {'type': 'string'},
                         'width': {'type': 'string'},
                         'height': {'type': 'string'},
                         'distance_unit': {'type': 'string'},
                         'weight': {'type': 'string'},
                         'mass_unit': {'type': 'string'}
                        }

        return json.dumps({'id':43})
