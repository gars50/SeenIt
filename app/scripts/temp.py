from app.models import User, Media, AppSettings
from app.extensions import cache_session
from app import db

def import_requests_original():
    abandonned_medias = Media.query.filter_by(picks=None)
    app_settings = AppSettings.query.first()
    ombi_base_url = "http://"+app_settings.ombi_host+":"+f'{app_settings.ombi_port}'
    ombi_headers = {'ApiKey' : app_settings.ombi_api_key}

    tv_requests_response = cache_session.request("GET",ombi_base_url+"/api/v1/Request/tv", headers=ombi_headers)
    tv_requests = tv_requests_response.json()

    for media in abandonned_medias:
        print("test")
        if media.type == "movie":
            movie_info_request_response = cache_session.request("GET",ombi_base_url+"/api/v1/Request/movie/info/"+str(media.ombi_id), headers=ombi_headers)
            movie_info = movie_info_request_response.json()
            requester_email = movie_info["requestedUser"]["email"]
            requester = User.query.filter_by(email=requester_email).first()
            media.last_user = requester

        elif media.type =="tv_show":
            for tv_request in tv_requests:
                if media.theTVDB_id == tv_request["tvDbId"]:
                    requester_email = tv_request["childRequests"][0]["requestedUser"]["email"]
                    requester = User.query.filter_by(email=requester_email).first()
                    media.last_user = requester
    db.session.commit()