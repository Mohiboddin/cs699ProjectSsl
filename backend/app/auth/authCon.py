from app import app
from flask import render_template, redirect, request, session, jsonify, make_response, url_for
from app.auth import authMod
import random
from functools import wraps


def loginRequired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":
        json_data = request.get_json(force = True)
        print("printing json data", json_data)
        username = json_data['username']
        email = json_data['email']
        password = json_data['password']
        if email and password and username:
            #locate the user
            userninfo= authMod.verify_email(email)
            # set the session
            if(userninfo is None):
                #Send Email
                already_otp= authMod.signup_otp_exist(email)
                if already_otp:
                    return {'messsage':'OTP already exist', 'otp': already_otp, 'code':3}, 200
                value = random.randint(1001,9999)
                #sending otp with email.
                email_sent=authMod.new_user_send_mail(email,value)
                if email_sent:
                    print("Email Sended", value)
                    authMod.signup_otp(email,value)
                    return {'messsage':'Enter the OTP', 'otp': value, 'code':1}, 200
                else:
                    return {'messsage':'Something went wrong in server', 'code': 3}, 200  
            else:
                return {'messsage':'Email already Exist, try differnt email', 'code': 2}, 200 # user not found
            

    print("returning signup page")
    return render_template('auth/signup.html')



@app.route("/signupotpverify", methods=["POST"])
def signupotpverify():
    if request.method == "POST":
        json_data = request.get_json(force = True)
        email = json_data['email']
        otp = json_data['otp']
        username = json_data['username']
        password = json_data['password']
        validate= authMod.signup_verify_otp(email, otp)
        if(validate):
            #store new user
            authMod.addNewUser(email, username, password)
            return {'messsage':'Account created', 'code': 1}, 200
        else:
            return {'messsage':'wrong OTP Or the 2 min time limit Exceed', 'code': 2}, 200


@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == "POST":
        json_data = request.get_json(force = True)
        print("printing json data", json_data)
        email = json_data['email']
        password = json_data['password']
        if email and password:
            #locate the user
            userninfo= authMod.verifyUser(email, password)
            # set the session
            if(userninfo is not None):
                session["email"]=email
                session["username"] = userninfo[1]
                session["userId"] = userninfo[0]
                session["logged_in"]=True
                print(userninfo)
                return {'msg': 'Successfully Loged in', 'code': 1},200 # OK
            else:
                return {'messsage':'Invalid Username Or password', 'code': 2}, 200 # user not found
            

    print("returning Login page")
    return render_template('auth/login.html')



@app.route("/logout")
def logout():
    session.pop('logged_in',None)
    session.pop('username',None)
    session.pop('email',None)
    return redirect(url_for('login'))


@app.route("/forgotpassword", methods=["POST", "GET"])
def forgot_password():

    if request.method == "POST":
        json_data = request.get_json(force = True)
        email = json_data['email']
        #locate the user
        username= authMod.verify_email(email)
        # set the session
        if username:
            #Send Email
            already_otp= authMod.otp_exist(email)
            if already_otp:
                return {'messsage':'OTP already exist', 'otp': already_otp, 'code':3}, 200
            value = random.randint(1001,9999)
            #sending otp with email.
            email_sent=authMod.new_user_send_mail(email,value)
            if email_sent:
                print("Email Sended", value)
                authMod.otp(email,value)
                return {'messsage':'Enter the OTP', 'otp': value, 'code':1}, 200
            else:
                return {'messsage':'Something went wrong in server', 'code': 3}, 200   
            
        return {'messsage':'user dosent exist', 'code': 2}, 200
   
    print("returning forgot Password page")
    return render_template('auth/forgotPassword.html')



@app.route("/otpverify", methods=["POST"])
def verify_otp():
    if request.method == "POST":
        json_data = request.get_json(force = True)
        email = json_data['email']
        otp = json_data['otp']

        validate= authMod.verify_otp(email, otp)
        if(validate):
            #store new password
            session["email"] = email
            return {'messsage':'proceed for change password', 'code': 1}, 200
        else:
            return {'messsage':'wrong OTP Or the 2 min time limit Exceed', 'code': 2}, 200


@app.route("/recovery", methods=["POST","GET"])
def recovery():
    if request.method == "POST":
        json_data = request.get_json(force = True)

        if'email' not in session:
            return {'messsage':'Invalid request-no session', 'code': 2}, 200
        
        email = session["email"]
        confirm_password = json_data['confirm_password']
        password = json_data['password']

        # validate= authMod.verify_otp_expired(email)
        session.pop('email',None)
        update=authMod.update_password(email,password)

        if update:
            return {'messsage':'Password Updated', 'code': 1}, 200
        else:
            return {'messsage':'Password Updated failed', 'code': 2}, 200

    print("returning recovery page")
    return render_template('auth/recPassword.html')
