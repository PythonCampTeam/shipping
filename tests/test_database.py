import unittest
from shipping.db import database as db

ADDRESS = {
    "object_id": "ab9c8c59d6a6485b8e8f262cde334d32",
    "shipment": "196675e7714542f8b0b16a75682bb504",
    "name": "Mr. Hippo",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "412",
    "country": "US",
    "phone": "+1 555 341 9393",
}


class TestStoreDB(unittest.TestCase):

    def setUp(self):
        self.test_db = db.StoreDB(data_stored='labels', data_key='object_id')
        self.address = ADDRESS
        self.field = db.ItemShipping(object_id='12', address_to=self.address)

    def test_add(self):
        """ check service_state(test method)
        AttributeError
        Raises:
            AttributeError: Raises an exception.
        """
        self.test_db.add(self.field)

    def test_delete(self):
        """ check service_state(test method)
        AttributeError
        Raises:
            AttributeError: Raises an exception.
        """
        self.test_db.add(self.field)
        self.test_db.delete('12')

    def test_sorting(self):
        self.test_db.add(self.field)
        print('##', self.test_db.sorting_items(order_by=None))
        print('##', self.test_db.sorting_items(order_by='object_id'))

    def test_get_item(self):
        self.test_db.add(self.field)
        print('##', self.test_db.get_item(object_id='12'))
        print('##', self.test_db.get_items())

    def test_item_rates(self):
        rates = db.ItemRates(object_id='12', rates=[{'name': 1}, {'name': 2}])

    def test_item_label(self):
        label = db.ItemLabel(object_id='12', label_url='url_pdf')

    def test_objdict(self):
        obj_dict = db.ObjDict(self.address)
        self.assertTrue(isinstance(obj_dict, db.ObjDict))
