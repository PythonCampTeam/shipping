

address_to = {
    "object_id": "ab9c8c59d6a6485b8e8f262cde334d31",
    "shipment": "5fcb12b061bd4f8a98af57c37b66fe76",
    "name": "Mr. Hippo",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
}
address_to1 = {
    "object_id": "ab9c8c59d6a6485b8e8f262cde334d31",
    "shipment": "196675e7714542f8b0b16a75682bb504",
    "name": "Mr. Hippo",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "4",
    "country": "US",
    "phone": "+1 555 341 9393",
}

address_to2 = {
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
a = StoreDB(data_stored='address_to', data_key='object_id')
print(a)
a.add(address_to1)
a.add(address_to2)
a.update(object_id='ab9c8c59d6a6485b8e8f262cde334d31', item=address_to2)

print(a.sorting_items(order_by='zip', reverse=False), '1*'*15)
#print(a.sorting_items(sort='zip'), '2*'*15)

#print(max(a.get_items(), key=operator.itemgetter('zip')), '*'*15)

#print(a.get_items())

#///////////

address_to = {
    "object_id": "ab9c8c59d6a6485b8e8f262cde334d31",
    "shipment": "5fcb12b061bd4f8a98af57c37b66fe76",
    "name": "Mr. Hippo",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
}
address_to1 = {}
address_to1['object_id'] = 'ab9c8c59d6a6485b8e8f262cde334d31'
address_to1['ab9c8c59d6a6485b8e8f262cde334d31'] = {
    "object_id": "ab9c8c59d6a6485b8e8f262cde334d31",
    "shipment": "196675e7714542f8b0b16a75682bb504",
    "name": "Mr. Hippo",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "4",
    "country": "US",
    "phone": "+1 555 341 9393",
}

address_to2 = {}
address_to2['ab9c8c59d6a6485b8e8f262cde334d32'] = {
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


a1 = ItemField(object_id='12313', address_to=address_to)
a2 = ItemField(object_id='1223', address_to=address_to)
a3 = ItemField(object_id='1233', address_to=address_to)
a4 = ItemField(object_id='11323', address_to=address_to)
a = StoreDB(data_stored='address_to', data_key='object_id')
inst = [a1, a2, a3, a4]
print(a)
[a.add(x) for x in inst]
d2 = ObjDict(address_to)
print(a.get_items())
print(a1.address_to.city)
#a.add(address_to2)
#a.update(object_id='ab9c8c59d6a6485b8e8f262cde334d31', item=address_to2)

print(a.sorting_items(order_by='address_to.name', reverse=False), '1*'*15)
#print(a.sorting_items(sort='zip'), '2*'*15)

#print(max(a.get_items(), key=operator.itemgetter('zip')), '*'*15)

#print(a.get_items())