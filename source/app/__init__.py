# IMPORTS
import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request
import os
from peewee import *
from playhouse.shortcuts import model_to_dict
import re
import smtplib

# APP INITIALIZATION
load_dotenv()
app = Flask(__name__)

# REGULAR EXPRESSIONS
email_re = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

# DATABASE SETTINGS
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")


if os.getenv("TESTING") == "true":
    print("Running in test mode => Using Sqlite in memory")
    db = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    db = MySQLDatabase(MYSQL_DATABASE,user=MYSQL_USER,password=MYSQL_PASSWORD,host=MYSQL_HOST,port=MYSQL_PORT)

print(db)

# DATABASE MODELS

## Contact Model
class Contact(Model):
    firstname = CharField()
    lastname = CharField()
    email = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = db

# DATABASE CONNECT AND INITIALIZE
db.connect()
db.create_tables([Contact])

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
        elif not re.fullmatch(email_re, email):
            error_statement = "Email format invalid..."
            return render_template("contact.html", error_statement=error_statement, firstname=firstname, lastname=lastname, email=email)
        else:
            success_statement = "Thank you! We will be in contact with you shortly..."
            message = """Thank you for contacting us! We will be reaching out to you as soon as possible!"""
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, email, message)
            Contact.create(firstname=firstname, lastname=lastname, email=email)
            return render_template("contact.html", success_statement=success_statement, firstname=firstname, lastname=lastname, email=email)
    else:
        error_statement = "Bad request..."
        return render_template("contact.html", error_statement=error_statement, firstname=firstname, lastname=lastname, email=email)
