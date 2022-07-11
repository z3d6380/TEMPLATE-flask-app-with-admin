from flask import Flask, render_template, request

app = Flask(__name__)

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
            return render_template("contact.html", success_statement=success_statement, firstname=firstname, lastname=lastname, email=email)
    else:
        error_statement = "Bad request..."
        return render_template("contact.html", error_statement=error_statement, firstname=firstname, lastname=lastname, email=email)
