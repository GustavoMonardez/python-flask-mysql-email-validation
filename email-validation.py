from flask import Flask, render_template, redirect, request, flash
import re
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "secret"
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
mysql = connectToMySQL('emailsdb')
# now, we may invoke the query_db method
# print("all the users", mysql.query_db("SELECT * FROM users;"))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    email = request.form["email"]
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if len(email) < 1:
        flash("Email cannot be blank!")
        return redirect("/")
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
        return redirect("/")
    email = request.form["email"]
    all_emails = mysql.query_db("select email from emails")
    for e in all_emails:
        #print(e["email"])
        if e["email"] == email:
            flash("Email already exists")
            return redirect("/")
    #print(all_emails)
    query = "insert into emails (email, created_at, updated_at) VALUES (%(email)s, now(), now());"
    data = {"email":email}
    mysql.query_db(query, data)
    return redirect("/success")

@app.route("/success")
def success():
    email_selected = mysql.query_db("select email from emails order by id desc limit 1")
    all_emails = mysql.query_db("select * from emails")
    #print(email_selected)
    return render_template("success.html", selected=email_selected, emails=all_emails)

@app.route("/remove", methods=["POST"])
def remove():
    email = request.form["email"]
    remove_email = "delete from emails where email=%(email)s;"
    data = {"email":email}
    mysql.query_db(remove_email, data)
    return redirect("/success")

if __name__ == "__main__":
    app.run(debug=True)