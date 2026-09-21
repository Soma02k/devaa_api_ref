from flask import jsonify

def api_response(status_code: int, is_success: bool, message: str, data=None):
    """
    Global API response formatter required across all endpoints.
    
    :param status_code: HTTP Status Code (e.g., 200, 201, 400, 404, 500)
    :param is_success: Boolean indicating if operation succeeded
    :param message: Descriptive message for response
    :param data: Response data payload (dict, list, or None)
    :return: Flask Response object tuple (json, status_code)
    """
    response_body = {
        "status_code": status_code,
        "is_success": is_success,
        "message": message,
        "data": data
    }
    return jsonify(response_body), status_code
