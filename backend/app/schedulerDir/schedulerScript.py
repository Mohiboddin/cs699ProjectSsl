from app import mail
from app import appcon
from app.db import connect_db, db_close
from datetime import datetime
from flask_mail import Mail, Message
import bcrypt
import ssl
import socket
import smtplib
import time


# certificate_info
# id |        url         |         created_at         |         updated_at         | expire_mail_day |              created_by              | expire_date | status | problem_occurred 

# appuser   id                  | username  |        email         |                           password                           |         createdat          |         updatedat          | verify 


def schedulerScriptFunc2():
    print("Hello, World from inner function!")
    current_datetime = datetime.now()
    print("Hello from inner, Current Date and Time:", current_datetime)
    allWebsiteData=fetchAllWebsite()
    print(allWebsiteData)
    notifications=[]
    for row in allWebsiteData:

        ssl_date_str = get_ssl_certificate_expiration(row['url'])
        if ssl_date_str:
            ssl_date = datetime.strptime(ssl_date_str, "%b %d %H:%M:%S %Y GMT")

            # Create a datetime object for the PostgreSQL date
            postgres_date = row['expire_date']

            # Calculate the current date
            current_date = datetime.now()

            # Calculate the remaining days until the SSL date
            remaining_days = (ssl_date - current_date).days
            print(remaining_days)
            # Check if the remaining days are less than 14
            if remaining_days < 14:
                print("Remaining days are less than 14.")
                notifications.append({'email':row['email'], 'url':row['url'], 'dayLeft':remaining_days , 'notificationCode':1, 'notificationMsg':"send msg only 14 days left." })
            else:
                print("Remaining days are not less than 14.")
        else:
            print ("URL problem")
            notifications.append({'email':row['email'], 'url':row['url'], 'notificationCode':2, 'notificationMsg':"can't able to access the certificate." })

    sendEmailFunc(notifications)

def sendEmailFunc(notifications):
    appcon.push()
    print(notifications)
    # with app.app_context():
    for row in notifications:
        #send expiry email.
        if row['notificationCode']==1:
            try:
                email=row['email']
                url=row['url']
                dayLeft=row['dayLeft']
                print(f'sending email to {email}' )
                body_text= f'you need to update the SSL certificate for url: {url} within {dayLeft} days.'
                print(body_text)
                msg=Message('SSL Alert', sender='mohibs2001@gmail.com', recipients=[email])
                msg.body= body_text
                mail.send(msg)
                #databse add msg
                addMsg(body_text, email, url)
            except smtplib.SMTPException as e:
                #databse add msg
                addMsg('cant sent Expiration email on given Email ID', email, url)
            except Exception as e:
                print("An error occurred:", str(e))
    
        #cant access certificate email
        if row['notificationCode']==2:
            try:
                email=row['email']
                url=row['url']
                print('sending email')
                body_text= f'Cant able to access the certificate for URL: {url}'
                print(f'sending email to {email}' )
                print(body_text)
                msg=Message('SSL Alert', sender='mohibs2001@gmail.com', recipients=[email])
                msg.body= body_text
                mail.send(msg)
                updateCertificateInfo(url, email)
                addMsg(f'Cant able to access the certificate for URL:{url}', email, url)
            except smtplib.SMTPException as e:
                updateCertificateInfo(url, email)
                addMsg('cant sent invalid certificate email on given Email ID', email, url)
            except Exception as e:
                print("An error occurred:", str(e))
            time.sleep(3)
    appcon.pop()

    

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
    except Exception as e:
        print("An error occurred:", str(e))
    

    
def fetchAllWebsite():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Define the SQL query to join the two tables and extract specific columns
        sql = """
        SELECT appuser.email, certificate_info.url, certificate_info.expire_mail_day, certificate_info.status, certificate_info.problem_occurred, certificate_info.expire_date
        FROM appuser, certificate_info
        WHERE appuser.id = certificate_info.created_by;
        """
        
        cursor.execute(sql)
        data = cursor.fetchall()
        db_close(cursor, conn)
        # Create a list of dictionaries to store the result
        result = []
        print(data)
        for row in data:
            if row[3]==True and row[4]==False:
                result.append({
                    'email': row[0],
                    'url': row[1],
                    'expire_email_day': row[2],
                    'status': row[3],
                    'problem_occurred': row[4],
                    'expire_date': row[5]
                })
        if result:
            return result
        else:
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None



def updateCertificateInfo(url, email):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """UPDATE certificate_info SET status=FALSE, problem_occurred =TRUE FROM appuser WHERE certificate_info.created_by = appuser.id AND appuser.email =%s AND certificate_info.url=%s;"""
        cursor.execute(sql, (email,url))
        db_close(cursor, conn)
        return
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def addMsg(msg, email, url):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        sql = """
        INSERT INTO notification (email, url, message) VALUES
            (%s, %s, %s);
        """
        cursor.execute(sql, (email,url,msg))
        db_close(cursor, conn)
        return
    except Exception as e:
        print("An error occurred:", str(e))
        return None
    
# schedulerScriptFunc2()
print("completed operation")
