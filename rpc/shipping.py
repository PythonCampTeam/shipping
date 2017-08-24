import json
import cerberus
import shippo
from nameko.rpc import rpc
import stripe
import db.database as db
from config.settings.common import company as storehouse
from config.settings.common import security as security_settings
from config.settings import local as store_settings
from nameko.timer import timer


def traverse(response_object=None):
    """
        Function convert enter response to object
    Args:
        response_object(dict): input response
    Return:
        inst: returned instance of StripeObject
    """
    if response_object:
        return stripe.StripeObject().construct_from(response_object, '')
    return None


def pack_parcel(parcel_items=None):
    """ function used for pack parcel items from order
    Args:
        parcel_items(list): part of order with items
    Return:
        dict: Returned dict with height, width, length,
        weight, distance_unit, mass_unit
    """
    parcel_attributes = ['height', 'width', 'length', 'weight']
    parcel = {key: 0 for key in parcel_attributes}

    # TODO: take this item from order object
    parcel['distance_unit'] = "cm"
    parcel['mass_unit'] = "oz"
    if parcel_items:
        for package_item in parcel_items:
            part_parcel = package_item.parent.package_dimensions
            if part_parcel:

                print(package_item, '##' * 25, package_item.amount)
                print(package_item.parent.package_dimensions.height)
                quantity = int(package_item.quantity)
                parcel['height'] += int(part_parcel.height) * quantity
                parcel['width'] += int(part_parcel.width) * quantity
                parcel['length'] += int(part_parcel.length) * quantity
                parcel['weight'] += int(part_parcel.weight) * quantity

        return parcel
    return None


def address_validation(order=None):
    """ function for address validation, using shippo API,
    if address not valid return False and the shipping creating is fall,
     mby need raise exception
    Args:
        order(inst): input object of order from stripe callback
    Return:
        address_to(dict): Pack of valid address if address valid
        is_complete(Boolean): if address is not valid return False, or
                            returned True.

    """
    address_to = {
        "name": order.order.shipping.name,
        "street1": order.order.shipping.address.line1,
        "city": order.order.shipping.address.city,
        "state": order.order.shipping.address.state,
        "zip": order.order.shipping.address.postal_code,
        "country": order.order.shipping.address.country,
        "phone": order.order.shipping.phone,
        "email": order.order.email,
    }
    address = shippo.Address.create(**address_to)
    print(address.is_complete, '#'* 85)
    if address.is_complete:
        return True, address_to
    return False



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
    shipment_db = db.StoreDB(data_stored='shipments', data_key='object_id')
    rates_db = db.StoreDB(data_stored='rates', data_key='object_id')

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
            sorting_items = self.shipment_db.get_items()
            return json.dumps(list(sorting_items))

        if sort.startswith('-'):
            sort = sort.strip('-')
            sorting_items = self.shipment_db.sorting_items(order_by=sort,
                                                           reverse=False)
            if sorting_items:
                return json.dumps(list(sorting_items))

        sorting_items = self.shipment_db.sorting_items(order_by=sort,
                                                       reverse=True)
        if sorting_items:
            return json.dumps(list(sorting_items))
        return None

    @rpc
    def shipments_rates(self, **kwargs):
        """
            method return rates of shipment
            Kwargs:
                object_id(str): object_id string of shipment
            Return:
                dict: return data from stored db of rates
        """
        object_id = kwargs.get('object_id', None)
        if object_id:
            print('#'*15, object_id)
            rates_object = self.rates_db.get_item(object_id=object_id)
            if rates_object:
                print('#'*85, rates_object)
                return json.dumps(rates_object)

    @rpc
    def shipments_create(self, **kwargs):
        """method take order from cart service and create shipment"""
        rate = {}
        shipping_methods = []
        rate_items = {}

        delivery_estimate = {
            "type": "exact",
            "date": "2017-08-28"
        }

        order = traverse(kwargs)
        print(kwargs, '#' * 85)
        # package_dimensions
        if hasattr(order.order, 'shipping'):
            address_status, address_to = address_validation(order)
            parcel = pack_parcel(order.order['items'])
            if parcel and address_status:
                shipment = shippo.Shipment.create(
                                    address_from=store_settings.ADDRESS_FROM,
                                    address_to=address_to,
                                    parcels=[parcel],
                                    async=False
                                    )
                self.shipment_db.add(shipment)
                rate['object_id'] = shipment.object_id
                rate[shipment.object_id] = shipment.rates
                self.rates_db.add(rate)

            for rate_item in shipment.rates:
                rate_items['id'] = rate_item.object_id
                rate_items['amount'] = int(float(rate_item.amount) * 100)
                rate_items['description'] = rate_item.duration_terms
                rate_items['currency'] = rate_item.currency.lower()
                rate_items['delivery_estimate'] = delivery_estimate
                shipping_methods.append(rate_items)

            order_update = {
                    'order_update': {
                        'order_id': shipment.object_id,
                        'shipping_methods': shipping_methods
                              },
                        }

            return order_update

    @rpc
    def shipment_transaction(self, shipment_id=None, order=None):
        """
            Method wait payment information from micro-service payments
                    Kwargs:
                        order_status(str): status order changed when charge
                        order_id(str): id of order before stored in db
                    Return:
                        label(url): shipment label
        """
        shippo.api_key = 'shippo_test_55dfc05531b49ed2e711fa2cca863d72c68f87b7'
        # selected_shipping_method
        shipment_rates = []
        if order:
            print(order, '##' * 95)
        if shipment_id:
            rate = self.rates_db.get_item(object_id=shipment_id)
            for x in rate.get(shipment_id):
                print(x.get('object_id'), '##'*79)
                shipment_rates.append(x.get('object_id'))

            transaction = shippo.Transaction.create(
                rate=shipment_rates[1],
                label_file_type="PDF",
                async=False)

            # Retrieve label url and tracking number or error message
            if transaction.status == "SUCCESS":
                return transaction.label_url
            else:
                return False, transaction.messages
        return None

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

            self.temp_db.delete(object_id=address_to)
            result = shippo.Address.create(**before_res)
            self.store_db.add(result)




