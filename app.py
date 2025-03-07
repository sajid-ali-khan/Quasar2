from flask import Flask
from routes.quiz_routes import quiz_bp

app = Flask(__name__)

# Register Blueprints (modular routes)
app.register_blueprint(quiz_bp)

if __name__ == '__main__':
    app.run(debug=True)
