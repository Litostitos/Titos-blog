from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()


app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()


@app.route('/')
def home():

    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        new_user = User()
        new_user.email = request.form['email']
        new_user.name = request.form['name']
        new_user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)

        db.session.add(new_user)
        db.session.commit()

        return render_template("secrets.html", name=new_user.name)

    return render_template("register.html")



@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    return render_template("login.html")


@app.route('/download')
def download():

    return send_from_directory('static', filename="files/cheat_sheet.pdf")

@login_manager.user_loader
def load_user(id):
    return User.get(id)


if __name__ == "__main__":
    app.run(debug=True)
