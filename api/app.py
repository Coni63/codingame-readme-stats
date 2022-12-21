import asyncio

from flask import Flask, request
from flask_cors import CORS

import application.user_data 
import application.svg_builder

app = Flask(__name__)
CORS(app)

@app.route("/api/details/<codingamer>", methods=['GET'])
def get_card_for(codingamer):
    user_datas = asyncio.run(application.user_data.get_all_data(codingamer))
    svg = application.svg_builder.render(user_datas)

    if svg is not None:
        return svg, 200
    else:
        return {}, 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)