import sqlite3

class DB:

    dbPath = 'storage/app.db'

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(statement, values):
        #Connect to db
        conn = sqlite3.connect(DB.dbPath)
        db = conn.cursor()

        #Insert data
        db.execute(statement, values)
        conn.commit()

        #Close connection
        conn.close()

    def selectOne(statement, params):
        #Connect to db
        conn = sqlite3.connect(DB.dbPath)
        db = conn.cursor()
        db.row_factory = DB.dict_factory

        #Insert data
        db.execute(statement, params)
        row = db.fetchone()
        conn.close()

        #Return data
        return row

    def selectAll(statement, params):
        #Connect to db
        conn = sqlite3.connect(DB.dbPath)
        db = conn.cursor()
        db.row_factory = DB.dict_factory

        #Insert data
        db.execute(statement, params)
        row = db.fetchall()
        conn.close()

        #Return data
        return row
       
        
        
