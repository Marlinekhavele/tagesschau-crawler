from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# app.register_blueprint(ws, url_prefix='/workers')



CORS(app)
@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to Blukers CRM API"


if __name__ == '__main__':
    app.run(debug=True)