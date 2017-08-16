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
    def __init__(self, **kwargs):
        self.db = {}
        self.data_stored = kwargs.get('data_stored')
        self.data_key = kwargs.get('data_key')
#        print(self.data_key, self.data_stored)

    def add(self, other):
        object_id = other.get(self.data_key)
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

    def lower(self, **kwargs):
        sort_value = kwargs.get('sort')
        if any(sort_value in _ for _ in self.db.values()):
            return sorted(self.db.values(),
                          key=operator.itemgetter(sort_value))

    def upper(self, **kwargs):
        sort_value = kwargs.get('sort')
        if any(sort_value in _ for _ in self.db.values()):
            return sorted(self.db.values(),
                          key=operator.itemgetter(sort_value),
                          reverse=True)

    def get_item(self, **kwargs):
        item = kwargs.get('object_id')
        return self.db[item]

    def get_items(self):
        return self.db.values()

