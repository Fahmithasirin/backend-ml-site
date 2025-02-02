from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for cross-origin requests
    app.config['UPLOAD_FOLDER'] = 'datasets/'
    app.config['VISUALIZATION_FOLDER'] = 'visualizations/'

    from .routes import main
    app.register_blueprint(main)

    return app
