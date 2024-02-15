from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # Initialize Flask application
app.secret_key = "secret"  # Set secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'  # Configure SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy track modifications
app.permanent_session_lifetime = timedelta(minutes=5)  # Set session lifetime

db = SQLAlchemy(app)  # Initialize SQLAlchemy database


# Define database model
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)  # Define primary key
    name = db.Column(db.String(100))  # Define name column
    email = db.Column(db.String(100))  # Define email column

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")  # Define route for home page
def home():
    return render_template("index.html", content="Home Page")  # Render home page template


@app.route("/view")  # Define route for viewing users
def view():
    return render_template("view.html", values=users.query.all())  # Render view template with user data


@app.route("/login", methods=["POST", "GET"])  # Define route for login
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))  # Redirect to user route upon successful login
    else:
        if "user" in session:
            flash("Already Logged In!")
            return redirect(url_for("user"))  # Redirect to user route if already logged in
        return render_template("login.html")  # Render login template


@app.route("/user", methods=["POST", "GET"])  # Define route for user profile
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("email was saved")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)  # Render user profile template with email data
    else:
        flash("You are not Logged In!")
        return redirect(url_for("login"))  # Redirect to login route if not logged in


@app.route("/logout")  # Define route for logout
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))  # Redirect to login route after logout


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)  # Run the Flask application
