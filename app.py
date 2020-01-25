import flask
from flask import Flask, render_template, flash, request, redirect
import flask_login
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from datetime import datetime
import dataAppend

app = Flask(__name__)
app.secret_key = 'super secret string'  # Change this!

login_manager = flask_login.LoginManager()

login_manager.init_app(app)
db = SQLAlchemy(app)

# # Our mock database.
con = sqlite3.connect('user.db')
cur = con.cursor()
user = cur.execute('select * from users')
user = [i for i in user]
cur.close()
con.close()
users = {user[0][0]:user[0][1]}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):

    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]

    return user

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('index.html')

    email = flask.request.form['email']
    if flask.request.form['password'] == users[email]:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('form'))

    return 'Bad login'



@app.route('/form', methods = ['GET', 'POST'])
@flask_login.login_required
def form():
    if flask.request.method == 'GET':
        return render_template('forms.html')

    timestamp = str(datetime.now())
    print(timestamp)

    data_vals = [timestamp, request.form["worked_out"],
    request.form["muscle_group"],
    request.form["exer_count"],
    request.form["meal_count"],
    request.form["fapped_to"],
    request.form["fap_count"],
    request.form["book"],
    request.form["minutes_read"],
    request.form["mood"],
    request.form["hours_slept"],
    request.form["tv_show"],
    request.form["episode_count"],
    request.form["coffee_count"],
    request.form["dollar_spent"]
    ]
    print(data_vals)
    dataAppend.insert_row(data_vals)
    return flask.redirect(flask.url_for('form'))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('login'))


if __name__ == "__main__":
    app.run()
