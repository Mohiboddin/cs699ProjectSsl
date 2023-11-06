from app import app
from flask import render_template, redirect, request, session, jsonify, make_response, url_for
from app.dashboard import dashMod
from app.auth.authCon import loginRequired
import random
from functools import wraps
from datetime import datetime

@app.route("/dashboard", methods=["GET"])
@loginRequired
def dashboard():
    userId = session["userId"]
    data = dashMod.certificateInfo(userId)
    print("returning dashboard page")
    if data is not None:
        return render_template('dashboard/dashboard3.html', data=data)
    else:
        # Handle the case where no data is found
        return render_template('dashboard/dashboard3.html', data=None)

@app.route("/certificate_info", methods=["POST", "GET", "DELETE", "PUT"])
@loginRequired
def certificate_info():
    if request.method == "POST":
        json_data = request.get_json(force=True)
        url = json_data['url']
        expire_mail_day = json_data['notifybefore']
        created_by = session['userId']
        print(url)
        
        urlAlreadyExist=dashMod.urlAlreadyExist(url, created_by)
        if urlAlreadyExist:
            return {'msg': 'URL Already Exist', 'code': 2}, 500  # Internal Server Error
      

        expire_date = None
        ssl_date_str = dashMod.get_ssl_certificate_expiration(url)
        if ssl_date_str:
            ssl_date = datetime.strptime(ssl_date_str, "%b %d %H:%M:%S %Y GMT")
            # Calculate the current date
            current_date = datetime.now()
            # Calculate the remaining days until the SSL date
            remaining_days = (ssl_date - current_date).days
            print(remaining_days)
            # Check if the remaining days are less than 14
            print("Remaining days are not less than 14.")
            expire_date = ssl_date
            #this if part will not run, temporarily because the expired certificate are all invalid in out implementation
            if remaining_days<0:
                certificate_id = dashMod.create_certificate_info(url, expire_mail_day, created_by, expire_date, status=True, problem_occurred=True)
        
                if certificate_id:
                    return {'msg': f'{certificate_id} created but expired certificate', 'code': 1}, 200  # Created
                else:
                    return {'msg': 'Error creating certificate_info', 'code': 2}, 500  # Internal Server Error
        else:
            print ("URL problem")
            return {'msg': 'Error creating certificate_info Incorrect URL', 'code': 3}, 200  # url problem    
        #search the user id
        #search if the url is valid
        #if valid store find the expiry--store the certificate with expire_date.
        #if sertificate is not valid then store send user that url invalid.
        certificate_id = dashMod.create_certificate_info(url, expire_mail_day, created_by, expire_date, status=True, problem_occurred=False)
        
        if certificate_id:
            return {'msg': f'certificate id {certificate_id} created', 'code': 1}, 200  # Created
        else:
            return {'msg': 'Error creating certificate_info', 'code': 2}, 500  # Internal Server Error
    

    #------------------------------------------------------------------------
    
    if request.method == "PUT":
        json_data = request.get_json(force=True)
        url = json_data.get('url')
        expire_mail_day = json_data.get('expire_mail_day')
        created_by = session['userId']
        ssl_date_str = dashMod.get_ssl_certificate_expiration(url)
        if ssl_date_str:
            ssl_date = datetime.strptime(ssl_date_str, "%b %d %H:%M:%S %Y GMT")
            # Calculate the current date
            current_date = datetime.now()
            # Calculate the remaining days until the SSL date
            remaining_days = (ssl_date - current_date).days
            print(remaining_days)
            # Check if the remaining days are less than 14
            expire_date = ssl_date

            if remaining_days<0:
                certificate_id = dashMod.update_certificate_info(url, expire_mail_day, created_by, expire_date, status=True, problem_occurred=True)
        
                if certificate_id:
                    return {'id': f'{certificate_id} certificate created but expired certificate', 'code': 1}, 200  # Created
                else:
                    return {'msg': 'Error creating certificate_info', 'code': 2}, 500  # Internal Server Error
            

        else:
            print ("URL problem")
            return {'msg': 'Error creating certificate_info Incorrect URL', 'code': 3}, 200  # url problem    

        success = dashMod.update_certificate_info(url, expire_mail_day, created_by, expire_date, status=True, problem_occurred=True)
        
        if success:
            return {'msg': 'Certificate info updated successfully', 'code': 1}, 200  # OK
        else:
            return {'msg': 'Error updating certificate_info', 'code': 2}, 500  # Internal Server Error



    if request.method == "DELETE":
        json_data = request.get_json(force=True)
        id = json_data.get('id')
        #created_by = session['userId']
        success = dashMod.delete_certificate_info(id, session['userId'])

        if success:
            return {'msg': 'Certificate deleted successfully', 'code': 1}, 200  # OK
        else:
            return {'msg': 'Error deleting certificate', 'code': 2}, 500  # Internal Server Error

    if request.method == "GET":
       userID = session['userId']
       certificateData=dashMod.certificateInfo(userID)
       if certificateData:
            return {'msg': certificateData, 'code': 1}, 200  # OK
       else:
            return {'msg': 'Error Finding certificate Info', 'code': 2}, 500  # Internal Server Error
