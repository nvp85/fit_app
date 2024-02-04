from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt                     
from ..wsgi import app

db = SQLAlchemy()


food_tracker_table = db.Table(
    'food_tracker',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'food_id', db.Integer,
        db.ForeignKey('food.id'),
        primary_key=True
    ),

    db.Column(
        'amount', db.Integer,
        nullable=False
    ),

    db.Column(
        'date', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) # it's password hash actually
    height = db.Column(db.Integer, nullable=True)
    current_weight = db.Column(db.Integer, nullable=True)
    food_records = db.relationship(
        'Food', secondary=food_tracker_table, lazy='subquery')

    def __init__(self, username, password, height=None, weight=None):
        self.username = username
        self.hash_password(password)
        self.height = height
        self.current_weight = weight

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "height": self.height,
            "weight": self.current_weight
        }

    def hash_password(self, password):
        self.password = generate_password_hash(password, salt_length=16)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_auth_token(self, expiration=600):
        return jwt.encode({'id': self.id, 'exp': datetime.now(tz=datetime.timezone.utc)+expiration}, 
                           app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithm=['HS256'])
        except:
            return
        return User.query.get(data['id'])


class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(280), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    proteins = db.Column(db.Integer, nullable=True)
    fats = db.Column(db.Integer, nullable=True)
    carbs = db.Column(db.Integer, nullable=True)

    def __init__(self, name: str, calories: int, prots=None, fats=None, carbs=None):
        self.name = name
        self.calories = calories
        self.proteins = prots
        self.fats = fats
        self.carbs = carbs

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories,
            'proteins': self.proteins,
            'fats': self.fats,
            'carbs': self.carbs
        }


class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(280), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, description=None):
        self.name = name

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


exercises_tracker_table = db.Table(
    'exercises_tracker',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'exercise_id', db.Integer,
        db.ForeignKey('exercise.id'),
        primary_key=True
    ),

    db.Column(
        'date', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    ),

    db.Column(
        'duration', db.Interval,
        nullable=True
    ),

    db.Column(
        'weight', db.Integer,
        nullable=True
    ),

    db.Column(
        'sets', db.Integer,
        nullable=True
    ),

    db.Column(
        'reps', db.Integer,
        nullable=True
    )
)
