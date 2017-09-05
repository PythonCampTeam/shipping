import json
import shippo
from nameko.rpc import rpc
import stripe
import shipping.db.database as db
from shipping.config.settings.common import security as security_settings
from shipping.config.settings import local as store_settings


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
        """ this method use for testing status of service, if service work,
        will be return id : 42
        Return:
            json: simple test request from service.
        """
        return json.dumps({'id': 42})

    @rpc
    def shipments(self, order_by):
        """ method for return information about shipments in store db,
        method can return sorted information, if attribute order_by
        is not None
        Args:
            order_by(str): sorting string, supported descent if symbol
            minus in string
        Return:
            sorted list
        """

        if not order_by:

            sorting_items = self.shipment_db.sorting_items(order_by=None,
                                                           reverse=False)
            return [x.__dict__ for x in sorting_items]

        if order_by.startswith('-'):
            order_by = order_by.strip('-')
            sorting_items = self.shipment_db.sorting_items(order_by=order_by,
                                                           reverse=False)
            return [x.__dict__ for x in sorting_items]

        sorting_items = self.shipment_db.sorting_items(order_by=order_by,
                                                       reverse=True)
        return [x.__dict__ for x in sorting_items]

    @rpc
    def shipments_rates(self, object_id, object_currency):
        """
            method return rates of shipment
            Args:
                object_id(str): object_id string of shipment
                object_currency(str): currency of rates
            Return:
                dict: return data from stored db of rates
        """
        if object_id:
            rates_object = self.rates_db.get_item(object_id=object_id)

            if rates_object:
                return str(rates_object)

    @rpc
    def shipments_create(self, order=None):
        """method take order from stripe, in moment order create,
         and append information about shipping
         Args:
             order(json): json object(stripe.Order) from stripe
                        service
        Return:
            dict: returned dict object with appended information.
         """
        shipping_methods = []
        rate_items = {}

        delivery_estimate = {
            "type": "exact",
            "date": "2017-08-28"
        }
        order = traverse(order)

        # package_dimensions
        if hasattr(order, 'shipping'):
            address_status, address_to = address_validation(order)
            parcel = pack_parcel(order['items'])
            if parcel and address_status:
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

                self.rates_db.add(shipment_rates)

            for rate_item in shipment.rates:
                rate_items['id'] = rate_item.object_id
                rate_items['amount'] = int(float(rate_item.amount) * 100)
                rate_items['description'] = rate_item.servicelevel.name
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
        """Method wait payment information from micro-service payments
        Args:
            shipment_id(str): object_id from object(stripe.Order),
                            selected_shipment_method stored in db
            order(object): order object(stripe.Order)
        Return:
            label(url): shipment label, and store this label in db.
        """
        shipment_rates = []
        transaction = None
        if order and shipment_id:
            order = stripe.Order.construct_from(order, '')
            transaction = shippo.Transaction.create(
                rate=order.selected_shipping_method,
                label_file_type="PDF",
                async=False)

        if shipment_id:
            rates = self.rates_db.get_item(object_id=shipment_id)
            if rates:
                for rate_item in rates.rate_items:
                    shipment_rates.append(rate_item.object_id)

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
            return self.label_db.get_item(object_id=object_id)
        return None
