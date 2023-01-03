from flask import Flask, request
from flask_cors import CORS

from application.app_logic import get_svg_for_user

app = Flask(__name__)
CORS(app)


@app.route("/api/details/<codingamer>", methods=['GET'])
def get_card_for(codingamer):
    online_str = request.args.get('online', "false")
    online = online_str.lower() == "true"

    second_category = request.args.get('display')
    if second_category not in ["certifications", "languages"]:
        second_category = None

    second_category_number_str = request.args.get('top', "6")
    second_category_number = int(second_category_number_str)

    svg = get_svg_for_user(codingamer, 
                           online=online, 
                           second_category=second_category, 
                           second_category_number=second_category_number)

    if svg is not None:
        return svg, 200
    else:
        return {"message": "error when generating the image"}, 500


@app.after_request
def add_header(response):
    if response.status_code == 200:
        response.cache_control.max_age = 86400
        response.cache_control.public = True
        response.cache_control.s_maxage = 86400
        response.content_type = "image/svg+xml"
        return response
    else:
        response.content_type = "application/json"
        return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
