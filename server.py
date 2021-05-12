from flask import Flask, render_template, redirect, request
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection
app = Flask(__name__)
@app.route("/")
def index():
    mysql = connectToMySQL('users_schema')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    return render_template("read_all.html", all_users = users)

@app.route("/create")
def show_create(): return render_template("create.html")

@app.route("/create/user", methods=["POST"])
def create_user():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        'fn' : request.form['fname'],
        'ln' : request.form['lname'],
        'em' : request.form['email'],
    }
    db = connectToMySQL('users_schema')
    db.query_db(query, data)
    return redirect("/")

@app.route("/show_one/<userid>")
def show_one(userid):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {'id' : userid}
    db = connectToMySQL('users_schema')
    info = db.query_db(query, data)
    return render_template("show_one.html", user = info)

@app.route("/delete/<userid>")
def delete_one(userid):
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {'id' : userid}
    db = connectToMySQL('users_schema')
    db.query_db(query, data)
    return redirect('/')

@app.route("/edit/<userid>")
def show_edit(userid):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {'id' : userid}
    db = connectToMySQL('users_schema')
    info = db.query_db(query, data)
    return render_template('edit.html', user = info)

@app.route("/edit/submit/<userid>", methods=['POST'])
def submit_edit(userid):
    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(em)s, updated_at = NOW() WHERE id = %(id)s;"
    data = {
        'fn' : request.form['fname'],
        'ln' : request.form['lname'],
        'em' : request.form['email'],
        'id' : userid,
    }
    print(query)
    db = connectToMySQL('users_schema')
    db.query_db(query, data)
    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)