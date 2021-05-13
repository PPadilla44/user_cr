from flask_app import app
from flask import render_template,redirect,request

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

@app.route("/")
def index():
    return render_template("read_all.html", all_users = User.get_all())

@app.route("/create")
def show_create(): return render_template("create.html")

@app.route("/create/user", methods=["POST"])
def create_user():
    User.save(request.form)
    return redirect("/")

@app.route("/show_one/<userid>")
def show_one(userid):
    data = {
        'id': userid
    }
    return render_template("show_one.html", user = User.get_by_id(data))

@app.route("/delete/<userid>")
def delete_one(userid):
    data = {
        'id': userid
    }
    User.delete(data)
    return redirect('/')

@app.route("/edit/<userid>")
def show_edit(userid):
    data = {
        'id': userid
    }
    return render_template('edit.html', user = User.get_by_id(data))

@app.route("/edit/submit/<userid>", methods=['POST'])
def submit_edit(userid):
    data = {
        'fn' : request.form['fname'],
        'ln' : request.form['lname'],
        'em' : request.form['email'],
        'id' : userid,
    }
    User.update(data)
    return redirect("/")