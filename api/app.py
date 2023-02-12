from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from application.app_logic import get_svg_for_user

app = Flask(__name__)
CORS(app)


# add a limit of requeste per IP address -- only valid in non debug mode for testing purposes
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60/hour;200/day"],
    default_limits_exempt_when=lambda: app.debug
)


@app.route("/api/details/<codingamer>", methods=['GET'])
def get_card_for(codingamer):
    first_category = request.args.get('first', "").lower()
    if first_category not in ["certifications", "languages", "leaderboard", "puzzles"]:
        first_category = "leaderboard"

    second_category = request.args.get('second', "").lower()
    if second_category not in ["certifications", "languages", "leaderboard", "puzzles"]:
        second_category = None

    third_category = request.args.get('third', "").lower()
    if third_category not in ["certifications", "languages", "leaderboard", "puzzles"]:
        third_category = None

    language_number_str = request.args.get('top', "6")
    language_number = int(language_number_str)

    night_str = request.args.get('night', "false").lower()
    night = night_str in ["1", "true", "yes"]

    svg, response_code = get_svg_for_user(codingamer, 
                                          first_category=first_category,
                                          second_category=second_category, 
                                          third_category=third_category, 
                                          language_number=language_number,
                                          night=night)

    return svg, response_code


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
