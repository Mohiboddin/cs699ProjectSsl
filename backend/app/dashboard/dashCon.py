from app import app
from flask import render_template, redirect, request, session, jsonify, make_response, url_for
from app.dashboard import dashMod
from app.auth.authCon import loginRequired
import random
from functools import wraps


@app.route("/dashboard", methods=["GET"])
@loginRequired
def dashboard():
    userId = session["userId"]
    data = dashMod.certificateInfo(userId)
    print("returning dashboard page")
    if data is not None:
        return render_template('dashboard/dashboard.html', data=data)
    else:
        # Handle the case where no data is found
        return render_template('dashboard/dashboard.html', data=None)
