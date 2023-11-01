from app import mail
from app.db import connect_db, db_close
from datetime import datetime
from flask_mail import Mail, Message
import bcrypt



# whether the user exist in the table   
def verifyUser(email, password): #done
    print('In model to find user', email, 'and', password)
    try:
        con = connect_db()
        cur = con.cursor()
        hashed_password = password_hashing(password)
        sql = "SELECT id, username FROM appuser WHERE email = %s AND password = %s"
        cur.execute(sql, (email, hashed_password))
        user = cur.fetchone()
        db_close(cur, con)
        print("Sign-in Ends", user)
        return user if user else None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

#whether email exist in the appuser table
def verify_email(email): #done
    print('in modal to find user',email)
    con=connect_db()
    cur = con.cursor()
    sql= "SELECT email FROM appuser WHERE email = %s"
    cur.execute(sql,(email,))
    user=cur.fetchone()
    db_close(cur,con)
    print("verify_email Ends")
    return user[0] if user else None  

#this method is no use I think. inpite verify_otp() method is use full.
#whether email exist in the otptable
def verify_email_otp(email,otp):
    print('in modal to find user',email, 'for otp=', otp)
    con=connect_db()    
    cur = con.cursor()
    sql= "SELECT email FROM otp WHERE email = %s AND otp=%s"
    cur.execute(sql,(email,otp))
    email=cur.fetchone()
    db_close(cur,con)
    print("verify_email_otp Ends")
    return True if email else False 

#update the password in the appuser table
def update_password(email,password):
    print('in modal to update user',email, 'for password=', password)
    hashed_password=password_hashing(password)
    con=connect_db() 
    cur = con.cursor()
# email = email.replace('"', "'")
    sql= "UPDATE appuser  SET password=%s, updatedAt=now() WHERE email = %s RETURNING email;"
#   print(f"UPDATE appuser SET password={hashed_password}' WHERE email = '{email}'")
    cur.execute(sql,(hashed_password,email))
    update=cur.fetchone()
    db_close(cur,con)
    print("update_password Ends")
    return True if update else False 

#whther the otp_exist in the otptable
def otp_exist(email):  #done
    print('in modal to check OTP exist for ',email)
    con=connect_db() 
    cur = con.cursor()
    sql= "SELECT otp from otptable WHERE email = %s and expire> %s"
    cur.execute(sql,(email,datetime.now()))
    otp_exist=cur.fetchone()
    db_close(cur,con)
    print("update_password Ends")
    return otp_exist[0] if otp_exist else None

#insert the OTP
def otp(email,otp): #done
    print('in modal to store otp  ',otp)
    con=connect_db() 
    cur = con.cursor()
    sql= "INSERT INTO public.otptable(email, otp) VALUES (%s, %s)"
    otp_stored=cur.execute(sql,(email,otp))
    db_close(cur,con)
    print("otp stored")
    return otp_stored[0] if otp_stored else None 

def verify_otp(email,otp): #done
    print('in modal to verify otp  ',otp)
    con=connect_db() 
    cur = con.cursor()
    sql= "SELECT otp FROM otptable WHERE email=%s AND otp=%s AND expire> %s"
    cur.execute(sql,(email,otp,datetime.now() ))
    verify_otp=cur.fetchone()
    db_close(cur,con)
    print("otp stored", verify_otp)
    return  verify_otp

#whether OTP expired?
def verify_otp_expired(email):
    print('in modal to verify otp  ',otp)
    con=connect_db() 
    cur = con.cursor()
    sql= "SELECT otp FROM otp WHERE email=%s AND expire> %s"
    cur.execute(sql,(email,datetime.now() ))
    verify_otp=cur.fetchone()
    db_close(cur,con)
    print("otp stored", verify_otp)
    return  verify_otp

def send_mail(email, otp): #done
    try:
        print('sending email')
        body_text= f'You have now requested for new password, your OTP is {otp}'
        msg=Message('Update Password', sender='utorrentdata1@gmail.com', recipients=[email])
        msg.body= body_text
        mail.send(msg)
        return True
    except: return False



def password_hashing(token): #done
    SECRET_KEY='$2b$12$ag3g.9K9b.8S8n6a6SMGBO'
    hashed_token = (bcrypt.hashpw(token.encode('utf-8'), SECRET_KEY.encode('utf-8'))).decode('utf-8')
    print(f'Token : {token} & Hashed Token : {hashed_token}')
    if hashed_token:
        return hashed_token
    else:
        return None


# def find_by_username(cls,username,password):
#     print('in modal to find user',username, 'and',password)
#     cursor = mysql.connection.cursor()
#     sql = "SELECT username FROM user WHERE username = %s AND password =%s"
#     cursor.execute(sql,(username,password))
#     data = cursor.fetchone()
#     cursor.close()    
#     mysql.connection.commit()
#     print("Signin Ends")
#     return True if data else False       pip