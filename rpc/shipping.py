import json
import cerberus
import shippo
from nameko.rpc import rpc
import stripe
import db.database as db
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
        "name": order.shipping.name,
        "street1": order.shipping.address.line1,
        "city": order.shipping.address.city,
        "state": order.shipping.address.state,
        "zip": order.shipping.address.postal_code,
        "country": order.shipping.address.country,
        "phone": order.shipping.phone,
        "email": order.email,
    }
    address = shippo.Address.create(**address_to)
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
    shippo.verify_ssl_certs = False
    shippo.api_key = security_settings.TOKEN_GOSHIPPO['TEST_TOKEN']
    shipment_db = db.StoreDB(data_stored='shipments', data_key='object_id')
    rates_db = db.StoreDB(data_stored='rates', data_key='object_id')
    label_db = db.StoreDB(data_stored='labels', data_key='object_id')

    @rpc
    def service_state(self, **kwargs):
        return json.dumps({'id': 42})

    @rpc
    def shipments(self, order_by):

        if not order_by:

            sorting_items = self.shipment_db.sorting_items(order_by=None,
                                                           reverse=False)
            return str(sorting_items)
        if order_by.startswith('-'):
            order_by = order_by.strip('-')
            sorting_items = self.shipment_db.sorting_items(order_by=order_by,
                                                           reverse=False)
            return str(sorting_items)

        sorting_items = self.shipment_db.sorting_items(order_by=order_by,
                                                       reverse=True)
        return str(sorting_items)

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
            rates_object = self.rates_db.get_item(object_id=object_id)
            if rates_object:
                return str(rates_object)

    @rpc
    def shipments_create(self, order=None):
        """method take order from cart service and create shipment"""
        shipping_methods = []
        rate_items = {}

        delivery_estimate = {
            "type": "exact",
            "date": "2017-08-28"
        }
        # take order for testing
        # print('###', order, '###')
        order = traverse(order)

        # package_dimensions
        if hasattr(order, 'shipping'):
            address_status, address_to = address_validation(order)
            parcel = pack_parcel(order['items'])
            if parcel and address_status:
                # TODO: add instance ItemField

                shipment = shippo.Shipment.create(
                                    address_from=store_settings.ADDRESS_FROM,
                                    address_to=address_to,
                                    parcels=[parcel],
                                    async=False
                                    )
                shipment_field = db.ItemShipping(object_id=shipment.object_id,
                                                 address_to=address_to)

                shipment_rates = db.ItemRates(object_id=shipment.object_id,
                                              rates=shipment.rates)

                self.shipment_db.add(shipment_field)

#                rate['object_id'] = shipment.object_id
#                rate[shipment.object_id] = shipment.rates

                self.rates_db.add(shipment_rates)

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
        shipment_rates = []
        transaction = None
        if order and shipment_id:

            transaction = shippo.Transaction.create(
                rate=order.selected_shipping_method,
                label_file_type="PDF",
                async=False)

        if shipment_id:
            rate = self.rates_db.get_item(object_id=shipment_id)
            for x in rate.rate_items:
                shipment_rates.append(x.get('object_id'))

            transaction = shippo.Transaction.create(
                rate=shipment_rates[1],
                label_file_type="PDF",
                async=False)

            # Retrieve label url and tracking number or error message
        if hasattr(transaction, 'status'):
            if transaction.status == "SUCCESS":
                shipment_label = db.ItemLabel(object_id=shipment_id,
                                              label_url=transaction.label_url)
                self.label_db.add(shipment_label)
                return transaction.label_url
            else:
                return False, transaction.messages
        return None

    @rpc
    def shipment_label(self, object_id=None):
        """ method return label of shipment
            Args:
                object_id(str): id of shipment object
            Return:
                label_url(str): returned label of shipment
        """
        if object_id:
            return str(self.label_db.get_item(object_id=object_id))
        return None
