import os

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from stollen.server.data_model import db
from stollen.server.main import main_routes


def create_app():
    db_uri = 'postgresql://%s:%s@%s:%s/%s?sslmode=%s' % (os.environ['DB_USER'],
                                              os.environ['DB_PASSWD'],
                                              os.environ['DB_HOST'],
                                              os.environ['DB_PORT'],
                                              os.environ['DB_NAME'],
                                              os.environ['DB_SSL'])

    app = Flask(__name__,
                static_url_path='')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}
    app.config['DEBUG'] = True
    # Add NLP related webservices
    app.register_blueprint(main_routes, url_prefix='/api')

    cors = CORS(app)
    db.init_app(app)
    Migrate(app, db, compare_type=True)
    # global options
    return app, db


app, _ = create_app()


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ['PORT'])
