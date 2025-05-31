from helper import getMessage,handle_bad_request
from flask import render_template,redirect,flash
import os
from middleware.middleware import allowed_file
from helper import encrypt,get_time_stamp,get_extension
from services.query import getOneQuery,insertQuery ,getAllQueryWithCondition,execQuery

def addCategory(mysql,cursor,data,files, user,page,action,method):
    try:
        result=getOneQuery(cursor,'SELECT name from categories WHERE name=%s',(data['name']))
        if  result:
            return render_template('/app/category/add_category.html',message=getMessage('CATEGORY_ALREADY_EXISTS') , success=False,user=user,data='',page=page,action=action,method=method)
        if 'image' not in files:
            flash(getMessage('CATEGORY_IMAGE_NOT_FOUND'))
        file = files['image']
        if file.filename == '':
            flash(getMessage('CATEGORY_IMAGE_NOT_FOUND'))
        if file and allowed_file(file.filename):
            ext=get_extension(file.filename)
            filename=get_time_stamp()
            current_dir = os.getcwd()
            file.save(os.path.join(current_dir + os.getenv('UPLOAD_FOLDER_CATEGORY') ,str(filename)+'.'+ext))
            name=data['name']
            qry='INSERT into  categories  (name,link,image) VALUES (%s,%s,%s)'
            values=(name,name.replace(" ", "-").lower(),str(filename)+'.'+ext)
            insertQuery(mysql,cursor,qry,values)
            result=getOneQuery(cursor,'SELECT name from categories WHERE email=%s',(data['name']))
            flash(getMessage('CATEGORY_ADDED_SUCCESSFULLY') )
            return redirect('/app/categories')
        
    except Exception as e:
         return render_template('/app/category/add_category.html',message=e.args[0], success=False,user=user,data='',page=page,action=action,method=method)
    

def updateCategory(mysql,cursor,data,files,category_id):
    try:
        if "name" in data:
            result=getOneQuery(cursor,'SELECT name from categories WHERE name=%s AND id != %s',(data['name'],category_id))
            if  result:
                return render_template('/app/category/add_category.html',message=getMessage('CATEGORY_ALREADY_EXISTS') , success=False )
        if 'image' in files:
           file = files['image']
        if file and allowed_file(file.filename):
            resu=getOneQuery(cursor,'SELECT image from categories WHERE id=%s',(category_id))
            ext=get_extension(file.filename)
            filename=get_time_stamp()
            current_dir = os.getcwd()
            file.save(os.path.join(current_dir + os.getenv('UPLOAD_FOLDER_CATEGORY') ,str(filename)+'.'+ext))
            os.remove(current_dir + os.getenv('UPLOAD_FOLDER_CATEGORY') +'/'+resu['image'])
            data['image']=str(filename)+'.'+ext
        fields=''
        for k, v in data.items():
            fields += k + '="'+v+'",'
        result=execQuery(mysql,cursor,'UPDATE  categories  SET '+fields.rstrip(',')+' WHERE id=%s',(category_id))
        flash(getMessage('CATEGORY_UPDATED_SUCCESSFULLY') )
        return redirect('/app/categories')
    except Exception as e:
        return handle_bad_request(e)
    

def activeDeativeCategory(mysql,cursor,category_id,is_active):
    try:
        result=getOneQuery(cursor,'SELECT name from categories WHERE id = %s',(category_id))
        if  result:   
            result=execQuery(mysql,cursor,'UPDATE  categories  SET is_active=%s WHERE id=%s',(is_active,category_id))
            flash(getMessage('CATEGORY_UPDATED_SUCCESSFULLY'))
            return {"updated":True }
        flash(getMessage('CATEGORY_NOT_FOUND') )
        return {"updated":False }
    except Exception as e:
        return handle_bad_request(e)
    

def deleteCategory(mysql,cursor,data):
    try:
        exist=getOneQuery(cursor,'SELECT name from categories WHERE id=%s',(data['category_id']))
        if exist:
             result=execQuery(mysql,cursor,'DELETE from categories WHERE id=%s',(data['category_id']))
             flash(getMessage('CATEGORY_DELETED_SUCCESSFULLY') )
             return redirect('/app/categories')
        raise Exception(getMessage('CATEGORY_NOT_FOUND'))
    except Exception as e:
        return handle_bad_request(e)    
    

def getCategory(cursor,categoryid):
    try:
        result=getOneQuery(cursor,'SELECT id,name,image from categories WHERE id=%s',(categoryid))
        if not result:
            raise Exception(getMessage('CATEGORY_NOT_FOUND'))
        return result
    except Exception as e:
        return handle_bad_request(e)
    

def getCategories(cursor):
    try:
        data=getAllQueryWithCondition(cursor,'SELECT id,name from categories  WHERE  is_active = %s',(True))
        return data
    except Exception as e:
        return handle_bad_request(e)
    

def getCategorysWithPagination(limit,page,cursor):
    try:
        if limit == None:
           limit = 10
        if page == None:
           page = 1
        offset=int(limit)*int(page)-int(limit)
        total=getAllQueryWithCondition(cursor,'SELECT COUNT(*) from categories',())
        data=getAllQueryWithCondition(cursor,'SELECT id,name,link,image , is_active from categories  LIMIT %s OFFSET %s',(int(limit),int(offset)))
        if not data:
            message=getMessage('CATEGORY_NOT_FOUND')
            return message
        result = { "data":data,"page":page,"limit":limit,"total":total[0]['COUNT(*)'],"totalPages":offset}
        return result
    except Exception as e:
        return handle_bad_request(e)
    

    

    
