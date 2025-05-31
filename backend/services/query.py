def getAllQueryWithCondition(cursor,query,values):
    try:
        cursor.execute(query,values)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)

def getAllQuery(cursor,query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)


def getOneQuery(cursor,query,values):
    try:
        cursor.execute(query,values)
        result=cursor.fetchone()
        return result
    except Exception as e:
        print(e)


def insertQuery(mysql,cursor,query,values):
    try:
        cursor.execute(query,values)
        result= mysql.connect().commit()
        return result
    except Exception as e:
        print(e)

def execQuery(mysql,cursor,query,values=None):
    try:
        cursor.execute(query,values)
        result= mysql.connect().commit()
        return result
    except Exception as e:
        print(e)
