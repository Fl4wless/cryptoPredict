from flask import Flask, render_template, flash, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import cryptocompare
from forms import RegistrationForm, LoginForm
from flask_moment import Moment
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask("__name__")
app.config['SECRET_KEY']  = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
moment = Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import Prediction, User

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        if request.form['action'] == 'enter':
            confidence = request.form['confidence']
            currency =  request.form['currency']
            target_price =  request.form['target_price']
            date_until =  request.form['date_until']
            confidence = request.form['confidence']
            date_until_formated = datetime.datetime.strptime(date_until, '%Y-%m-%d').date()
            currency_info = cryptocompare.get_price(currency, currency='USD')
            starting_price = currency_info[currency]['USD']
            price_difference = float(target_price) - starting_price

            if not currency and target_price and date_until:
                flash('please fill everything', 'danger')
            else:
                post = Prediction(currency=currency, date_to_target=date_until_formated, target_price=target_price, starting_price=starting_price, confidence=confidence,price_difference=price_difference)
                db.session.add(post)
                db.session.commit()
                return redirect(url_for('feed'))
            return redirect(url_for('feed'))
    return render_template("index.html")

@app.route('/feed')
def feed():
    posts = Prediction.query.order_by(Prediction.date_posted.desc()).all()
    return render_template("feed.html", posts=posts, current_time = datetime.datetime.utcnow())

@app.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data}, you can log in now.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        return redirect(url_for('index'))
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))