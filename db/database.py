import operator
import time


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
    def __init__(self, **kwargs):
        self.db = {}
        self.data_stored = kwargs.get('data_stored')
        self.data_key = kwargs.get('data_key')

    def add(self, other):
        object_id = other.get(self.data_key, str(time.time()))
        if isinstance(other, dict):
            if other not in self.db.items():
                self.db[object_id] = other
        return self

    def update(self, **kwargs):
        item = kwargs.get(self.data_stored)
        object_id = item.get(self.data_key)
        if self.db[object_id]:
            self.db[object_id].update(item)
        return self

    def delete(self, **kwargs):
        object_id = kwargs.get(self.data_key)
        if any(object_id in _ for _ in self.db):
            del self.db[object_id]
        return self.db

    def sorting_items(self, order_by='name', reverse=False):
        if any(order_by in _ for _ in self.db.values()):
            return sorted(self.db.values(),
                          key=operator.itemgetter(order_by),
                          reverse=reverse)
        return None

    def get_item(self, *args, **kwargs):
        item = kwargs.get('object_id')
        try:
            result = self.db[item]
            return result
        except KeyError:
            pass
        return None

    def get_items(self):
        return self.db.items()

