from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Food, food_tracker_table
import sqlalchemy

bp = Blueprint('food', __name__, url_prefix='/food')


@bp.route('', methods=['GET'])
def index():
    food_lst = Food.query.all()
    result = []
    for item in food_lst:
        result.append(item.serialize())
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    item = Food.query.get_or_404(id)
    return jsonify(item.serialize())


@bp.route('', methods=['POST'])
def create():
    if "name" not in request.json \
            or "calories" not in request.json:
        return abort(400)
    item = Food(
        request.json["name"],
        request.json["calories"]
    )
    if "proteins" in request.json:
        item.proteins = request.json["proteins"]
    if "fats" in request.json:
        item.fats = request.json["fats"]
    if "carbs" in request.json:
        item.carbs = request.json["carbs"]
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    item = Food.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


@bp.route('/<int:id>', methods=['PATCH'])
def update():
    if not request.json:
        return abort(400)
    item = Food.query.get_or_404(id)
    if "calories" in request.json:
        item.calories = request.json["calories"]
    if "name" in request.json:
        item.name = request.json["name"]
    if "proteins" in request.json:
        item.proteins = request.json["proteins"]
    if "fats" in request.json:
        item.fats = request.json["fats"]
    if "carbs" in request.json:
        item.carbs = request.json["carbs"]
    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize())
