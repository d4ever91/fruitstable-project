from helper import getMessage,sendResponse,handle_bad_request,set_cookie_value,decrypt,generateToken
from flask import render_template,session,redirect,flash
import os
import uuid
from helper import encrypt
from services.query import getOneQuery,insertQuery ,getAllQueryWithCondition,execQuery

def userLogin(cursor,data):
    try:
        values=(data['email'])
        result=getOneQuery(cursor,'SELECT * from users WHERE email=%s',values)
        if not result:
             return render_template('/auth/login.html',email=getMessage('EMAIL_INCORRECT'))
        if decrypt(result['password'],os.getenv('CRYPTO_KEY')) != data['password']:
            return render_template('/auth/login.html',password=getMessage('PASSWORD_INCORRECT'))
        #token=generateToken(result['pubic_id'])
        session['public_id']=result['pubic_id']
        return redirect('/app/dashboard')
    except Exception as e:
        return handle_bad_request(e)
    

def getCurrentUser(cursor):
    public_id=session.get("public_id")
    user=getOneQuery(cursor,'SELECT * from users WHERE pubic_id=%s',(public_id))
    return user

def addUser(mysql,cursor,data,user,page,action,method):
    try:
        result=getOneQuery(cursor,'SELECT email from users WHERE email=%s',(data['email']))
        if not result:
             qry='INSERT into  users  (first_name,last_name,email,pubic_id,role,password) VALUES (%s,%s,%s,%s,%s,%s)'
             values=(data['first_name'],data['last_name'],data['email'],uuid.uuid4(),2, encrypt(data['password'],os.getenv('CRYPTO_KEY')))
             insertQuery(mysql,cursor,qry,values)
             result=getOneQuery(cursor,'SELECT email from users WHERE email=%s',(data['email']))
             flash(getMessage('USER_ADDED_SUCCESSFULLY') )
             return redirect('/app/users')
        return render_template('/app/user/add_user.html',message=getMessage('EMAIL_ALREADY_EXISTS') , success=False,user=user,data='',page=page,action=action,method=method)
    except Exception as e:
        return handle_bad_request(e)
    

def updateUser(mysql,cursor,data,user_id):
    try:
        print(data)
        if "email" in data:
            result=getOneQuery(cursor,'SELECT email from users WHERE email=%s AND id != %s',(data['email'],user_id))
            if  result:
                return render_template('/app/user/add_user.html',message=getMessage('EMAIL_ALREADY_EXISTS') , success=False )
        fields=''
        for k, v in data.items():
            if k == 'password':
                v = encrypt(v,os.getenv('CRYPTO_KEY'))
            fields += k + '="'+v+'",'
        result=execQuery(mysql,cursor,'UPDATE  users  SET '+fields.rstrip(',')+' WHERE id=%s',(user_id))
        flash(getMessage('USER_UPDATED_SUCCESSFULLY') )
        return redirect('/app/users')
    except Exception as e:
        return handle_bad_request(e)
    

def activeDeativeUser(mysql,cursor,user_id,is_active):
    try:
        result=getOneQuery(cursor,'SELECT email from users WHERE id = %s',(user_id))
        if  result:   
            result=execQuery(mysql,cursor,'UPDATE  users  SET is_active=%s WHERE id=%s',(is_active,user_id))
            flash(getMessage('USER_UPDATED_SUCCESSFULLY'))
            return {"updated":True }
        flash(getMessage('USER_NOT_FOUND') )
        return {"updated":False }
    except Exception as e:
        return handle_bad_request(e)
    

def deleteUser(mysql,cursor,data):
    try:
        exist=getOneQuery(cursor,'SELECT email from users WHERE id=%s AND role!=%s',(data['user_id'],os.getenv('ROLE')))
        if exist:
             result=execQuery(mysql,cursor,'DELETE from users WHERE id=%s',(data['user_id']))
             flash(getMessage('USER_DELETED_SUCCESSFULLY') )
             return redirect('/app/users')
        raise Exception(getMessage('USER_NOT_FOUND'))
    except Exception as e:
        return handle_bad_request(e)    
    

def getUser(cursor,userid):
    try:
        result=getOneQuery(cursor,'SELECT id,first_name,last_name,email from users WHERE id=%s',(userid))
        if not result:
            raise Exception(getMessage('USER_NOT_FOUND'))
        return result
    except Exception as e:
        return handle_bad_request(e)
    

def getUsersWithPagination(limit,page,cursor):
    try:
        if limit == None:
           limit = 10
        if page == None:
           page = 1
        offset=int(limit)*int(page)-int(limit)
        total=getAllQueryWithCondition(cursor,'SELECT COUNT(*) from users WHERE role != %s',(os.getenv('ROLE')))
        data=getAllQueryWithCondition(cursor,'SELECT id,email,first_name,last_name,role,is_active from users WHERE role != %s LIMIT %s OFFSET %s',(os.getenv('ROLE'),int(limit),int(offset)))
        if not data:
            message=getMessage('USER_NOT_FOUND')
            return message
        result = { "data":data,"page":page,"limit":limit,"total":total[0]['COUNT(*)'],"totalPages":offset}
        return result
    except Exception as e:
        return handle_bad_request(e)
    

    

    
