from app import scheduler
from app.scripts.media import import_requests_from_ombi, import_movies_from_radarr, import_shows_from_sonarr, update_media_infos, update_free_space_info, delete_expired_medias, update_user_storage_usage

def update_medias_and_requests():
    with scheduler.app.app_context():
        scheduler.app.logger.info("Importing new requests from Ombi.")
        import_requests_from_ombi()
        scheduler.app.logger.info("Importing new movies from Radarr.")
        import_movies_from_radarr()
        scheduler.app.logger.info("Importing new shows from Sonarr.")
        import_shows_from_sonarr()
        scheduler.app.logger.info("Updating media info from Sonarr/Radarr.")
        update_media_infos()
        scheduler.app.logger.info("Updating free space available.")
        update_free_space_info()
        scheduler.app.logger.info("Updating storage per user.")
        update_user_storage_usage()

def delete_all_expired_medias():
    with scheduler.app.app_context():
        scheduler.app.logger.info("Deleting all expired medias.")
        delete_expired_medias()