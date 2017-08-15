import json
import cerberus
import shippo
from nameko.rpc import rpc
import db.database as db
#import integration.goshippo as shippo


class ShippingRPC(object):
    """ this class make shipping request to add cost to trash
    Args:
        shipments(dict): information about address of the shipment
        parcel(dict): information about products
    Return:
        cost(int): total payment for shipping
        """
    name = 'ShippingRPC'
    store_db = db.StoreDB(data_stored='address_to', data_key='object_id')

    @rpc
    def service_state(self, **kwargs):
        return json.dumps({'id': 42})

    @rpc
    def shipping_add(self, **kwargs):
        shipments = json.loads(kwargs.get('address_to'))
        parcel = kwargs.get('parcel')

        schema_shipments = {'name': {'type': 'string'},
                            'street1': {'type': 'string'},
                            'city': {'type': 'string'},
                            'state': {'type': 'string'},
                            'zip': {'type': 'string'},
                            'country': {'type': 'string'},
                            'phone': {'type': 'string'}
                            }
        parcel = {
            "length": "5",
            "width": "5",
            "height": "5",
            "distance_unit": "in",
            "weight": "2",
            "mass_unit": "lb",
        }

        v = cerberus.Validator()
        if v(shipments, schema_shipments):
            shippo.verify_ssl_certs = True
            shippo.api_key = 'shippo_test_55dfc05531b49ed2e711fa2cca863d72c68f87b7'

            shipment = shippo.Shipment.create(address_from=shipments,
                                              address_to=shipments,
                                              parcels=parcel)

            result = json.dumps(shipment)
            self.store_db.add(json.loads(result))
            return json.dumps(list(self.store_db.get_items()))
        return {}

    @rpc
    def shipping_parcel(self, **kwargs):
        schema_parcel = {'length': {'type': 'string'},
                         'width': {'type': 'string'},
                         'height': {'type': 'string'},
                         'distance_unit': {'type': 'string'},
                         'weight': {'type': 'string'},
                         'mass_unit': {'type': 'string'}
                        }
        return

    @rpc
    def shippments(self, **kwarg):

        return json.dumps(list(self.store_db.get_items()))
