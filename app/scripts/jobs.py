from app import scheduler
from flask import current_app
from app.scripts.media import import_requests_from_ombi, update_media_infos

def update_medias_and_requests():
    current_app.logger.info("Running an update on all medias.")
    with scheduler.app.app_context():
        #Import new requests from Ombi
        import_requests_from_ombi()
        #Update media infos from Sonarr/Radarr
        update_media_infos()
    current_app.logger.info("Update completed.")
    #Maybe import Medias from Sonarr/Radarr?