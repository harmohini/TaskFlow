from flask import Flask, render_template, redirect, url_for
from config import Config
from database.db import Database

# Import Route Blueprints
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.project_routes import project_bp
from routes.task_routes import task_bp
from routes.workflow_routes import workflow_bp

# ---------------------------------------------------
# Create Flask App
# ---------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

# Secret Key
app.secret_key = Config.SECRET_KEY

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------

db = Database()
db.connect()

# ---------------------------------------------------
# Register Blueprints
# ---------------------------------------------------

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(project_bp)
app.register_blueprint(task_bp)
app.register_blueprint(workflow_bp)

# ---------------------------------------------------
# Error Handlers
# ---------------------------------------------------


@app.errorhandler(404)
def page_not_found(error):
    """Render custom 404 page."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Render custom 500 page."""
    return render_template("500.html"), 500


# ---------------------------------------------------
# Entry Point
# ---------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)