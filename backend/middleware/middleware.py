from helper import sendResponse, handle_bad_request,sendResponseByStatus,getMessage
from flask import Flask ,request ,flash,session,redirect
from functools import wraps
from services.query import getOneQuery 
from helper import set_cookie_value,get_cookie_value,verifyToken
import os
            

def check_super_admin_role(cursor,redirectR):
    def decorator(func):
        @wraps(func)
        def wrapper(**kwargs):
            try:
                public_id=session.get("public_id")
                sql_check="SELECT * from  users WHERE  role = %s AND pubic_id = %s"
                values=(1,public_id)
                data=getOneQuery(cursor,sql_check,values)
                if data:
                    return func( **kwargs) 
                else:
                    raise Exception(getMessage('UNAUTHORIZED'))
            except Exception as e:
                return handle_bad_request(e)
        return wrapper
    return decorator
        


def require_authentication(func):
    @wraps(func)
    def wrapper(**kwargs):
        if "Authorization" not in request.headers:
            return sendResponseByStatus(getMessage('UNAUTHORIZED'),401)
        obj= verifyToken(request.headers['Authorization'])
        if not obj:
            return sendResponseByStatus(getMessage('UNAUTHORIZED'),401)
        return func(obj, **kwargs)
    return wrapper



def require_session_authentication(func):
    @wraps(func)
    def wrapper(**kwargs):
        public_id=session.get("public_id")
        if public_id:
            return func( **kwargs) 
        else:
            return redirect('/auth/login') 
    return wrapper


def require_session_non_authentication(func):
    @wraps(func)
    def wrapper(**kwargs):
        public_id=session.get("public_id")
        if public_id:
             return redirect('/app/dashboard') 
        else:
            return func( **kwargs) 
        
    return wrapper


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in os.getenv('ALLOWED_EXTENSIONS') 






