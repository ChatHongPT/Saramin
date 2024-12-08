from flask import request, jsonify

def validate_request(required_fields):
    data = request.json
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"message": f"Missing fields: {', '.join(missing_fields)}"}), 400
    return data
