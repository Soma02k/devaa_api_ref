from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from app.utils.response import api_response

class AppException(Exception):
    """Base custom application exception."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ValidationError(AppException):
    """Validation exception with HTTP 400 status."""
    def __init__(self, message: str = "Invalid request"):
        super().__init__(message, status_code=400)

class NotFoundException(AppException):
    """Resource not found exception with HTTP 404 status."""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class DuplicateEmailException(AppException):
    """Duplicate email conflict exception with HTTP 400 status."""
    def __init__(self, message: str = "Email already exists"):
        super().__init__(message, status_code=400)

def register_exception_handlers(app):
    """Register centralized global exception handlers with Flask app."""
    
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return api_response(
            status_code=error.status_code,
            is_success=False,
            message=error.message,
            data=None
        )

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return api_response(
            status_code=400,
            is_success=False,
            message=str(error),
            data=None
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        return api_response(
            status_code=500,
            is_success=False,
            message="A database error occurred",
            data=None
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return api_response(
            status_code=error.code,
            is_success=False,
            message=error.description or "HTTP Error",
            data=None
        )

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return api_response(
            status_code=500,
            is_success=False,
            message=f"An unexpected error occurred: {str(error)}",
            data=None
        )
