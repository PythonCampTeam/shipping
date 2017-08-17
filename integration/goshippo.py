import json
import shippo
from config.settings.common import security as security_settings


class Shippo(object):
    """ Initialize connection on goshippo and work
    with goshippo REST API, create, delete and other.
    Methods:

        create_shipment(**kwargs)
            Args:
                address_from(dict):
                address_to(dict):
                parcels(dict):

            Return:

    """
    def __init__(self, *args, **kwargs):

        shippo.api_key = security_settings.TOKEN_GOSHIPPO['TEST_TOKEN']
        self.address_from = kwargs.get('address_from')
        self.address_to = kwargs.get('address_to')
        self.parcels = kwargs.get('parcels')

    def create_shipment(self):
        shipment = shippo.Shipment.create(
                                                address_from=self.address_from,
                                                address_to=self.address_to,
                                                parcels=[self.parcels],
                                                async=False
                                                )
        return json.dumps(shipment)

    def create_transaction(self, **kwargs):
        shipment = kwargs.get('shipment')
        rate = shipment.rates[0]

        # Purchase the desired rate.
        transaction = shippo.Transaction.create(
                                            rate=rate.object_id,
                                            label_file_type="PDF",
                                            async=False)

        # Retrieve label url and tracking number or error message

        if transaction.status == "SUCCESS":
            print(transaction.label_url)
            print(transaction.tracking_number)
        else:
            print(transaction.messages)
        return transaction

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
#test = Shippo(address_from=address_from, parcels=parcel, address_to=address_to)
#test1 = Shippo(address_from=address_from, parcels=parcel, address_to=address_to)
#ship = test.create_shipment()
#print(ship)