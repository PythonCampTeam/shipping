import unittest
import stripe
import shippo
from nameko.testing.services import worker_factory
from shipping.rpc.shipping import ShippingRPC


ORDER2 = {'livemode': False,
          'currency': 'usd',
          'selected_shipping_method': None,
          'id': 'or_1AvltvBqraFdOKT2IDZrI0sy',
          'email': 'jenny@example.com',
          'amount': 200, 'created': 1503921571,
          'charge': None, 'external_sku_ids': None,
          'status': 'created',
          'items': [{'description': 'Jorajora', 'type': 'sku', 'parent': {'active': True, 'livemode': False, 'inventory': {'quantity': 12470, 'type': 'finite', 'value': None}, 'package_dimensions': {'width': 3.0, 'height': 5.0, 'length': 5.0, 'weight': 2.0}, 'id': 'sku_BDPHxHpBqYMftp', 'image': None, 'metadata': {}, 'object': 'sku', 'price': 200, 'created': 1502778214, 'updated': 1503565206, 'product': {'active': True, 'livemode': False, 'caption': None, 'package_dimensions': {'width': 3.0, 'height': 3.0, 'length': 3.0, 'weight': 2.0}, 'id': 'prod_BD03WMdIThFmq4', 'url': None, 'deactivate_on': [], 'object': 'product', 'skus': {'total_count': 1, 'data': [{'active': True, 'livemode': False, 'inventory': {'quantity': 12470, 'type': 'finite', 'value': None}, 'package_dimensions': {'width': 3.0, 'height': 5.0, 'length': 5.0, 'weight': 2.0}, 'id': 'sku_BDPHxHpBqYMftp', 'image': None, 'metadata': {}, 'object': 'sku', 'price': 200, 'created': 1502778214, 'updated': 1503565206, 'product': 'prod_BD03WMdIThFmq4', 'attributes': {'type': 'food', 'kg': '50'}, 'currency': 'usd'}], 'object': 'list', 'has_more': False, 'url': '/v1/skus?product=prod_BD03WMdIThFmq4&active=true'}, 'created': 1502684389, 'updated': 1503646311, 'description': 'Corm for kitty', 'shippable': True, 'attributes': ['kg', 'type'], 'metadata': {'type': 'meat', 'category': 'food', 'for': 'cats'}, 'name': 'Jorajora', 'images': []}, 'attributes': {'type': 'food', 'kg': '50'}, 'currency': 'usd'}, 'quantity': 1, 'currency': 'usd', 'amount': 200}], 'shipping': {'address': {'line1': '1092 Indian Summer Ct', 'state': 'CA', 'country': 'US', 'line2': None, 'city': 'San Jose', 'postal_code': '95122'}, 'name': 'Shippo Friend', 'phone': None, 'carrier': None, 'tracking_number': None}, 'metadata': {}, 'upstream_id': None}


class TmpOrder(object):
    selected_shipping_method = None


def tmp(object_id=None, shipment=None, shipping_method=None):
    if not hasattr(tmp, 'object_id'):
        tmp.object_id = object_id
    if not hasattr(tmp, 'shipment'):
        tmp.shipment = shipment
    if not hasattr(tmp, 'selected_shipping_method'):
        tmp.selected_shipping_method = shipping_method


class TestShippingRPC(unittest.TestCase):

    def setUp(self):
        shippo.api_key = 'shippo_test_55dfc05531b49ed2e711fa2cca863d72c68f87b7'
        self.rpc = ShippingRPC
        self.service = worker_factory(self.rpc)
        self.shipment = None
        self.object_id = None

        self.order = stripe.Order.construct_from(ORDER2, '')

    def test_service_state(self):
        """ check service_state(test method)
        AttributeError
        Raises:
            AttributeError: Raises an exception.
        """
        self.assertTrue('42' in self.service.service_state())

    def test_shipments_create(self):
        """Test for check create shipment object and create transaction """
        self.shipment = self.service.shipments_create(self.order)
        self.object_id = self.shipment.get('order_update').get('order_id')
        print(self.shipment)
        rate_item = self.shipment.get('order_update').get('shipping_methods')[0].get('id')
        tmp(object_id=self.object_id, shipment=self.shipment, shipping_method=rate_item)

    def test_shipment_transaction(self):
        """ Test for check creating label"""
        if hasattr(tmp, 'object_id'):
            label = self.service.shipment_transaction(tmp.object_id)
            self.assertTrue('pdf' in label)

    def test_torder_transaction(self):
        """ Test for check creating label"""
        if hasattr(tmp, 'object_id'):
            label = self.service.shipment_transaction(shipment_id=tmp.object_id, order=tmp)
            self.assertTrue('pdf' in label)

    def test_zshipment(self):
        """ """
        shipments = self.service.shipments(order_by='object_id')
        print(shipments)

    def test_zshipment2(self):
        """ """
        shipments = self.service.shipments(order_by=None)
        print(shipments)

    def test_zshipment3(self):
        """ """
        shipments = self.service.shipments(order_by='-object_id')
        print(shipments)

    def test_zrates(self):
        """"""
        rates = self.service.shipments_rates(object_id=tmp.object_id)

    def test_zlabel(self):
        rates = self.service.shipment_label(object_id=tmp.object_id)
