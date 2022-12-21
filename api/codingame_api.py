import requests
import json
import fake_data

import constants


def get_info_for(codingamer):
    return fake_data.FAKE_USER

    json = [codingamer]
    req = requests.post(constants.CG_USER_GLOBAL_STATS, json=json, headers=constants.CG_headers)
    return req.json()

def get_certifications_for(userid):
    return fake_data.FAKE_CERTIF

    json = [userid]
    req = requests.post(constants.CG_USER_CERTIFICATIONS, json=json, headers=constants.CG_headers)
    return req.json()

def get_languages_used_by(userid):
    return fake_data.FAKE_LANGUAGES

    json = [userid]
    req = requests.post(constants.CG_USER_LANGUAGE, json=json, headers=constants.CG_headers)
    return req.json()

def get_achievements_for(userid):
    return fake_data.FAKE_ACHIVEMENTS

    json = [userid]
    req = requests.post(constants.CG_USER_ACHIEVEMENTS, json=json, headers=constants.CG_headers)
    return req.json()