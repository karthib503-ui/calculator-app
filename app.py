import os
from flask import Flask, request, jsonify

app = Flask(__name__)

HOSTNAME = os.getenv('HOSTNAME', 'unknown-host')


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "hostname": HOSTNAME}), 200


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON body", "hostname": HOSTNAME}), 400

    operation = data.get('operation')
    a = data.get('a')
    b = data.get('b')

    if operation is None or a is None or b is None:
        return jsonify({
            "error": "Request must include 'operation', 'a', and 'b'",
            "hostname": HOSTNAME
        }), 400

    try:
        a = float(a)
        b = float(b)
    except (ValueError, TypeError):
        return jsonify({"error": "'a' and 'b' must be numeric", "hostname": HOSTNAME}), 400

    if operation == 'add':
        result = a + b
    elif operation == 'subtract':
        result = a - b
    elif operation == 'multiply':
        result = a * b
    elif operation == 'divide':
        if b == 0:
            return jsonify({"error": "Division by zero is not allowed", "hostname": HOSTNAME}), 400
        result = a / b
    else:
        return jsonify({
            "error": f"Unsupported operation '{operation}'. Use add, subtract, multiply, or divide.",
            "hostname": HOSTNAME
        }), 400

    return jsonify({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result,
        "hostname": HOSTNAME
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)