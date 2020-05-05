import json
from flask import Blueprint, Response, abort, request
from app import db
from sqlalchemy.exc import SQLAlchemyError
from .models import Engineers
from app.studio import permissions

sound_engineer = Blueprint('sound_engineer', __name__)

# import serializers and deserializers
from .serializers import (engineer_schema,
                          create_engineer_schema, update_engineer_schema)


@sound_engineer.route('/engineer/create', methods=['POST'])
@permissions.studio_login_required
def create(user_id):
    errors = create_engineer_schema.validate(request.json)
    if errors:
        return abort(Response(json.dumps(errors), 400, mimetype='application/json'))
    details = request.json
    studio_id = user_id
    name = details['name']
    role = details['role']

    try:
        engineer = Engineers(name=name, role=role, studio_id=studio_id)
        db.session.add(engineer)
        db.session.commit()
        result = engineer_schema.dumps(engineer)
        return Response(result, 201, mimetype='application/json')
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


@sound_engineer.route('/engineer/<int:engineer_id>/update', methods=['PATCH'])
@permissions.studio_login_required
def update(engineer_id, user_id):
    errors = update_engineer_schema.validate(request.json)
    if errors:
        return abort(Response(json.dumps(errors), 400, mimetype='application/json'))

    try:
        details = request.json
        engineer = Engineers.query.filter_by(id=engineer_id, studio_id=user_id)
        engineer.update(dict(details))
        db.session.commit()
        return Response(engineer_schema.dumps(engineer))
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return error


# TODO: delete engineer

