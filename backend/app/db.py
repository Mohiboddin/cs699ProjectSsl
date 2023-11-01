import psycopg2


def connect_db():    
    con = psycopg2.connect(
        dbname='sslmonitor' ,
        user='postgres' ,
        host='localhost' ,
        password='postgres')
    return con

def db_close(cur, con):
    con.commit()
    cur.close()
    con.close()

# Script to make query to db 

#     # connect the db
#     cur = con.cursor()

#     cur.execute("CREATE TABLE test(id serial PRIMARY KEY, name varchar, email varchar)")

#     con.commit()

#     # closing the db connection
#     cur.close()
#     con.close()
