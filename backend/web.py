from flask import request , render_template,session,redirect
from helper import handle_bad_request
from controller.web.dashboard import getDashboardCounts
from controller.web.user import userLogin,addUser,getUser,getUsersWithPagination,updateUser,deleteUser,getCurrentUser,activeDeativeUser
from controller.web.customer import addCustomer, getCustomer,getCustomersWithPagination,updateCustomer,deleteCustomer,activeDeativeCustomer
from controller.web.product import getProductsWithPagination,addProduct,getProduct,updateProduct,deleteProduct,activeDeativeProduct

from controller.web.category import getCategorysWithPagination,addCategory,deleteCategory,updateCategory,activeDeativeCategory,getCategory,getCategories

from model.user import userSchema,UserSchemaAddUser,UserSchemaUpdateUser,UserSchemaDeleteUser
from model.customer import CustomerSchemaAddCustomer,CustomerSchemaUpdateCustomer,CustomerSchemaDeleteCustomer
from model.category import CategorySchemaAddcategory,CategorySchemaDeletecategory,CategorySchemaUpdatecategory
from model.product import ProductSchemaAddproduct,ProductSchemaUpdateproduct,ProductSchemaDeleteproduct



from middleware.middleware import require_session_authentication,require_session_non_authentication,check_super_admin_role

def DashboardWebRoutes(app,cursor):
        @app.route('/app/dashboard', methods=['GET'])
        @require_session_authentication
        def app_dashboard():
            try:    
                user=getCurrentUser(cursor)
                data=getDashboardCounts(cursor)
                return render_template('/app/dashboard/dashboard.html',page='dashboard',user=user,data=data)
            except Exception as e:
                return handle_bad_request(e)

def UserWebRoutes(app,mysql,cursor):
        @app.route('/', methods=['GET'])
        @require_session_non_authentication
        def home():
            try:
                return redirect('/auth/login');
            except Exception as e:
                return handle_bad_request(e)

        @app.route('/auth/login', methods=['POST','GET'])
        @require_session_non_authentication
        def auth_login():
            try:
                if request.method == "POST":
                    data =request.form
                    result = userSchema.load(data)
                    return userLogin(cursor,result)
                if request.method == "GET":
                    return render_template('/auth/login.html')
            except Exception as e:
                return handle_bad_request(e)
    


            
        @app.route('/app/users', methods=['GET'])
        @require_session_authentication
        def app_users():
            try:
                    if request.method == "GET":
                         limit = request.args.get('limit')
                         page = request.args.get('page')
                         result=getUsersWithPagination(limit,page,cursor)
                         user=getCurrentUser(cursor)
                         return render_template('/app/user/users.html',page='users',result=result,user=user , modal_title="Update User",modal_body="Are you sure ?")
            except Exception as e:
                return handle_bad_request(e)
            
            
        @app.route('/app/user/add', methods=['GET','POST'])
        @require_session_authentication
        def app_user_add():
            try:
                    user=getCurrentUser(cursor)
                    if request.method == "GET":
                        return render_template('/app/user/add_user.html',page='add user',action='/app/user/add',method="POST", user=user,data='')
                    if request.method == "POST":
                        data =request.form
                        result = UserSchemaAddUser.load(data)
                        return addUser(mysql,cursor,result, user=user,page='add user',action='/app/user/add',method="POST")
            except Exception as e:
                return handle_bad_request(e)
            

            
        @app.route('/app/logout', methods=['GET'])
        @require_session_authentication
        def app_logout():
            try:
                session['public_id']='';
                return redirect('/auth/login')
            except Exception as e:
                return handle_bad_request(e)

            

        @app.route('/app/user/edit/<user_id>', methods=['GET'])
        @require_session_authentication
        def user_get(user_id):
            try:
                if request.method == "GET":
                    data=getUser(cursor,user_id)
                    user=getCurrentUser(cursor)
                    return render_template('/app/user/add_user.html',page='update user',action='/app/user/update/'+user_id,method="POST", user=user,data=data)
            except Exception as e:
                return handle_bad_request(e)
            

        @app.route('/app/user/update/<user_id>', methods=['POST'])
        @require_session_authentication
        def user_update(user_id):
            try:
                if request.method == "POST":
                    data =request.form
                    result = UserSchemaUpdateUser.load(data)
                    return updateUser(mysql,cursor,result,user_id)
            except Exception as e:
                return handle_bad_request(e)
        
        @app.route('/app/user/active/<user_id>', methods=['PUT'])
        @require_session_authentication
        def user_active_deactive(user_id):
            try:
                if request.method == "PUT":
                    data =request.get_json(force=True)
                    UserSchemaUpdateUser.load(data)
                    return activeDeativeUser(mysql,cursor,user_id,data['is_active'])
            except Exception as e:
                return handle_bad_request(e)
            

        @app.route('/app/user/delete/<user_id>', methods=['DELETE'])
        @require_session_authentication 
        def user_delete(user_id):
            try:
                if request.method == "DELETE":
                    result = UserSchemaDeleteUser.load({"user_id":user_id})
                    return deleteUser(mysql,cursor,result)
            except Exception as e:
                return handle_bad_request(e)
            
        # categories routes
def CategoryWebRoutes(app,mysql,cursor):
        @app.route('/app/categories', methods=['GET'])
        @require_session_authentication
        def app_categories():
            try:
                    if request.method == "GET":
                         limit = request.args.get('limit')
                         page = request.args.get('page')
                         result=getCategorysWithPagination(limit,page,cursor)
                         user= getCurrentUser(cursor)
                         return render_template('/app/category/categories.html',page='categories',result=result,user=user , modal_title="Update Category",modal_body="Are you sure ?")
            except Exception as e:
                return handle_bad_request(e)

        @app.route('/app/category/add', methods=['GET','POST'])
        @require_session_authentication
        def app_category_add():
            try:
                    user=getCurrentUser(cursor)
                    if request.method == "GET":
                        return render_template('/app/category/add_category.html',page='add category',action='/app/category/add',method="POST", user=user,data='')
                    if request.method == "POST":
                        data =request.form
                        result = CategorySchemaAddcategory.load(data)
                        return addCategory(mysql,cursor,result,request.files, user=user,page='add category',action='/app/category/add',method="POST")
            except Exception as e:
                return handle_bad_request(e)
            
        
        @app.route('/app/category/edit/<category_id>', methods=['GET'])
        @require_session_authentication
        def category_get(category_id):
            try:
                if request.method == "GET":
                    data=getCategory(cursor,category_id)
                    user=getCurrentUser(cursor)
                    return render_template('/app/category/add_category.html',page='update category',action='/app/category/update/'+category_id,method="POST", user=user,data=data)
            except Exception as e:
                return handle_bad_request(e)
            

        @app.route('/app/category/update/<category_id>', methods=['POST'])
        @require_session_authentication
        def category_update(category_id):
            try:
                if request.method == "POST":
                    data =request.form
                    result = CategorySchemaUpdatecategory.load(data)
                    return updateCategory(mysql,cursor,result,request.files,category_id)
            except Exception as e:
                return handle_bad_request(e)
        
        @app.route('/app/category/active/<category_id>', methods=['PUT'])
        @require_session_authentication
        def category_active_deactive(category_id):
            try:
                if request.method == "PUT":
                    data =request.get_json(force=True)
                    CategorySchemaUpdatecategory.load(data)
                    return activeDeativeCategory(mysql,cursor,category_id,data['is_active'])
            except Exception as e:
                return handle_bad_request(e)
            

        @app.route('/app/category/delete/<category_id>', methods=['DELETE'])
        @require_session_authentication 
        def category_delete(category_id):
            try:
                if request.method == "DELETE":
                    result = CategorySchemaDeletecategory.load({"category_id":category_id})
                    return deleteCategory(mysql,cursor,result)
            except Exception as e:
                return handle_bad_request(e)
            

        # product routes
def ProductWebRoutes(app,mysql,cursor):
        @app.route('/app/products', methods=['GET'])
        @require_session_authentication
        def app_products():
            try:
                    if request.method == "GET":
                         limit = request.args.get('limit')
                         page = request.args.get('page')
                         result=getProductsWithPagination(limit,page,cursor)
                         user= getCurrentUser(cursor)
                         return render_template('/app/product/products.html',page='products',result=result,user=user , modal_title="Update Product",modal_body="Are you sure ?")
            except Exception as e:
                return handle_bad_request(e)

        @app.route('/app/product/add', methods=['GET','POST'])
        @require_session_authentication
        def app_product_add():
            try:
                    user=getCurrentUser(cursor)
                    if request.method == "GET":
                        categories=getCategories(cursor)
                        return render_template('/app/product/add_product.html',page='add product',action='/app/product/add',method="POST", user=user,data='',categories=categories)
                    if request.method == "POST":
                        data =request.form
                        result = ProductSchemaAddproduct.load(data)
                        return addProduct(mysql,cursor,result,request.files, user=user,page='add product',action='/app/product/add',method="POST")
            except Exception as e:
                return handle_bad_request(e)
            
        @app.route('/app/product/edit/<product_id>', methods=['GET'])
        @require_session_authentication
        def product_get(product_id):
            try:
                if request.method == "GET":
                    data=getProduct(cursor,product_id)
                    categories=getCategories(cursor)
                    user=getCurrentUser(cursor)
                    return render_template('/app/product/add_product.html',page='update product',action='/app/product/update/'+product_id,method="POST", user=user,data=data,categories=categories)
            except Exception as e:
                return handle_bad_request(e)
        
        @app.route('/app/product/update/<product_id>', methods=['POST'])
        @require_session_authentication
        def product_update(product_id):
            try:
                if request.method == "POST":
                    data =request.form
                    result = ProductSchemaUpdateproduct.load(data)
                    return updateProduct(mysql,cursor,result,request.files,product_id)
            except Exception as e:
                return handle_bad_request(e)
            
        @app.route('/app/product/active/<product_id>', methods=['PUT'])
        @require_session_authentication
        @check_super_admin_role(cursor,'/app/products')
        def product_active_deactive(product_id):
            try:
                if request.method == "PUT":
                    data =request.get_json(force=True)
                    ProductSchemaUpdateproduct.load(data)
                    return activeDeativeProduct(mysql,cursor,product_id,data['is_active'])
            except Exception as e:
                return handle_bad_request(e)
        
        @app.route('/app/product/delete/<product_id>', methods=['DELETE'])
        @require_session_authentication 
        def product_delete(product_id):
            try:
                if request.method == "DELETE":
                    result = ProductSchemaDeleteproduct.load({"product_id":product_id})
                    return deleteProduct(mysql,cursor,result)
            except Exception as e:
                return handle_bad_request(e)

        
def CustomerWebRoutes(app,mysql,cursor):
        @app.route('/app/customers', methods=['GET'])
        @require_session_authentication
        def app_customers():
            try:
                    limit = request.args.get('limit')
                    page = request.args.get('page')
                    result=getCustomersWithPagination(limit,page,cursor)
                    user=getCurrentUser(cursor)
                    return render_template('/app/customer/customers.html',page='customers',result=result,user=user , modal_title="Update Category",modal_body="Are you sure ?")
            except Exception as e:
                return handle_bad_request(e)
            
            
        @app.route('/app/customer/add', methods=['GET','POST'])
        @require_session_authentication
        def app_customer_add():
            try:
                    if request.method == "GET":
                        return render_template('/app/customer/add_customer.html',page='add customer')
                    if request.method == "POST":
                        data =request.form
                        result = CustomerSchemaAddCustomer.load(data)
                        return addCustomer(mysql,cursor,result)
            except Exception as e:
                return handle_bad_request(e)
        
        @app.route('/app/customer/edit/<customer_id>', methods=['GET'])
        @require_session_authentication
        def customer_get(customer_id):
            try:
                if request.method == "GET":
                    data=getCustomer(cursor,customer_id)
                    user=getCurrentUser(cursor)
                    return render_template('/app/customer/add_customer.html',page='update customer',action='/app/customer/update/'+customer_id,method="POST", user=user,data=data)
            except Exception as e:
                return handle_bad_request(e)
        
        @app.route('/app/customer/update/<customer_id>', methods=['GET','POST'])
        @require_session_authentication
        def app_customer_update(customer_id):
            try:
                    if request.method == "GET":
                        return render_template('/app/customer/add_customer.html',page='update customer')
                    if request.method == "POST":
                        data =request.form
                        result = CustomerSchemaUpdateCustomer.load(data)
                        return updateCustomer(mysql,cursor,result,customer_id)
            except Exception as e:
                return handle_bad_request(e)
            
        @app.route('/app/customer/active/<customer_id>', methods=['PUT'])
        @require_session_authentication
        def customer_active_deactive(customer_id):
            try:
                if request.method == "PUT":
                    data =request.get_json(force=True)
                    CustomerSchemaUpdateCustomer.load(data)
                    return activeDeativeCustomer(mysql,cursor,customer_id,data['is_active'])
            except Exception as e:
                return handle_bad_request(e)
        
        @app.route('/app/customer/delete/<customer_id>', methods=['DELETE'])
        @require_session_authentication 
        def customer_delete(customer_id):
            try:
                if request.method == "DELETE":
                    result = CustomerSchemaDeleteCustomer.load({"customer_id":customer_id})
                    return deleteCustomer(mysql,cursor,result)
            except Exception as e:
                return handle_bad_request(e)



