from app.api import bp
from time import sleep
from flask import request, current_app
from flask_login import login_required
from app.scripts.media import test_ombi, test_radarr, test_sonarr

@bp.route('/settings/test_ombi_from_server', methods=['POST'])
@login_required
def test_ombi_from_server():
    data = request.get_json()
    ombi_host = data['ombi_host']
    ombi_port = data['ombi_port']
    ombi_api_key = data['ombi_api_key']
    return test_ombi(ombi_host, ombi_port, ombi_api_key)

@bp.route('/settings/test_radarr_from_server', methods=['POST'])
@login_required
def test_radarr_from_server():
    data = request.get_json()
    radarr_host = data['radarr_host']
    radarr_port = data['radarr_port']
    radarr_api_key = data['radarr_api_key']
    return test_radarr(radarr_host, radarr_port, radarr_api_key)

@bp.route('/settings/test_sonarr_from_server', methods=['POST'])
@login_required
def test_sonarr_from_server():
    data = request.get_json()
    sonarr_host = data['sonarr_host']
    sonarr_port = data['sonarr_port']
    sonarr_api_key = data['sonarr_api_key']
    return test_sonarr(sonarr_host, sonarr_port, sonarr_api_key)

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