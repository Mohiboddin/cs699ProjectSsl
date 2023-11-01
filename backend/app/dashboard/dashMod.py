from app import mail
from app.db import connect_db, db_close
from datetime import datetime
from flask_mail import Mail, Message
import bcrypt



def certificateInfo(userId):
    try:
        con = connect_db()
        cur = con.cursor()
        sql = """
            SELECT url, created_at, updated_at, expire_mail_day, expire_date, status, problem_occurred
            FROM certificate_info
            WHERE created_by = %s
        """
        cur.execute(sql, (userId,))
        data = cur.fetchall()
        db_close(cur, con)
        return data if data else None
    except Exception as e:
        print("An error occurred:", str(e))
        return None
