
from marshmallow import Schema, fields,validate

class UserSchema(Schema):
      email = fields.Email(required=True,error_messages={"required": "Email is required"})
      password = fields.String(required=True)

class UserSchemaAddUser(Schema):
      email = fields.Email(required=True,error_messages={"required": "Email is required"})
      password = fields.String(required=True)
      first_name = fields.String(required=True)
      last_name = fields.String(required=True)

class UserSchemaUpdateUser(Schema):
      email = fields.Email(required=False,error_messages={"required": "Email is required"})
      first_name = fields.String(required=False)
      last_name = fields.String(required=False)
      password = fields.String(required=False)
      is_active = fields.Boolean(required=False)


class UserSchemaDeleteUser(Schema):
      user_id = fields.Number(required=True,error_messages={"required": "User id is required"})
      
class UserModel():
      def __init__(self,email,password,first_name,role,pubic_id,last_name):
         self.first_name=first_name
         self.email=email
         self.password=password
         self.last_name=last_name
         self.role=role
         self.pubic_id=pubic_id

userSchema=UserSchema()
UserSchemaAddUser=UserSchemaAddUser()
UserSchemaUpdateUser=UserSchemaUpdateUser()
UserSchemaDeleteUser=UserSchemaDeleteUser()
