import requests
from datetime import datetime
from app.models import User, Movie, TVShow, AppSettings, Pick
from app import db

def check_user_creation(email, alias):
    added_to_db = False
    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(email=email, alias=alias)
        db.session.add(new_user)
        db.session.commit()
        added_to_db = True
    return User.query.filter_by(email=email).first(), added_to_db

def check_movie_creation(title, TMDB_id, TMDB_url, release_date, ombi_id):
    added_to_db= False
    movie = Movie.query.filter_by(TMDB_id=TMDB_id).first()
    if not movie:
        new_movie_request = Movie(title=title, TMDB_id=TMDB_id, TMDB_url=TMDB_url, release_date=release_date, ombi_id=ombi_id)
        db.session.add(new_movie_request)
        db.session.commit()
        added_to_db= True
    return Movie.query.filter_by(TMDB_id=TMDB_id).first(), added_to_db

def check_tvShow_creation(title, theTVDB_id, theTVDB_url, ombi_id):
    added_to_db = False
    show = TVShow.query.filter_by(theTVDB_id=theTVDB_id).first()
    if not show:
        new_show = TVShow(title=title, theTVDB_id=theTVDB_id, theTVDB_url=theTVDB_url, ombi_id=ombi_id)
        db.session.add(new_show)
        db.session.commit()
        added_to_db = True
    return TVShow.query.filter_by(theTVDB_id=theTVDB_id).first(), added_to_db

def check_pick_creation(media, requester, pick_date, pick_method):
    added_to_db= False
    pick = Pick.query.filter_by(media=media, user=requester).first()
    if not pick:
        new_pick = Pick(media=media, user=requester, pick_date=pick_date, pick_method=pick_method)
        db.session.add(new_pick)
        media.deletion_date = None
        media.expiry_date = None
        db.session.commit()
        added_to_db= True
    return Pick.query.filter_by(media=media, user=requester).first(), added_to_db

def test_services():
    app_settings = AppSettings.query.first()

    radarr_base_url = "http://"+app_settings.radarr_host+":"+f'{app_settings.radarr_port}'
    radarr_headers = {'X-Api-Key' : app_settings.radarr_api_key}

    sonarr_base_url = "http://"+app_settings.sonarr_host+":"+f'{app_settings.sonarr_port}'
    sonarr_headers = {'X-Api-Key' : app_settings.sonarr_api_key}

    ombi_base_url = "http://"+app_settings.ombi_host+":"+f'{app_settings.ombi_port}'
    ombi_headers = {'ApiKey' : app_settings.ombi_api_key}

    try:
        requests.get(radarr_base_url+"/api/v3/system/status", headers=radarr_headers)
        requests.get(sonarr_base_url+"/api/v3/system/status", headers=sonarr_headers)
        requests.get(ombi_base_url+"/api/v1/Status", headers=ombi_headers)
    except Exception as err:
        raise Exception(str(err))


def import_all_requests():
    test_services()

    added_users = 0
    added_movies = 0
    added_movie_picks = 0
    added_tv_shows = 0
    added_tv_show_picks = 0

    app_settings = AppSettings.query.first()
    radarr_base_url = "http://"+app_settings.radarr_host+":"+f'{app_settings.radarr_port}'
    radarr_headers = {'X-Api-Key' : app_settings.radarr_api_key}

    sonarr_base_url = "http://"+app_settings.sonarr_host+":"+f'{app_settings.sonarr_port}'
    sonarr_headers = {'X-Api-Key' : app_settings.sonarr_api_key}

    ombi_base_url = "http://"+app_settings.ombi_host+":"+f'{app_settings.ombi_port}'
    ombi_headers = {'ApiKey' : app_settings.ombi_api_key}


    movie_requests_response = requests.get(ombi_base_url+"/api/v1/Request/movie", headers=ombi_headers)
    movie_requests = movie_requests_response.json()

    for movie_request in movie_requests:
        title = movie_request["title"]
        TMDB_id = movie_request["theMovieDbId"]
        TMDB_url = "https://www.themoviedb.org/movie/"+str(TMDB_id)
        release_date = movie_request["releaseDate"]
        requester_email = movie_request["requestedUser"]["email"]
        requester_alias = movie_request["requestedUser"]["userAlias"]
        ombi_id = movie_request["id"]
        pick_date = movie_request["requestedDate"]

        release_date_mod = datetime.strptime(release_date.replace("T", " "), "%Y-%m-%d %H:%M:%S")
        #Weird bug with Ombi where sometimes the date is wrong?
        if (pick_date == "0001-01-01T00:00:00"):
            pick_date_mod = datetime.min
        else:
            pick_date_mod = datetime.strptime(pick_date.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")

        requester, added_user = check_user_creation(requester_email, requester_alias)
        movie, added_movie = check_movie_creation(title, TMDB_id, TMDB_url, release_date_mod, ombi_id)
        moviePick, added_movie_pick = check_pick_creation(movie, requester, pick_date_mod, "Ombi Request")

        if added_user:added_users+=1
        if added_movie:added_movies+=1
        if added_movie_pick:added_movie_picks+=1


    tv_requests_response = requests.get(ombi_base_url+"/api/v1/Request/tv", headers=ombi_headers)
    tv_requests = tv_requests_response.json()

    for tv_request in tv_requests:
        title = tv_request["title"]
        theTVDB_id = tv_request["tvDbId"]
        theTVDB_url = "https://www.thetvdb.com/?id="+str(theTVDB_id)+"&tab=series"

        requester_email = tv_request["childRequests"][0]["requestedUser"]["email"]
        requester_alias = tv_request["childRequests"][0]["requestedUser"]["userAlias"]
        ombi_id = tv_request["id"]
        pick_date = tv_request["childRequests"][0]["requestedDate"]

        pick_date_mod = datetime.strptime(pick_date.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")

        requester, added_user = check_user_creation(requester_email, requester_alias)
        tvShow, added_tv_show = check_tvShow_creation(title, theTVDB_id, theTVDB_url, ombi_id)
        tvShowPick, added_tv_show_pick = check_pick_creation(tvShow, requester, pick_date_mod, "Ombi Request")

        if added_user:added_users+=1
        if added_tv_show:added_tv_shows+=1
        if added_tv_show_pick:added_tv_show_picks+=1

    response = "Imported \n"+str(added_users)+" Users.\n"+str(added_movies)+" Movies.\n"+str(added_movie_picks)+" Movie Picks.\n"+str(added_tv_shows)+" TV Shows.\n"+str(added_tv_show_picks)+" TV Show Picks"
    return response

def import_requests_delta():
    test_services()

def delete_media_everywhere(media):
    test_services()