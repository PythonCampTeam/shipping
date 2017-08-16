from shipping.db.database import StoreDB

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

a.update(address_to=address_to2)

print(a.lower(sort='zip'), '1*'*15)
print(a.upper(sort='zip'), '2*'*15)

print(max(a.get_items(), key=operator.itemgetter('zip')), '*'*15)

print(a.get_items())