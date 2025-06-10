from flask import Flask, request, jsonify, render_template
from utils import is_valid_url
from scanner import check_endpoints

app = Flask(__name__)

# Endpoint to scan the URL for endpoints
@app.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid request body"}), 400

        target_url = data.get("url", "").strip()
        if not is_valid_url(target_url):
            return jsonify({"error": "Invalid URL"}), 400

        results = check_endpoints(target_url)
        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return render_template("dashboard.html")

# Runs the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
