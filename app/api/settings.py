from app.api import bp
from flask import request
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