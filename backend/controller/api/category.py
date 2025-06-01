from helper import getMessage,sendResponse,handle_bad_request
from services.query import getAllQueryWithCondition
import json

def getCategories(cursor):
    try:
        data=getAllQueryWithCondition(cursor,'SELECT id,name,link,image  from categories WHERE is_active = ?',(True,))
        columns = [column[0] for column in cursor.description]
        data = [dict(zip(columns, row)) for row in data]
        if not data:
            raise Exception(getMessage('CATEGORY_NOT_FOUND'))
        return sendResponse("",data)
    except Exception as e:
        print(e)
        return handle_bad_request(e)
    


    

    
