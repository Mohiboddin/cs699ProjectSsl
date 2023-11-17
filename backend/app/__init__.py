from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail, Message
import smtplib
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime

load_dotenv()

app=Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app)


#mail server configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True


mail=Mail(app)

#inorder to avoid the circular import these files are imported here
from app.auth import authCon
from app.dashboard import dashCon
from app.schedulerDir import schedulerScript
schedulerScript.schedulerScriptFunc2()
# scheduler = BackgroundScheduler()
# x=0
# def schedulerScriptFunc():
#     # Get the current date and time
#     current_datetime = datetime.datetime.now()
#     global x
#     print("Hello from main, Current Date and Time:", current_datetime, " ", x)
#     schedulerScript.schedulerScriptFunc2()
#     # Get the list of jobs
#     jobs = scheduler.get_jobs()
#     x=x+10
#     # Print the list of jobs
#     for job in jobs:
#         print(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}")

# if not scheduler.running:
#     scheduler.add_job(schedulerScriptFunc, IntervalTrigger(seconds=2))
#     scheduler.start()

#these are testing routes
@app.route("/")
def show_page():
   
    print("returning home show page")
    return "Hello"
    #return render_template('display/show_page.html')

@app.route("/sendemail",  methods=['GET'])
def send_mail(): #done
    try:
        email="mohibs2001@gmail.com"
        otp=1234
        print('sending email')
        body_text= f'You have now requested for new password, your OTP is {otp}'
        msg=Message('Update Password', sender='mohibs2001@gmail.com', recipients=[email])
        msg.body= body_text
        mail.send(msg)
        return "Message Sent"
    except smtplib.SMTPException as e:
        return f"Message not sent. Error: {str(e)}"
    
