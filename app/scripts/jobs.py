from app import scheduler
from app.scripts.media import import_requests_from_ombi, update_media_infos

def update_medias_and_requests():
    with scheduler.app.app_context():
        scheduler.app.logger.info("Running an update on all medias.")
        #Import new requests from Ombi
        import_requests_from_ombi()
        #Update media infos from Sonarr/Radarr
        update_media_infos()
        scheduler.app.logger.info("Update completed.")
    #Maybe import Medias from Sonarr/Radarr?