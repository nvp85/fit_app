from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Exercise, food_tracker_table
import sqlalchemy

bp = Blueprint('exercises', __name__, url_prefix='/exercises')


@bp.route('', methods=['GET'])
def index():
    exercises_lst = Exercise.query.all()
    result = []
    for item in exercises_lst:
        result.append(item.serialize())
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    item = Exercise.query.get_or_404(id)
    return jsonify(item.serialize())


@bp.route('', methods=['POST'])
def create():
    if "name" not in request.json:
        return abort(400)
    item = Exercise(
        request.json["name"]
    )
    if "description" in request.json:
        item.description = request.json["description"]

    db.session.add(item)
    db.session.commit()
    return jsonify(item.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    item = Exercise.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
