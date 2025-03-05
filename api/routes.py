from api.controllers import auth, client_controller, wishlist_controller

def register_routes(app):
    app.register_blueprint(auth.bp)
    app.register_blueprint(wishlist_controller.bp)
    app.register_blueprint(client_controller.bp)
