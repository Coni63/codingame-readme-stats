from flask import Flask, request
from flask_cors import CORS

import application
import codingame_api

app = Flask(__name__)
CORS(app)

@app.route("/api/details/<codingamer>", methods=['GET'])
def get_card_for(codingamer):
    data = application.get_all_data(codingamer)

    if data is not None:
        return data, 200
    else:
        return {}, 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)