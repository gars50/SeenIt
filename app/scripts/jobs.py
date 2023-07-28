from app import scheduler
from app.scripts.media import import_requests_from_ombi, update_media_infos

def update_medias_and_requests():
    with scheduler.app.app_context():
        scheduler.app.logger.info("Job Update on all medias started.")
        scheduler.app.logger.debug("Importing new requests from Ombi.")
        import_requests_from_ombi()
        scheduler.app.logger.debug("Updating media info from Sonarr/Radarr.")
        update_media_infos()
        scheduler.app.logger.info("Job completed.")
    #Maybe import Medias from Sonarr/Radarr?