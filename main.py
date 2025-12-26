from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Serverless! 🚀\n"

@app.route('/echo', methods=['POST'])
def echo():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)