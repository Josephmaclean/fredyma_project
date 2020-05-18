import json
from flask import Blueprint, Response, abort, request
from sqlalchemy.exc import SQLAlchemyError

from app import db


from .models import Engineers
from .serializers import create_engineer_schema, engineer_schema, \
    update_engineer_schema
from .permissions import studio_login_required

engineers = Blueprint('engineers', __name__)


@engineers.route('/engineer/create', methods=['POST'])
@studio_login_required
def create(user_id):
    errors = create_engineer_schema.validate(request.json)
    if errors:
        return abort(Response(json.dumps(errors), 400, mimetype='application/json'))
    details = request.json
    studio_id = user_id
    name = details['name']
    role = details['role']

    try:
        engineer_instance = Engineers(name=name, role=role, studio_id=studio_id)
        db.session.add(engineer_instance)
        db.session.commit()
        result = engineer_schema.dumps(engineer_instance)
        return Response(result, 201, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@engineers.route('/engineer/<int:engineer_id>', methods=['PATCH'])
@studio_login_required
def update(engineer_id, user_id):
    errors = update_engineer_schema.validate(request.json)
    if errors:
        return abort(Response(json.dumps(errors), 400, mimetype='application/json'))

    try:
        details = request.json
        engineer_instance = Engineers.query.filter_by(id=engineer_id, studio_id=user_id)
        engineer_instance.update(dict(details))
        db.session.commit()
        return Response(engineer_schema.dumps(engineer_instance))
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@engineers.route('/engineer/<int:engineer_id>/delete', methods=['DELETE'])
@studio_login_required
def delete(user_id, engineer_id):
    engineer_instance = Engineers.query.filter_by(id=engineer_id, studio_id=user_id)
    engineer_instance.delete()
    db.session.commit()
    return Response("", 204, mimetype='application/json')
