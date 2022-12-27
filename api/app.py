import asyncio

from flask import Flask, request
from flask_cors import CORS

from application import user_data, svg_builder, leveler

app = Flask(__name__)
CORS(app)

@app.route("/api/details/<codingamer>", methods=['GET'])
def get_card_for(codingamer):
    user_datas = asyncio.run(user_data.get_all_data(codingamer))
    profile_data = leveler.get_profile_data(user_datas)
    svg = svg_builder.render(profile_data)

    if svg is not None:
        return svg, 200
    else:
        return {}, 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)