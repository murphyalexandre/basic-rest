from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

DATABASE = 'database.db'

# create app
app = Flask(__name__)

# setup db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basic-rest.db'
db = SQLAlchemy(app)

# register blueprints
from app.views import basic_rest
app.register_blueprint(basic_rest)


# Run server
if __name__ == '__main__':
    app.run()
