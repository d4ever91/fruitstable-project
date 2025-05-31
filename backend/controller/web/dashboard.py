from helper import handle_bad_request
from services.query import getAllQuery
    
    
def getDashboardCounts(cursor):
    try:
        totalCustomers=getAllQuery(cursor,'SELECT COUNT(*) from customers')
        totalCategories=getAllQuery(cursor,'SELECT COUNT(*) from categories')
        totalProducts=getAllQuery(cursor,'SELECT COUNT(*) from products')
        totalUsers=getAllQuery(cursor,'SELECT COUNT(*) from users WHERE role != 1')
        result = {"total_customers":totalCustomers[0]['COUNT(*)'],"total_categories":totalCategories[0]['COUNT(*)'],
                  "total_products":totalProducts[0]['COUNT(*)'],"total_users":totalUsers[0]['COUNT(*)']} 
        return result
    except Exception as e:
        return handle_bad_request(e)
    
