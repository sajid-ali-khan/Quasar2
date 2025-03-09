from flask import Flask
from flask_cors import CORS
from routes.quiz_routes import quiz_bp
from routes.resource_routes import res_bp

app = Flask(__name__)

# Enable CORS
CORS(app)

# Register Blueprints (modular routes)
app.register_blueprint(quiz_bp)
app.register_blueprint(res_bp)

if __name__ == '__main__':
    app.run(debug=True)
