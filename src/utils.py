import os
import json
import time
import sqlite3
from src.db import DB
from datetime import datetime, timedelta

class Utils:

    def cache(key, value = False, expiry = False):
        try:
            #Open data or write
            if value == False:
                #Get db cache
                cache = DB.selectOne("SELECT * FROM cache WHERE key = ?;", (key,))

                #Check if expired
                if(cache['expiry']):
                    datetime.strptime(cache['expiry'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now()
                else:
                    return None

                return cache['value']
            else:
                DB.execute("INSERT OR REPLACE INTO cache(key, value, expiry) VALUES(?, ?, ?);", (
                        key, value, str(datetime.now() + timedelta(minutes=expiry)),
                    )
                )
        except Exception as e:
            print(e)
            return None