from flask import Blueprint, jsonify, abort, request, session
from ..models import Exercise, User, db, food_tracker_table, Food, exercises_tracker_table
import hashlib
import secrets
import sqlalchemy
import datetime


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def index():
    users = User.query.all()
    result = []
    for usr in users:
        result.append(usr.serialize())
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    usr = User.query.get_or_404(id)
    return jsonify(usr.serialize())


@bp.route('', methods=['POST'])
def create():
    if "username" not in request.json \
            or "password" not in request.json \
            or len(request.json["username"]) < 3 \
            or len(request.json["password"]) < 8:
        return abort(400)
    usr = User(
        request.json["username"],
        scramble(request.json["password"])
    )
    if 'heigt' in request.json:
        usr.height = request.json["height"]
    if 'weight' in request.json:
        usr.current_weight = request.json["weight"]
    db.session.add(usr)
    db.session.commit()
    return jsonify(usr.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    usr = User.query.get_or_404(id)
    try:
        db.session.delete(usr)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>', methods=['PATCH'])
def update(id: int):
    usr = User.query.get_or_404(id)
    try:
        if not request.json:
            return abort(400)
        if "username" in request.json:
            if len(request.json["username"]) < 3:
                return jsonify(False)
            usr.username = request.json["username"]
        if "password" in request.json:
            if len(request.json["password"]) < 8:
                return jsonify(False)
            usr.password = scramble(request.json["password"])
        if 'height' in request.json:
            usr.height = request.json["height"]
        if 'weight' in request.json:
            usr.current_weight = request.json["weight"]
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>/food_records/<date>', methods=['GET'])
def food_tracker(id: int, date: str):
    try:
        date = datetime.date.fromisoformat(date)
    except:
        abort(404)
    usr = User.query.get_or_404(id)
    stmt = sqlalchemy.select(food_tracker_table.join(Food)).where(
        food_tracker_table.c.user_id == usr.id, sqlalchemy.func.date(food_tracker_table.c.date) == date)
    result = {"records": [], }
    records = db.session.execute(stmt)
    for record in records:
        result["records"].append(
            {
                "user_id": record.user_id,
                "food_name": record.name,
                "calories_per_serving": record.calories * record.amount/100,
                "calories_per_100g": record.calories,
                "amount (g)": record.amount
            }
        )
    result["total"] = {
        "total_calories": sum([item["calories_per_serving"] for item in result["records"]])
    }  # TODO add here total proteins, fats and carbs
    return jsonify(result)


@bp.route('/<int:id>/food_tracker', methods=['POST'])
def food_tracker_create(id: int):
    usr = User.query.get_or_404(id)
    if "food_id" not in request.json or "amount" not in request.json:
        return abort(400)
    food_item = Food.query.get_or_404(request.json["food_id"])
    stmt = sqlalchemy.insert(food_tracker_table).values(
        user_id=usr.id, food_id=food_item.id, amount=request.json["amount"])
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>/exercises_records/<date>', methods=['GET'])
def exercises_tracker(id: int, date: str):
    try:
        date = datetime.date.fromisoformat(date)
    except:
        abort(404)
    usr = User.query.get_or_404(id)
    stmt = sqlalchemy.select(exercises_tracker_table.join(Exercise)).where(
        exercises_tracker_table.c.user_id == usr.id, sqlalchemy.func.date(exercises_tracker_table.c.date) == date)
    result = {"records": [], }
    records = db.session.execute(stmt)
    for record in records:
        result["records"].append(
            {
                "user_id": record.user_id,
                "exercise_name": record.name,
                "duration": record.duration,
                "sets": record.sets,
                "reps": record.reps,
                "weight": record.weight
            }
        )
    return jsonify(result)


@bp.route('/<int:id>/exercises_tracker', methods=['POST'])
def exercises_tracker_cre(id: int):
    usr = User.query.get_or_404(id)
    if "exercise_id" not in request.json:
        return abort(400)
    exercise = Exercise.query.get_or_404(request.json["exercise_id"])
    keys = ["weight", "duration", "sets", "reps"]
    values = {key: request.json.get(key, None) for key in keys}
    values["user_id"] = usr.id
    values["exercise_id"] = exercise.id
    stmt = sqlalchemy.insert(exercises_tracker_table).values(**values)
    try:
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
