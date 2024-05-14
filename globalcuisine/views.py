from flask import Flask
from .main import main as main_blueprint
from . import db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_blueprint)
    db.create_all(app=app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
