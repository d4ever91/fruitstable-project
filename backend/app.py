from flask import Flask 
from flaskext.mysql import MySQL
from flask_cors import CORS
import os
import sqlite3
from web import UserWebRoutes,CustomerWebRoutes,CategoryWebRoutes,ProductWebRoutes,DashboardWebRoutes
from api import ApiCustomerRoutes,ApiCategoryRoutes,ApiProductRoutes
from migration import categoryMigration ,countryMigation, productMigration , reviewMigration,userMigation,customerMigration
app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config['UPLOAD_FOLDER'] =os.getenv('UPLOAD_FOLDER') 
CORS(app, resources={ r"/*":{ "origins":"*" }})
# cors = CORS(app, resources={r"/": {"origins": "http://127.0.0.1:5500"}})
app.secret_key = os.getenv('SESSION_SECRET_KEY')
mysql = sqlite3.connect('project.db', check_same_thread=False)
mysql.row_factory = sqlite3.Row
cursor = mysql.cursor()

# userMigation(mysql,cursor)
# countryMigation(mysql,cursor)
# customerMigration(mysql,cursor)
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







