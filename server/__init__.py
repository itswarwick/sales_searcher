from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def home():
        return "Welcome to Fetch Order History"
    
    from .routes.salessearcher import salessearcher
    app.register_blueprint(salessearcher, url_prefix='/api')
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)