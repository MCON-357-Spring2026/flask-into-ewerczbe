from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def welcome():
    return "<h1>Welcome to My Flask API!</h1>"

@app.route("/about")
def about():
    return jsonify({
        "name": "Etty Werczberger",
        "course": "MCON-357 - Practicum",
        "semester": "Spring 2026"
    })

@app.route("/greet/<name>")
def greet(name):
    return f"<p>Hello, {name}! Welcome to Flask.</p>"

@app.route("/calculate")
def calculate():
    num1 = float(request.args.get("num1", 0))
    num2 = float(request.args.get("num2", 0))
    operation = request.args.get("operation")
    try:
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            result = num1 / num2
        else:
            return jsonify({"error": "Invalid operation"}), 400
        return jsonify({"result": result, "operation": operation})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred during calculation"}), 500

@app.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    data["echoed"] = True
    return jsonify(data)

@app.route("/status/<int:code>")
def status(code):
    return f"This is a {code} error", code

@app.before_request
def log_request():
    print(f"Before Request: {request.method} {request.path}")

@app.after_request
def add_custom_header(response):
    response.headers["X-Custom-Header"] = "FlaskRocks"
    return response

@app.teardown_request
def teardown_request(exception):
    if exception:
        print(f"Teardown Request: Exception occurred - {exception}")

@app.route("/debug/routes")
def show_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "path": str(rule)
        })
    return jsonify(routes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)