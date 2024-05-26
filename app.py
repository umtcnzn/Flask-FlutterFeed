from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    with app.app_context():
        from routes import auth_routes,html_routes,user_routes,post_routes,comment_routes  # import routes
        app.register_blueprint(auth_routes.bp)
        app.register_blueprint(html_routes.bp)
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(post_routes.bp)
        app.register_blueprint(comment_routes.bp)

    return app
