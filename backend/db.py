
def getConnection(app,host,user,password,database):
    try:
       app.secret_key = '1a2b3c4d5e6d7g8h9i10'
       app.config['MYSQL_HOST'] = host
       app.config['MYSQL_USER'] = user
       app.config['MYSQL_PASSWORD'] = password#Replace ******* with  your database password.
       app.config['MYSQL_DB'] = database
       print("Database connected successfully")
       return app
    except Exception as e:
        print(e)


# def dbQuery(query,connect):
#     try:
#         with connect:
#              with connect.cursor() as cursor:
#                  cursor.execute(query)
#                  result = cursor.fetchone()
#                  return result
#     except Exception as e:
#         print(e)


