from flask import jsonify

def success_response(data=None, pagination=None):
    response = {"status": "success", "data": data or {}}
    if pagination:
        response["pagination"] = pagination
    return jsonify(response)

def error_response(message, code="ERROR_CODE"):
    return jsonify({"status": "error", "message": message, "code": code}), 400
