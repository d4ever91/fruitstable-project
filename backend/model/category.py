
from marshmallow import Schema, fields

class CategorySchemaAddcategory(Schema):
      name = fields.String(required=True)
      image = fields.Raw(type='file')

class CategorySchemaUpdatecategory(Schema):
      name = fields.String(required=False)
      image = fields.String(required=False)
      is_active = fields.Boolean(required=False)
      
class CategorySchemaDeletecategory(Schema):
      category_id = fields.Number(required=True,error_messages={"required": "category id is required"})
      
class CategoryModel():
      def __init__(self,name,link,image):
         self.name=name
         self.link=link
         self.image=image

CategorySchemaAddcategory=CategorySchemaAddcategory()
CategorySchemaUpdatecategory=CategorySchemaUpdatecategory()
CategorySchemaDeletecategory=CategorySchemaDeletecategory()