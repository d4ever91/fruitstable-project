
from marshmallow import Schema, fields,validate

class CustomerSchema(Schema):
      country_id = fields.Number(required=True)
      address_line_1 = fields.String(required=True)
      address_line_2 = fields.String(required=True)
      pincode = fields.String(required=True)
      city = fields.String(required=True)

class CustomerAddAddressSchema(Schema):
      country_id = fields.Number(required=True)
      address_line_1 = fields.String(required=True)
      address_line_2 = fields.String(required=True)
      pincode = fields.String(required=True)
      city = fields.String(required=True)


class CustomerSchemaUpdateCustomerAddress(Schema):
      country_id = fields.Number(required=False)
      address_line_1 = fields.String(required=False)
      address_line_2 = fields.String(required=False)
      pincode = fields.String(required=False)
      city = fields.String(required=False)


class CustomerModel():
      def __init__(self,customer_id,country_id, email,password,first_name,pubic_id,last_name):
         self.customer_id=customer_id
         self.country_id=country_id
         self.first_name=first_name
         self.email=email
         self.password=password
         self.last_name=last_name
         self.pubic_id=pubic_id

CustomerSchema=CustomerSchema()
CustomerAddAddressSchema=CustomerAddAddressSchema()
CustomerSchemaUpdateCustomerAddress=CustomerSchemaUpdateCustomerAddress()
