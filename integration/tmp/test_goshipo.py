from shipping.integration.tmp.goshippo import Shippo

address_from = {
    "name":"Mr Hippo",
    "company":"Shippo",
    "street1":"965 Mission St",
    "city":"San Francisco",
    "state":"CA",
    "zip":"94117",
    "country":"US",
    "phone":"+1 555 341 9393",
}

# Example address_to object dict
# The complete refence for the address object is available here: https://goshippo.com/docs/reference#addresses

address_to = {
    "name": "Mr. Hippo",
    "street1": "1092 Indian Summer Ct",
    "city": "San Jose",
    "state": "CA",
    "zip": "95122",
    "country": "US",
    "phone": "+1 555 341 9393",
}

# parcel object dict
# The complete reference for parcel object is here: https://goshippo.com/docs/reference#parcels
parcel = {
    "length": "5",
    "width": "5",
    "height": "5",
    "distance_unit": "in",
    "weight": "2",
    "mass_unit": "lb",
}

test = Shippo(address_from=address_from, parcels=parcel, address_to=address_to)
test1 = Shippo(address_from=address_from, parcels=parcel, address_to=address_to)
ship = test.create_shipment()
ship1 = test1.create_address()
#print(ship.rates[0], '#'*25)
#print(ship1.rates[0], '#'*25)

#print(test.create_transaction(shipment=ship))
#print(test)