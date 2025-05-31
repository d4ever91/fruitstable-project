from services.query import insertQuery,getOneQuery,execQuery
from helper import handle_bad_request
import os
from helper import encrypt,getJSONData

def userMigation(mysql,cursor):
    try:
        table='CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY AUTOINCREMENT ,pubic_id TEXT NOT NULL,  first_name TEXT NOT NULL, last_name TEXT NOT NULL,  email TEXT UNIQUE NOT NULL,  password TEXT NOT NULL,role INTEGER NOT NULL,is_active INTEGER DEFAULT 1 )'
        execQuery(mysql,cursor,table,"")
        sql_check="SELECT email from users WHERE email = ?"
        values=(os.getenv('EMAIL'))
        data=getOneQuery(cursor,sql_check,values)
        if  data == None:
             sql2='INSERT into  users  (pubic_id,first_name,last_name,email,password,role) VALUES (?,?,?,?,?,?)'
             values=(os.getenv('UUID'),os.getenv('FIRST_NAME'),os.getenv('LAST_NAME'),os.getenv('EMAIL'), encrypt(os.getenv('PASSWORD'),os.getenv('CRYPTO_KEY')), os.getenv('ROLE'),)
             insertQuery(mysql,cursor,sql2,values)
             print("User migration done successfully") 
        else:
            print("User migration already done") 
    except Exception as e:
        print(e)
        return handle_bad_request(e)
    

def countryMigation(mysql,cursor):
    try:
        countries= getJSONData('countries')
        table='CREATE TABLE IF NOT EXISTS countries  ( id INTEGER PRIMARY KEY AUTOINCREMENT , name TEXT NOT NULL, code TEXT NOT NULL,  is_active INTEGER DEFAULT 1 )'
        execQuery(mysql,cursor,table,"")
        sql_check="SELECT * from  countries WHERE code = ?"
        values=("IND",)
        data=getOneQuery(cursor,sql_check,values)
        if  data == None:
             for con in countries:
                 sql2='INSERT into  countries  (name,code) VALUES (?,?)'
                 values=(con['name'],con['code'],)
                 insertQuery(mysql,cursor,sql2,values)
             print("Country migration done successfully") 
        else:
             print("Country migration already done") 
    except Exception as e:
        return handle_bad_request(e)


def customerMigration(mysql,cursor):
    try:
        table='CREATE TABLE IF NOT EXISTS customers ( id INTEGER PRIMARY KEY AUTOINCREMENT ,pubic_id TEXT NOT NULL,  first_name TEXT NOT NULL, last_name TEXT NOT NULL,  email TEXT NOT NULL,  password TEXT NOT NULL , is_active INTEGER DEFAULT 1)'
        table2='CREATE TABLE IF NOT EXISTS customer_addresses ( id INTEGER  PRIMARY KEY AUTOINCREMENT ,customer_id INTEGER , country_id INTEGER,  address_line_1 TEXT NOT NULL, address_line_2 TEXT NOT NULL,  pincode TEXT NOT NULL,  city TEXT NOT NULL )'
        execQuery(mysql,cursor,table,"")
        execQuery(mysql,cursor,table2,"")
        print("Customer migration already done") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)
    
def categoryMigration(mysql,cursor):
    try:
        table='CREATE TABLE IF NOT EXISTS categories ( id INTEGER PRIMARY KEY AUTOINCREMENT ,  name TEXT NOT NULL,  link TEXT NOT NULL ,image TEXT NOT NULL , is_active INTEGER DEFAULT 1)'
        execQuery(mysql,cursor,table,"")
        print("categories migration created") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)
    

def productMigration(mysql,cursor):
    try:
        table='CREATE TABLE IF NOT EXISTS products ( id INTEGER PRIMARY KEY AUTOINCREMENT ,  name TEXT NOT NULL,  link TEXT NOT NULL , thumbnail_image TEXT NOT NULL , full_image TEXT NOT NULL ,short_description varchar(500) ,full_description TEXT NOT NULL, qty int,  price int,  category_id INTEGER , is_active INTEGER DEFAULT 1)'
        execQuery(mysql,cursor,table,"")
        print("Products migration created") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)


def reviewMigration(mysql,cursor):
    try:
        table='CREATE TABLE IF NOT EXISTS reviews ( id INTEGER PRIMARY KEY AUTOINCREMENT ,product_id INTEGER,  name TEXT NOT NULL,  description TEXT NOT NULL , is_active INTEGER DEFAULT 1)'
        execQuery(mysql,cursor,table,"")
        print("Reviews migration created") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)
    