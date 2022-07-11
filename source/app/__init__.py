# IMPORTS
import datetime
from flask import Flask, render_template, request
import os
import re
import smtplib

# APP INITIALIZATION
app = Flask(__name__)

# DATABASE SETTINGS
#

# DATABASE MODELS
#

# SMTP MAIL SETTINGS
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# APP ROUTES
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "GET": 
        return render_template("contact.html")
    elif request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")

        if not firstname or not lastname or not email:
            error_statement = "All form fields required..."
            return render_template("contact.html", error_statement=error_statement, firstname=firstname, lastname=lastname, email=email)
        else:
            success_statement = "Thank you! We will be in contact with you shortly..."
            message = """\
                Subject: FLASK_APP Contact Request

                Thank you for contacting us! We will be reaching out to you as soon as possible!"""
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, email, message)
            return render_template("contact.html", success_statement=success_statement, firstname=firstname, lastname=lastname, email=email)
    else:
        error_statement = "Bad request..."
        return render_template("contact.html", error_statement=error_statement, firstname=firstname, lastname=lastname, email=email)
