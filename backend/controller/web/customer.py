from helper import getMessage,sendResponse,handle_bad_request
from flask import render_template,redirect,flash
import uuid
import os
from helper import encrypt
from services.query import getOneQuery,getAllQueryWithCondition ,execQuery,insertQuery
    
def addCustomer(mysql,cursor,data):
    try:
        result=getOneQuery(cursor,'SELECT email from customers WHERE email=%s',(data['email']))
        if not result:
             qry='INSERT into  customers  (first_name,last_name,email,pubic_id,password) VALUES (%s,%s,%s,%s,%s)'
             values=(data['first_name'],data['last_name'],data['email'],uuid.uuid4(), encrypt(data['password'],os.getenv('CRYPTO_KEY')))
             insertQuery(mysql,cursor,qry,values)
             result=getOneQuery(cursor,'SELECT email from customers WHERE email=%s',(data['email']))
             return render_template('/app/customer/add_customer.html',message=getMessage('customer_ADDED_SUCCESSFULLY') ,success=True)
        return render_template('/app/customer/add_customer.html',message=getMessage('EMAIL_ALREADY_EXISTS') , success=False)
    except Exception as e:
        return handle_bad_request(e)
    
def getCustomer(cursor,customerid):
    try:
        result=getOneQuery(cursor,'SELECT id,first_name,last_name,email from customers WHERE id=%s',(customerid))
        if not result:
            raise Exception(getMessage('customer_NOT_FOUND'))
        return result
    except Exception as e:
        return handle_bad_request(e)
    

def getCustomers(cursor):
    try:
        result=getAllQueryWithCondition(cursor,'SELECT id,email,first_name,last_name,is_active from customers',())
        if not result:
            message=getMessage('customer_NOT_FOUND')
            return message
        return result
    except Exception as e:
        return handle_bad_request(e)
    
    
def updateCustomer(mysql,cursor,data,customer_id):
    try:
        if "email" in data:
            result=getOneQuery(cursor,'SELECT email from customers WHERE email=%s AND id != %s',(data['email'],customer_id))
            if   result:
                raise Exception(getMessage('EMAIL_ALREADY_EXISTS'))
        fields=''
        for k, v in data.items():
            if k == 'password':
                v = encrypt(v,os.getenv('CRYPTO_KEY'))
            fields += k + '="'+v+'",'
        result=execQuery(mysql,cursor,'UPDATE  customers  SET '+fields.rstrip(',')+' WHERE id=%s',(customer_id))
        flash(getMessage('CUSTOMER_UPDATED_SUCCESSFULLY') )
        return redirect('/app/customers')
    except Exception as e:
        return handle_bad_request(e)
    
def getCustomersWithPagination(limit,page,cursor):
    try:
        if limit == None:
           limit = 10
        if page == None:
           page = 1
        offset=int(limit)*int(page)-int(limit)
        total=getAllQueryWithCondition(cursor,'SELECT COUNT(*) from customers',())
        data=getAllQueryWithCondition(cursor,'SELECT id,email,first_name,last_name,is_active from customers  LIMIT %s OFFSET %s',(int(limit),int(offset)))
        if not data:
            message=getMessage('CUSTOMER_NOT_FOUND')
            return message
        result = { "data":data,"page":page,"limit":limit,"total":total[0]['COUNT(*)'],"totalPages":offset}
        return result
    except Exception as e:
        return handle_bad_request(e)
    
def activeDeativeCustomer(mysql,cursor,customer_id,is_active):
    try:
        result=getOneQuery(cursor,'SELECT email from customers WHERE id = %s',(customer_id))
        if  result:   
            result=execQuery(mysql,cursor,'UPDATE  customers  SET is_active=%s WHERE id=%s',(is_active,customer_id))
            flash(getMessage('CUSTOMER_UPDATED_SUCCESSFULLY'))
            return {"updated":True }
        flash(getMessage('CUSTOMER_NOT_FOUND') )
        return {"updated":False }
    except Exception as e:
        return handle_bad_request(e)
    

def deleteCustomer(mysql,cursor,data):
    try:
        exist=getOneQuery(cursor,'SELECT email from customers WHERE id=%s',(data['customer_id']))
        if exist:
             execQuery(mysql,cursor,'DELETE from customers WHERE id=%s',(data['customer_id']))
             flash(getMessage('CUSTOMER_DELETED_SUCCESSFULLY') )
             return redirect('/app/customers')
        raise Exception(getMessage('CUSTOMER_NOT_FOUND'))
    except Exception as e:
        return handle_bad_request(e)   
    