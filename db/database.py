import abc
import json
import operator


class StoreDB(object):
    """
        class for storing and sorting data from micro services
        Methods:
            __iadd__: function append store
                Args:
                    other(dict): information to save in db
                Return:
                    self
            update(dict):
                Args:
                     address_to(dict): shipment address information
                Return:
                    self.db
            delete(dict):
                Args:
                    address_to(dict): shipment address information for delete
                Return:
                    self.db(list)
            lower:
                Args:
                    sort(str): string for sorted lower output from db
                Return:
                    list
            upper:
                Args:
                    sort(str): string for upper sorted output from db
                Return:
                    list
            get:
                Args:
                    object_id(str): string of object id
                Return:
                    dict
    """
    def __init__(self, data_stored=None, data_key=None):
        self.db = {}
        self.data_stored = data_stored
        self.data_key = data_key

    def add(self, item):
        if item.object_id not in self.db.items():
            self.db[item.object_id] = item
        return self

    def update(self, object_id=None, item=None):
        if self.db[object_id]:
            self.db[object_id].update(item)
        return self

    def delete(self, object_id):
        del self.db[object_id]
        return self.db

    def sorting_items(self, order_by='object_id', reverse=False):
        if order_by:
            return sorted(self.db.values(),
                          key=operator.attrgetter(order_by),
                          reverse=reverse)
        else:
            return sorted(self.db.values(),
                          key=operator.attrgetter(self.data_key),
                          reverse=reverse)

    def get_item(self, object_id):
        return self.db.get(object_id)

    def get_items(self):
        return self.db.items()


class ItemField(abc.ABC):
    """ Class for store item in db
     args:
        object_id(str): id of item shipments, rates, order
        address_to(dict): dict element from stripe, goshippo response
    return:
        instance: returned self item
    """
    def __init__(self, object_id):
        self. object_id = object_id

    @property
    def item(self):
        return self


class ObjDict(dict):
    """ class make from dict attributes values"""
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


class ItemShipping(ItemField):
    """class for store shipments in db """
    def __init__(self, object_id, address_to):
        super().__init__(object_id)
        self.address_to = ObjDict(address_to)


class ItemRates(ItemField):
    """ class for store rates in db """
    def __init__(self, object_id, rates):
        super().__init__(object_id)
        self.rate_items = [ObjDict(rate) for rate in rates]


class ItemLabel(ItemField):
    """ class for store labels in db """
    def __init__(self, object_id, label_url):
        super().__init__(object_id)
        self.label_url = label_url
