from helper import getMessage,sendResponse,handle_bad_request,set_cookie_value,decrypt,generateToken
import os
import uuid
from helper import encrypt
from services.query import getOneQuery,insertQuery 

def customerLogin(cursor,data):
    try:
        values=(data['email'],)
        result=getOneQuery(cursor,'SELECT * from customers WHERE email=?',values)
        if not result:
              raise Exception(getMessage('EMAIL_INCORRECT'))
        if decrypt(result['password'],os.getenv('CRYPTO_KEY')) != data['password']:
             raise Exception(getMessage('PASSWORD_INCORRECT'))
        if result['is_active'] == False:
            raise Exception(getMessage('CUSTOMER_IS_NOT_ACTIVE'))
        token=generateToken(result['pubic_id'])
        return sendResponse(getMessage('USER_LOGGED_SUCCESSFULLY'),{"token":token,
                "user":{"first_name":result['first_name'],"last_name":result['last_name']} })
    except Exception as e:
        return handle_bad_request(e)

def customerRegister(mysql,cursor,data):
    try:
        result=getOneQuery(cursor,'SELECT email from customers WHERE email=?',(data['email'],))
        if  result:
             raise Exception(getMessage('EMAIL_ALREADY_EXISTS'))
        else:
            qry='INSERT into  customers  (first_name,last_name,email,pubic_id,password) VALUES (?,?,?,?,?)'
            values=(data['first_name'],data['last_name'],data['email'],str(uuid.uuid4()),encrypt(data['password'],os.getenv('CRYPTO_KEY')))
            insertQuery(mysql,cursor,qry,values)
            result=getOneQuery(cursor,'SELECT email from customers WHERE email=?',(data['email'],))
            columns = [column[0] for column in cursor.description]
            result = [dict(zip(columns, row)) for row in result]
            return sendResponse(getMessage('USER_REGISTER_SUCCESSFULLY'),result)
    except Exception as e:
        return handle_bad_request(e)
    

    
