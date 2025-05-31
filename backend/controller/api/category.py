from helper import getMessage,sendResponse,handle_bad_request
from services.query import getAllQueryWithCondition

def getCategories(cursor):
    try:
        data=getAllQueryWithCondition(cursor,'SELECT id,name,link,image  from categories WHERE is_active = %s',(True))
        if not data:
            raise Exception(getMessage('CATEGORY_NOT_FOUND'))
        return sendResponse("",data)
    except Exception as e:
        return handle_bad_request(e)
    


    

    
