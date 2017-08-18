import json
import cerberus
import shippo
from nameko.rpc import rpc
import db.database as db
from config.settings.common import company as storehouse
from config.settings.common import security as security_settings
from nameko.timer import timer


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
    temp_db = db.StoreDB(data_stored='address_to_tmp', data_key='object_id')

    @rpc
    def service_state(self, **kwargs):
        return json.dumps({'id': 42})

    @rpc
    def shipping_add(self, **kwargs):
        shipments = json.loads(kwargs.get('address_to'))
        session = kwargs.get('session')
        parcel = kwargs.get('parcel')

        schema_shipments = {'name': {'type': 'string'},
                            'street1': {'type': 'string'},
                            'city': {'type': 'string'},
                            'state': {'type': 'string'},
                            'zip': {'type': 'string'},
                            'country': {'type': 'string'},
                            'phone': {'type': 'string'},
                            'email': {'type': 'string'}
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
            shippo.verify_ssl_certs = False
            self.temp_db.add(shipments)
        return {session: shipments}

    @rpc
    def shipping_parcel(self, **kwargs):
        schema_parcel = {'length': {'type': 'string'},
                         'width': {'type': 'string'},
                         'height': {'type': 'string'},
                         'distance_unit': {'type': 'string'},
                         'weight': {'type': 'string'},
                         'mass_unit': {'type': 'string'}
                        }
        return schema_parcel

    @rpc
    def shipments(self, **kwarg):
        sort = kwarg.get('order_by', 'name')
        if not sort:
            sorting_items = self.store_db.get_items()
            return json.dumps(list(sorting_items))

        if sort.startswith('-'):
            sort = sort.strip('-')
            sorting_items = self.store_db.sorting_items(order_by=sort,
                                                        reverse=False)
            return json.dumps(list(sorting_items))
        sorting_items = self.store_db.sorting_items(order_by=sort,
                                                    reverse=True)
        return json.dumps(list(sorting_items))

    @rpc
    def get_rates(self, **kwargs):
        """
            method return rates of shipment
            Kwargs:
                object_id(str): object_id string
                object_rates(str): currency of shipment
        """
        object_id = kwargs.get('object_id', None)
        object_rates = kwargs.get('object_rates', None)
        if object_id:
            print('#'*15, object_id)
            rates_object = self.store_db.get_item(object_id=object_id)

            return json.dumps({object_id: rates_object})

    @timer(interval=1)
    def sprinter(self):
        """
            method work infinity and check temp db, and take
            from temp db max timestamp item and create address, and delete
            item from temp store.
        Return:
             None
        """
        shippo.verify_ssl_certs = False
        shippo.api_key = security_settings.TOKEN_GOSHIPPO['LIVE_TOKEN']
        test_items = self.temp_db.get_items()

        if test_items:
            address_to = max(dict(self.temp_db.get_items()))
            before_res = self.temp_db.get_item(object_id=address_to)
            result = shippo.Address.create(**before_res)
            if result:
                self.temp_db.delete(object_id=address_to)
            print(result)
            self.store_db.add(result)




