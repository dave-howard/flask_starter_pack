from flaskr import app, login_manager
from flaskr.models import session, User
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, current_user, logout_user, AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
import os


@login_manager.user_loader
def load_user(userid):
    print(f"@login_manager.user_loader(user_id={userid})")
    u = User.get_by_id(int(userid))
    return u


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    print("signup")
    if request.method == 'POST':
        print(request.form)
        user_name = request.form.get('username')
        password = request.form.get('password')

        if User.get_by_user_name(user_name):
            flash("User name already in use.")
        else:
            user = User(user_name=user_name, password_hash=generate_password_hash(password))
            # set first user as admin role
            if len(User.all()) == 0:
                user.role = "admin"
            else:
                user.role = "user"
            user.status = "enabled"  # todo: add function to allow admin to enable new users
            session().add(user)
            session().commit()

            return login()
    return render_template("signup.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    print("login")
    if request.method == 'POST':
        print(request.form)
        user_name = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_user_name(user_name)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # authenticate user with flask_login
            return home()

    return render_template("login.html")


# send to login page when a user accesses a page they are not authorised to
login_manager.unauthorized_callback = login


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    print("logout")
    logout_user()
    return redirect(url_for('home'))


@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html")

