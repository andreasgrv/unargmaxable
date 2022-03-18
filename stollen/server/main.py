import os
import json
import datetime
import requests

from flask import Blueprint, request
from flask import current_app as app
from sqlalchemy import and_

from stollen.server.data_model import db
from stollen.server.data_model import Experiment, Model, Result
from stollen.server.utils import response


main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/results', methods=['GET'])
def get_results():
    try:
        results = Result.query.all()
            
        return response(True,
                        msg='Request handled successfully',
                        results=[r.as_dict() for r in results])
    except Exception as e:
        return response(False, msg=repr(e))


@main_routes.route('/results/<query>', methods=['GET'])
def get_results_with_query(query):
    try:
        results = Result.query.join(Experiment).join(Model).filter(Model.name.contains(query))
            
        return response(True,
                        msg='Request handled successfully',
                        results=[r.as_dict() for r in results])
    except Exception as e:
        return response(False, msg=repr(e))


@main_routes.route('/experiments', methods=['GET'])
def get_experiments():
    try:

        experiments = Experiment.query.all()
            
        return response(True,
                        msg='Request handled successfully',
                        # results=[experiments.as_dict()])
                        results=[e.as_dict()
                                 for e in sorted(experiments, key=lambda x: x.num_bounded)])
    except Exception as e:
        return response(False, msg=repr(e))


@main_routes.route('/experiments/<query>', methods=['GET'])
def get_experiments_on_model(query):
    try:
        experiments = Experiment.query.join(Model).filter(Model.name.contains(query))
            
        return response(True,
                        msg='Request handled successfully',
                        results=[e.as_dict() for e in experiments])
    except Exception as e:
        return response(False, msg=repr(e))


@main_routes.route('/bounded_ids/<query>', methods=['GET'])
def get_bounded_ids(query):
    try:
        results = Result.query.filter(Result.is_bounded == True).join(Experiment).join(Model).filter(Model.name.contains(query))
            
        return response(True,
                        msg='Request handled successfully',
                        results=[r.index for r in results if r.is_bounded])
    except Exception as e:
        return response(False, msg=repr(e))
