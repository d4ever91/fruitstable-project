from helper import getMessage,sendResponse,handle_bad_request
from services.query import getAllQueryWithCondition

def getProductsByCategory(category_id,cursor):
    try:
        data=getAllQueryWithCondition(cursor,'SELECT p.name,p.link, p.thumbnail_image,p.short_description,p.price,p.qty, c.name as category_name  from products p LEFT JOIN categories c ON  p.category_id = c.id WHERE  p.category_id =? AND p.is_active =? AND c.is_active =?',(category_id,True,True))
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in data]
        return sendResponse("",data)
    except Exception as e:
        print(e)
        return handle_bad_request(e)
    

def getProductsAll(cursor,filter):
    try:
        qry ='SELECT p.name,p.link, p.thumbnail_image,p.short_description,p.price,p.qty, c.name as category_name  from products p LEFT JOIN categories c ON  p.category_id = c.id WHERE  p.is_active =? AND c.is_active =?'
        values =(True,True)
        if "cat_id" in filter and "price_value" in filter:
            qry += ' AND p.category_id = ? AND p.price <= ? '
            values=(True,True,filter['cat_id'],filter['price_value'])
        elif "cat_id" in filter:
            qry += ' AND p.category_id = ?'
            values=(True,True,filter['cat_id'])
        elif "price_value" in filter:
            qry += ' AND p.price <= ?'
            values=(True,True,filter['price_value'])

    
        if "price" in filter or "sort" in filter:
           opt =' ORDER BY'
        if "price" in filter and "sort" in filter:
            if filter['price'] == 0 and filter['sort'] == 0: 
                opt += ' p.price,p.name DESC '
            if filter['price'] == 1 and filter['sort'] == 1: 
                opt += ' p.price,p.name ASC '
            if filter['price'] == 1 and filter['sort'] == 0: 
                opt += ' p.price ASC , p.name DESC '
            if filter['price'] == 0 and filter['sort'] == 1: 
                opt += ' p.price DESC , p.name ASC '
        elif "price" in filter:
            opt += ' p.price '
            if filter['price'] == 0:
                opt +=' DESC'
            if filter['price'] == 1:
                opt +=' ASC'
        elif "sort" in filter:
            opt += ' p.name '
            if filter['sort'] == 0:
                opt +=' DESC'
            if filter['sort'] == 1:
                opt +=' ASC'
        qry += opt
        data=getAllQueryWithCondition(cursor,qry,values)
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in data]
        return sendResponse("",data)
    except Exception as e:
        return handle_bad_request(e)
    


    

    
