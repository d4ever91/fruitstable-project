from services.query import insertQuery,getOneQuery,execQuery
from helper import handle_bad_request
import os
from helper import encrypt,getJSONData

def userMigation(mysql,cursor):
    try:
        # table='CREATE TABLE users ( id int PRIMARY KEY AUTO_INCREMENT ,pubic_id varchar(255),  first_name varchar(255), last_name varchar(255),  email varchar(255),  password varchar(255) , role int)'
        # execQuery(mysql,cursor,table)
        table='ALTER TABLE users ADD is_active int DEFAULT 1'
        execQuery(mysql,cursor,table)
        # sql_check="SELECT email from  users WHERE email = %s"
        # values=(os.getenv('EMAIL'))
        # data=getOneQuery(cursor,sql_check,values)
        # if  data == None:
        #      sql2='INSERT into  users  (pubic_id,first_name,last_name,email,password,role) VALUES (%s,%s,%s,%s,%s,%s)'
        #      values=(os.getenv('UUID'),os.getenv('FIRST_NAME'),os.getenv('LAST_NAME'),os.getenv('EMAIL'), encrypt(os.getenv('PASSWORD'),os.getenv('CRYPTO_KEY')), os.getenv('ROLE'))
        #      insertQuery(mysql,cursor,sql2,values)
        #      print("User migration done successfully") 
        # else:
        print("User migration already done") 
    except Exception as e:
        print(e)
        return handle_bad_request(e)
    

def countryMigation(mysql,cursor):
    try:
        countries= getJSONData('countries')
#        table='CREATE TABLE countries ( id int PRIMARY KEY AUTO_INCREMENT , name varchar(255), code varchar(255),  is_active int DEFAULT 1 )'
 #       execQuery(mysql,cursor,table)
        sql_check="SELECT * from  countries WHERE code = %s"
        values=("IND")
        data=getOneQuery(cursor,sql_check,values)
        if  data == None:
             for con in countries:
                 sql2='INSERT into  countries  (name,code) VALUES (%s,%s)'
                 values=(con['name'],con['code'])
                 insertQuery(mysql,cursor,sql2,values)
             print("Country migration done successfully") 
        else:
             print("Country migration already done") 
    except Exception as e:
        print(e)
        return handle_bad_request(e)


def customerMigration(mysql,cursor):
    try:
        table='CREATE TABLE customers ( id int PRIMARY KEY AUTO_INCREMENT ,pubic_id varchar(255),  first_name varchar(255), last_name varchar(255),  email varchar(255),  password varchar(255) , is_active int DEFAULT 1)'
        table2='CREATE TABLE customer_addresses ( id int PRIMARY KEY AUTO_INCREMENT ,customer_id int , country_id int,  address_line_1 varchar(255), address_line_2 varchar(255),  pincode varchar(255),  city varchar(255) )'
        execQuery(mysql,cursor,table)
        execQuery(mysql,cursor,table2)
        print("Customer migration already done") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)
    
def categoryMigration(mysql,cursor):
    try:
        table='CREATE TABLE categories ( id int PRIMARY KEY AUTO_INCREMENT ,  name varchar(255),  link varchar(255) ,image varchar(255) , is_active int DEFAULT 1)'
        execQuery(mysql,cursor,table)
        print("categories migration created") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)
    

def productMigration(mysql,cursor):
    try:
        table='CREATE TABLE products ( id int PRIMARY KEY AUTO_INCREMENT ,  name varchar(255),  link varchar(255) , thumbnail_image varchar(255) , full_image varchar(255) ,short_description varchar(500) ,full_description varchar(2500), qty int,  price int,  category_id int , is_active int DEFAULT 1)'
        execQuery(mysql,cursor,table)
        print("Products migration created") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)


def reviewMigration(mysql,cursor):
    try:
        table='CREATE TABLE reviews ( id int PRIMARY KEY AUTO_INCREMENT ,product_id int,  name varchar(255),  description varchar(255) , is_active int DEFAULT 1)'
        execQuery(mysql,cursor,table)
        print("Reviews migration created") 

    except Exception as e:
        print(e)
        return handle_bad_request(e)
    