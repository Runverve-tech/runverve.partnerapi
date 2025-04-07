from flask import jsonify
from extensions import db

class ErrorHandler:
    @staticmethod
    def init_app(app):
        """Initialize error handlers for the app"""
        
        @app.errorhandler(400)
        def bad_request(e):
            return jsonify({"error": "Bad request", "message": str(e)}), 400
            
        @app.errorhandler(401)
        def unauthorized(e):
            return jsonify({"error": "Unauthorized", "message": str(e)}), 401
            
        @app.errorhandler(403)
        def forbidden(e):
            return jsonify({"error": "Forbidden", "message": str(e)}), 403
            
        @app.errorhandler(404)
        def not_found(e):
            return jsonify({"error": "Not found", "message": str(e)}), 404
            
        @app.errorhandler(500)
        def server_error(e):
            return jsonify({"error": "Internal server error", "message": str(e)}), 500