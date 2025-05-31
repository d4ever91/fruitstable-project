
from marshmallow import Schema, fields


class ProductSchemaAddproduct(Schema):
      name = fields.String(required=True,error_messages={"required": "Name is required"})
      category_id = fields.Integer(required=True)
      thumbnail_image = fields.Raw(type='file')
      full_image = fields.Raw(type='file')
      qty =  fields.Integer(required=True)
      price =  fields.Number(required=True)
      short_description =  fields.String(required=True)
      full_description =  fields.String(required=True)

class ProductSchemaUpdateproduct(Schema):
      name = fields.String(required=False)
      is_active= fields.Boolean(required=False)
      category_id = fields.Integer(required=False)
      thumbnail_image = fields.Raw(type='file')
      full_image = fields.Raw(type='file')
      qty =  fields.Integer(required=False)
      price =  fields.Number(required=False)
      short_description =  fields.String(required=False)
      full_description =  fields.String(required=False)


class ProductSchemaDeleteproduct(Schema):
      product_id = fields.Integer(required=True,error_messages={"required": "product id is required"})
      
class ProductModel():
      def __init__(self,name,link,thumbnail_image, full_image,short_description,full_description,qty,price,is_active):
         self.name=name
         self.link=link
         self.thumbnail_image=thumbnail_image
         self.full_image=full_image
         self.short_description=short_description
         self.full_description=full_description
         self.qty=qty
         self.is_active=is_active
         self.price=price

ProductSchemaAddproduct=ProductSchemaAddproduct()
ProductSchemaUpdateproduct=ProductSchemaUpdateproduct()
ProductSchemaDeleteproduct=ProductSchemaDeleteproduct()