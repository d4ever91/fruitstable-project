from flask import Flask 
from flaskext.mysql import MySQL
from flask_cors import CORS
import os
import pymysql.cursors
from web import UserWebRoutes,CustomerWebRoutes,CategoryWebRoutes,ProductWebRoutes,DashboardWebRoutes
from api import ApiCustomerRoutes,ApiCategoryRoutes,ApiProductRoutes
from migration import categoryMigration , productMigration , reviewMigration
app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config['UPLOAD_FOLDER'] =os.getenv('UPLOAD_FOLDER') 
CORS(app, resources={ r"/*":{ "origins":"*" }})
# cors = CORS(app, resources={r"/": {"origins": "http://127.0.0.1:5500"}})
app.secret_key = os.getenv('SESSION_SECRET_KEY')
mysql = MySQL(app,host=os.getenv('DB_HOST'),user=os.getenv('DB_USER'),password=os.getenv('DB_PASSWORD'),db=os.getenv('DB_NAME'), autocommit=True, cursorclass=pymysql.cursors.DictCursor)
mysql.init_app(app)
with app.app_context():
    cursor =mysql.get_db().cursor()
    # categoryMigration(mysql,cursor)
    # productMigration(mysql,cursor)
    # reviewMigration(mysql,cursor)
DashboardWebRoutes(app,cursor)
UserWebRoutes(app,mysql,cursor)
ProductWebRoutes(app,mysql,cursor)
CustomerWebRoutes(app,mysql,cursor)
CategoryWebRoutes(app,mysql,cursor)

ApiCustomerRoutes(app,mysql,cursor)
ApiCategoryRoutes(app,mysql,cursor)
ApiProductRoutes(app,mysql,cursor)







