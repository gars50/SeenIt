from app import scheduler
from app.scripts.media import import_requests_from_ombi, update_media_infos

def update_medias_and_requests():
    print("Running an update on the database")
    with scheduler.app.app_context():
        #Import new requests from Ombi
        import_requests_from_ombi()
        #Update media infos from Sonarr/Radarr
        update_media_infos()
    print("Job done")
    #Maybe import Medias from Sonarr/Radarr?