
from marshmallow import Schema, fields,validate

class CountrySchema(Schema):
      name = fields.String(required=True)
      code = fields.String(required=True)
      
class CountrySchemaCountryUpdate(Schema):
      is_active = fields.Bool(required=True)

class CountryModel():
      def __init__(self,name,code,is_active):
         self.name=name
         self.code=code
         self.is_active=is_active

CountrySchema=CountrySchema()
CountrySchemaCountryUpdate=CountrySchemaCountryUpdate()
