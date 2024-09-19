import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time
import random
import string
import statistics
import settings as st

res = [0 for i in range(0, 10)]
sql_query_string = 'SELECT * FROM students WHERE Name LIKE \'%kh%\''
for i in range(0, 10):
    connection = psycopg2.connect(**st.db_params)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    start = time.time()
    cursor.execute(sql_query_string) 
    connection.commit()
    end = time.time()
    res[i] = end - start
    cursor.close()
    connection.close()
print(statistics.mean(res))