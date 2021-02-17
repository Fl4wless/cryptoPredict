from main import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import cryptocompare
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(80), nullable=False)
    date_to_target = db.Column(db.DateTime)
    date_posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    starting_price = db.Column(db.Float(30))
    target_price = db.Column(db.Float(30), nullable=False)
    confidence = db.Column(db.Integer)
    convert = db.Column(db.Integer, default='USD')
    price_difference = db.Column(db.Integer)
    actual_price_difference = db.Column(db.Integer)
    actual_price = db.Column(db.Integer)

    def days_left(self):
        current_date = datetime.utcnow().date()
        target_date = self.date_to_target.date()
        return abs((target_date - current_date).days)


    def ping_actual_price(self):
        get_price = cryptocompare.get_price(self.currency, self.convert)
        self.actual_price = get_price[self.currency][self.convert]
        db.session.add(self)
        db.session.commit()
        return self.actual_price

    def ping_price_difference(self):
        get_price = cryptocompare.get_price(self.currency, self.convert)
        actual_price = get_price[self.currency][self.convert]
        self.actual_price_difference = self.target_price - actual_price
        db.session.add(self)
        db.session.commit()
        return self.actual_price_difference

    def calculate_percentage(self):
        diff = self.ping_price_difference()
        result = ((self.price_difference - diff) / self.price_difference) * 100
        return round(result)



    def __repr__(self):
        return '<Prediction>', self.currency, 'will be', self.target_price, 'from ', self.starting_price

