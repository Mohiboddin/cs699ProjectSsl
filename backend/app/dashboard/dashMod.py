from app import mail
from app.db import connect_db, db_close
from datetime import datetime
from flask_mail import Mail, Message
import bcrypt
import ssl
import socket



def certificateInfo(userId):
    try:
        con = connect_db()
        cur = con.cursor()
        sql = """
            SELECT url, created_at, updated_at, expire_mail_day, expire_date, status, problem_occurred, id
            FROM certificate_info
            WHERE created_by = %s
        """
        data={}
        cur.execute(sql, (userId,))
        data["url"] = cur.fetchall()
        sql = """
            SELECT url, message, id FROM notification WHERE email = (select email from appuser where id=%s)
        """
        cur.execute(sql, (userId,))
        data["messages"] = cur.fetchall()



        db_close(cur, con)
        return data if data else None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def create_certificate_info(url, expire_mail_day, created_by, expire_date, status, problem_occurred):
    con = connect_db()
    cur = con.cursor()
    sql = "INSERT INTO certificate_info (url, expire_mail_day, created_by, expire_date, status, problem_occurred) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"
    cur.execute(sql, (url, expire_mail_day, created_by, expire_date, status, problem_occurred))
    certificate_id = cur.fetchone()[0]
    db_close(cur, con)
    return certificate_id

def update_certificate_info(id, expire_mail_day, expire_date, status, problem_occurred):
    con = connect_db()
    cur = con.cursor()
    sql = "UPDATE certificate_info SET updated_at=NOW(), expire_mail_day = %s, expire_date = %s, status = %s, problem_occurred = %s WHERE id = %s"
    cur.execute(sql, (expire_mail_day, expire_date, status, problem_occurred, id))
    success = cur.rowcount > 0
    db_close(cur, con)
    return success

def update_certificate_info_days(id, expire_mail_day):
    con = connect_db()
    cur = con.cursor()
    sql = "UPDATE certificate_info SET expire_mail_day = %s, updated_at=NOW() WHERE id = %s"
    print( f"UPDATE certificate_info SET expire_mail_day = {expire_mail_day}, updated_at=NOW() WHERE id = {id}")
    cur.execute(sql, ( expire_mail_day, id))
    success = cur.rowcount > 0
    print(f"Inside the update_certificate_info_days {success}")
    db_close(cur, con)
    return success

def delete_certificate_info(id, created_by):
    con = connect_db()
    cur = con.cursor()
    sql = "DELETE FROM certificate_info WHERE id = %s and created_by=%s"
    cur.execute(sql, (id,created_by))
    success = cur.rowcount > 0
    db_close(cur, con)
    return success


def urlAlreadyExist(url, email):
    con = connect_db()
    cur = con.cursor()
    sql = "select url from certificate_info where url=%s and created_by=%s"
    cur.execute(sql, (url, email))
    success = cur.rowcount > 0
    db_close(cur, con)
    return success


def get_ssl_certificate_expiration(url):
    try:
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=url)
        conn.connect((url, 443))
        cert = conn.getpeercert()
        not_after = cert['notAfter']
        print(not_after)
        return not_after        
    except (ssl.SSLError, socket.error, KeyError):
        print("invalid url")
        return None
    
def delete_notification(id):
    con = connect_db()
    cur = con.cursor()
    sql = "DELETE FROM notification WHERE id = %s"
    cur.execute(sql, (id,))
    success = cur.rowcount > 0
    db_close(cur, con)
    return success
