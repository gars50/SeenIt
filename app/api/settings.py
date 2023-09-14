from app.api import bp
from flask import request
from app.scripts.media import test_ombi, test_radarr, test_sonarr

@bp.route('/settings/test_ombi_from_server', methods=['POST'])
def test_ombi_from_server():
    ombi_host = request.json['ombi_host']
    ombi_port = request.json['ombi_port']
    ombi_api_key = request.json['ombi_api_key']
    return test_ombi(ombi_host, ombi_port, ombi_api_key)

@bp.route('/settings/test_radarr_from_server', methods=['POST'])
def test_radarr_from_server():
    radarr_host = request.json['radarr_host']
    radarr_port = request.json['radarr_port']
    radarr_api_key = request.json['radarr_api_key']
    return test_radarr(radarr_host, radarr_port, radarr_api_key)

@bp.route('/settings/test_sonarr_from_server', methods=['POST'])
def test_sonarr_from_server():
    sonarr_host = request.json['sonarr_host']
    sonarr_port = request.json['sonarr_port']
    sonarr_api_key = request.json['sonarr_api_key']
    return test_sonarr(sonarr_host, sonarr_port, sonarr_api_key)