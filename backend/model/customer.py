
from marshmallow import Schema, fields,validate

class CustomerSchema(Schema):
      email = fields.Email(required= True,error_messages={"required": "Email is required"})
      password = fields.String(required=True)

class CustomerSchemaAddCustomer(Schema):
      email = fields.Email(required=True,error_messages={"required": "Email is required"})
      password = fields.String(required=True)
      first_name = fields.String(required=True)
      last_name = fields.String(required=True)


class CustomerSchemaUpdateCustomer(Schema):
      email = fields.Email(required=False,error_messages={"required": "Email is required"})
      first_name = fields.String(required=False)
      last_name = fields.String(required=False)
      password = fields.String(required=False)
      is_active= fields.Bool(required=False)

class CustomerSchemaDeleteCustomer(Schema):
      customer_id = fields.Number(required=True,error_messages={"required": "Customer id is required"})


class CustomerModel():
      def __init__(self,email,password,first_name,pubic_id,last_name,is_active):
         self.first_name=first_name
         self.email=email
         self.password=password
         self.last_name=last_name
         self.pubic_id=pubic_id
         self.is_active=is_active

CustomerSchema=CustomerSchema()
CustomerSchemaAddCustomer=CustomerSchemaAddCustomer()
CustomerSchemaUpdateCustomer=CustomerSchemaUpdateCustomer()
CustomerSchemaDeleteCustomer=CustomerSchemaDeleteCustomer()
