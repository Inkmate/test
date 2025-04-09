import os
from flask import Flask
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.print_routes import print_bp
from routes.search_routes import search_bp  # ✅ added

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(print_bp)
app.register_blueprint(search_bp)  # ✅ registered

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
