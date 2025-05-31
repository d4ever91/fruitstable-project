from flask import request ,render_template
from flask_cors import cross_origin
from helper import getMessage,sendResponseByStatus,handle_bad_request
from controller.api.customer import customerLogin,customerRegister

from controller.api.category import getCategories
from controller.api.product import getProductsByCategory,getProductsAll

from model.customer import CustomerSchema,CustomerSchemaAddCustomer
from middleware.middleware import require_authentication,check_super_admin_role,require_session_authentication,require_session_non_authentication

def ApiCustomerRoutes(app,mysql,cursor):
    @app.route('/api/customer/login', methods=['POST'])
    def customer_login():
        try:
                data = request.get_json(force=True)
                result = CustomerSchema.load(data)
                return customerLogin(cursor,result)
        except Exception as e:
            return handle_bad_request(e)
    

    @app.route('/api/customer/register', methods=['POST'])
    def customer_register():
        try:
                data = request.get_json(force=True)
                result = CustomerSchemaAddCustomer.load(data)
                return customerRegister(mysql,cursor,result)
        except Exception as e:
            return handle_bad_request(e)
        
    @app.route('/api/customer/detail', methods=['GET'])
    def customer_detail():
        try:
                return customerRegister(mysql,cursor)
        except Exception as e:
            return handle_bad_request(e)

def ApiCategoryRoutes(app,mysql,cursor):
    @app.route('/api/categories', methods=['GET'])
    def categories_get():
        try:
                return getCategories(cursor)
        except Exception as e:
            return handle_bad_request(e)
    

    @app.route('/api/category/register', methods=['POST'])
    def category_register():
        try:
                data = request.get_json(force=True)
                result = CustomerSchemaAddCustomer.load(data)
                return customerRegister(mysql,cursor,result)
        except Exception as e:
            return handle_bad_request(e)
        
    @app.route('/api/category/detail', methods=['GET'])
    def category_detail():
        try:
                return customerRegister(mysql,cursor)
        except Exception as e:
            return handle_bad_request(e)

def ApiProductRoutes(app,mysql,cursor):
    @app.route('/api/products/<category_id>', methods=['GET'])
    def products_category_get(category_id):
        try:
                return getProductsByCategory(category_id,cursor)
        except Exception as e:
            return handle_bad_request(e)
    
    @app.route('/api/products/all', methods=['POST'])
    def products_get():
        try:
                data = request.get_json(force=True)
                return getProductsAll(cursor,data)
        except Exception as e:
            return handle_bad_request(e)
        

        

        

   
        
    





