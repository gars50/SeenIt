from app.api import bp
from time import sleep
from flask import request, current_app
from flask_login import login_required
from app.scripts.media import test_ombi, test_radarr, test_sonarr
import jsonschema
from jsonschema import validate

valid_ip_address_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
valid_hostname_regex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
alphanumeric_regex = "^[a-zA-Z0-9]+$"


api_schema= {
    "type" : "object",
    "properties" : {
        "host" : { 
            "type" : "string",
            "anyOf" : [
                {
                    "pattern": valid_ip_address_regex
                },
                {
                    "pattern": valid_hostname_regex
                }
            ]
        },
        "port" : {
            "type" : "integer"
        },
        "api_key" : {
            "type" : "string",
            "pattern" : alphanumeric_regex
        },
    }
}

def validate_json(data):
    try:
        validate(data, schema=api_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


@bp.route('/settings/test_ombi_from_server', methods=['POST'])
@login_required
def test_ombi_from_server():
    data = request.get_json()
    if validate_json(data):
        return test_ombi(data['host'], data['port'], data['api_key'])
    else:
        return {
            "error" : "Bad input"
        }, 400

@bp.route('/settings/test_radarr_from_server', methods=['POST'])
@login_required
def test_radarr_from_server():
    data = request.get_json()
    if validate_json(data):
        return test_radarr(data['host'], data['port'], data['api_key'])
    else:
        return {
            "error" : "Bad input"
        }, 400

@bp.route('/settings/test_sonarr_from_server', methods=['POST'])
@login_required
def test_sonarr_from_server():
    data = request.get_json()
    if validate_json(data):
        return test_sonarr(data['host'], data['port'], data['api_key'])
    else:
        return {
            "error" : "Bad input"
        }, 400

@login_required
def stream_log(file):
    def generate():
        with open(file) as log_file:
            #Give the last 40 lines as a starter
            all_lines = log_file.readlines()
            last_few_lines = all_lines[-40:]
            for line in last_few_lines:
                yield line

            #Stream now lines afterwards
            while True:
                lines = log_file.readlines()
                if lines:
                    for line in lines:
                        yield line
                else:
                    sleep(1)
    return current_app.response_class(generate(), mimetype='text/plain')

@bp.route('/settings/logs/app', methods=['GET'])
@login_required
def stream_applog():
    return stream_log('logs/app.log')
    

@bp.route('/settings/logs/www', methods=['GET'])
@login_required
def stream_wwwlog():
    return stream_log('logs/www.log')