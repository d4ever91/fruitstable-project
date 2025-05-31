from helper import getMessage,handle_bad_request
from flask import render_template,redirect,flash
import os
from middleware.middleware import allowed_file
from helper import encrypt,get_time_stamp,get_extension
from services.query import getOneQuery,insertQuery ,getAllQueryWithCondition,execQuery

def addProduct(mysql,cursor,data,files, user,page,action,method):
    try:
        result=getOneQuery(cursor,'SELECT name from products WHERE name=%s',(data['name']))
        if result:
            return render_template('/app/product/add_product.html',message=getMessage('PRODUCT_ALREADY_EXISTS') , success=False,user=user,data='',page=page,action=action,method=method)
        if 'thumbnail_image' not in files:
            flash(getMessage('PRODUCT_THUMB_IMAGE_NOT_FOUND'))
        if 'full_image' not in files:
            flash(getMessage('PRODUCT_FULL_IMAGE_NOT_FOUND'))
        thumbnail_image = files['thumbnail_image']
        full_image = files['full_image']
        if thumbnail_image.filename == '':
            flash(getMessage('PRODUCT_THUMB_IMAGE_NOT_FOUND'))
        if full_image.filename == '':
            flash(getMessage('PRODUCT_FULL_IMAGE_NOT_FOUND'))
        if thumbnail_image and allowed_file(thumbnail_image.filename) and full_image and allowed_file(full_image.filename):
            ext_thumb=get_extension(thumbnail_image.filename)
            ext_full=get_extension(full_image.filename)
            filename_thumb=get_time_stamp()
            filename_full=get_time_stamp()
            current_dir = os.getcwd()
            thumbnail_image.save(os.path.join(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/thumb' ,str(filename_thumb)+'_thumb.'+ext_thumb))
            full_image.save(os.path.join(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/full' ,str(filename_full)+'_full.'+ext_full))
            name=data['name']
            short_description=data['short_description']
            full_description=data['full_description']
            qty=data['qty']
            price=data['price']
            category_id=data['category_id']
            qry='INSERT into  products  (name,link,category_id,thumbnail_image,full_image,short_description,full_description,qty,price) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            values=(name,name.replace(" ", "-").lower(),category_id,str(filename_thumb)+'_thumb.'+ext_thumb,str(filename_full)+'_full.'+ext_full,short_description,full_description,qty,price)
            result=insertQuery(mysql,cursor,qry,values)
            flash(getMessage('PRODUCT_ADDED_SUCCESSFULLY') )
            return redirect('/app/products')

    except Exception as e:
         return render_template('/app/product/add_product.html',message=e.args[0], success=False,user=user,data='',page=page,action=action,method=method)

def updateProduct(mysql,cursor,data,files,product_id):
    try:
        if "name" in data:
            result=getOneQuery(cursor,'SELECT name from products WHERE name=%s AND id != %s',(data['name'],product_id))
            if  result:
                return render_template('/app/product/add_product.html',message=getMessage('PRODUCT_ALREADY_EXISTS') , success=False )
        thumbnail_image = files['thumbnail_image']
        full_image = files['full_image']
        if thumbnail_image and allowed_file(thumbnail_image.filename):
            resu=getOneQuery(cursor,'SELECT thumbnail_image from products WHERE id=%s',(product_id))
            ext_thumb=get_extension(thumbnail_image.filename)
            filename_thumb=get_time_stamp()
            current_dir = os.getcwd()
            thumbnail_image.save(os.path.join(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/thumb' ,str(filename_thumb)+'_thumb.'+ext_thumb))
            os.remove(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/thumb' +'/'+resu['thumbnail_image'])
            data['thumbnail_image']=str(filename_thumb)+'_thumb.'+ext_thumb
        if full_image and allowed_file(full_image.filename):
            resu=getOneQuery(cursor,'SELECT full_image from products WHERE id=%s',(product_id))
            ext_full=get_extension(full_image.filename)
            filename_full=get_time_stamp()
            current_dir = os.getcwd()
            full_image.save(os.path.join(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/full' ,str(filename_full)+'_full.'+ext_full))
            os.remove(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/full' +'/'+resu['full_image'])
            data['full_image']=str(filename_full)+'_full.'+ext_full
        fields=''
        for k, v in data.items():
            fields += k + '="'+str(v)+'",'
        result=execQuery(mysql,cursor,'UPDATE  products  SET '+fields.rstrip(',')+' WHERE id=%s',(product_id))
        flash(getMessage('PRODUCT_UPDATED_SUCCESSFULLY') )
        return redirect('/app/products')
    except Exception as e:
         print(e)
         return handle_bad_request(e)

def getProduct(cursor,productid):
    try:
        result=getOneQuery(cursor,'SELECT id,category_id,name,thumbnail_image,full_image,price,qty,short_description,full_description from products WHERE id=%s',(productid))
        if not result:
            raise Exception(getMessage('PRODUCT_NOT_FOUND'))
        return result
    except Exception as e:
        return handle_bad_request(e)

def activeDeativeProduct(mysql,cursor,product_id,is_active):
    try:
        result=getOneQuery(cursor,'SELECT name from products WHERE id = %s',(product_id))
        if  result:   
            result=execQuery(mysql,cursor,'UPDATE  products  SET is_active=%s WHERE id=%s',(is_active,product_id))
            flash(getMessage('PRODUCT_UPDATED_SUCCESSFULLY'))
            return {"updated":True }
        flash(getMessage('PRODUCT_NOT_FOUND') )
        return {"updated":False }
    except Exception as e:
        return handle_bad_request(e)
    

def deleteProduct(mysql,cursor,data):
    try:
        exist=getOneQuery(cursor,'SELECT name,thumbnail_image,full_image from products WHERE id=%s',(data['product_id']))
        if exist:
             execQuery(mysql,cursor,'DELETE from products WHERE id=%s',(data['product_id']))
             current_dir = os.getcwd()
             os.remove(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/thumb' +'/'+ exist['thumbnail_image'])
             os.remove(current_dir + os.getenv('UPLOAD_FOLDER_PRODUCT')+'/full' +'/'+exist['full_image'])
             flash(getMessage('PRODUCT_DELETED_SUCCESSFULLY') )
             return redirect('/app/products')
        raise Exception(getMessage('PRODUCT_NOT_FOUND'))
    except Exception as e:
        return handle_bad_request(e)    
    

def getProductsWithPagination(limit,page,cursor):
    try:
        if limit == None:
           limit = 10
        if page == None:
           page = 1
        offset=int(limit)*int(page)-int(limit)
        total=getAllQueryWithCondition(cursor,'SELECT COUNT(*) from products',())
        data=getAllQueryWithCondition(cursor,'SELECT * from products  LIMIT %s OFFSET %s ',(int(limit),int(offset)))
        result = { "data":data,"page":page,"limit":limit,"total":total[0]['COUNT(*)'],"totalPages":offset}
        return result
    except Exception as e:
        return handle_bad_request(e)