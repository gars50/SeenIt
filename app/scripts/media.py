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

def check_movie_creation(TMDB_id, ombi_id=0, title=""):
    added_to_db = False
    movie = Movie.query.filter_by(TMDB_id=TMDB_id).first()
    if not movie:
        #Get the required info from Radarr
        app_settings = AppSettings.query.first()
        radarr_base_url = "http://"+app_settings.radarr_host+":"+f'{app_settings.radarr_port}'
        radarr_headers = {'X-Api-Key' : app_settings.radarr_api_key}
        radarr_get_movie = requests.get(radarr_base_url+"/api/v3/movie?tmdbid="+str(TMDB_id), headers=radarr_headers)
        radarr_infos = radarr_get_movie.json()
        if radarr_infos:
            #Movie is already in Radarr, process its information
            title = radarr_infos[0]["title"]
            year = radarr_infos[0]["year"]
            radarr_id = radarr_infos[0]["id"]
            total_size = radarr_infos[0]["sizeOnDisk"]
        else:
            #Movie is not in Radarr, have to look up its information
            radarr_id = -1
            total_size = 0
            year = 0
            radarr_lookup = requests.get(radarr_base_url+"/api/v3/movie/lookup/tmdb?tmdbid="+str(TMDB_id), headers=radarr_headers)
            if not radarr_lookup.status_code == 500:
                radarr_infos = radarr_lookup.json()
                title = radarr_infos["title"]
                year = radarr_infos["year"]
        new_movie = Movie(title=title, TMDB_id=TMDB_id, year=year, ombi_id=ombi_id, total_size=total_size, radarr_id=radarr_id)
        db.session.add(new_movie)
        db.session.commit()
        added_to_db = True
    return Movie.query.filter_by(TMDB_id=TMDB_id).first(), added_to_db

def check_tv_show_creation(theTVDB_id, ombi_id=0, title=""):
    added_to_db = False
    show = TVShow.query.filter_by(theTVDB_id=theTVDB_id).first()
    if not show:
        #Get the required info from Sonarr
        app_settings = AppSettings.query.first()
        sonarr_base_url = "http://"+app_settings.sonarr_host+":"+f'{app_settings.sonarr_port}'
        sonarr_headers = {'X-Api-Key' : app_settings.sonarr_api_key}
        sonarr_response = requests.get(sonarr_base_url+"/api/v3/series?tvdbId="+str(theTVDB_id), headers=sonarr_headers)
        sonarr_infos = sonarr_response.json()
        if sonarr_infos:
            #Show is already in Sonarr, process its information
            title = sonarr_infos[0]["title"]
            sonarr_id = sonarr_infos[0]["id"]
            total_size = sonarr_infos[0]["statistics"]["sizeOnDisk"]
        else:
            #Show is not in Sonarr, have to look up its information
            sonarr_id = -1
            total_size = 0
            sonarr_lookup = requests.get(sonarr_base_url+"/api/v3/series/lookup?term=tvdbid:"+str(theTVDB_id), headers=sonarr_headers)
            if not sonarr_lookup.status_code == 500:
                sonarr_infos = sonarr_lookup.json()
                title = sonarr_infos[0]["title"]
            
        new_show = TVShow(title=title, theTVDB_id=theTVDB_id, ombi_id=ombi_id, sonarr_id=sonarr_id, total_size=total_size)
        db.session.add(new_show)
        db.session.commit()
        added_to_db = True
    return TVShow.query.filter_by(theTVDB_id=theTVDB_id).first(), added_to_db

def check_pick_creation(media, user, pick_date, pick_method):
    added_to_db = False
    pick = Pick.query.filter_by(media=media, user=user).first()
    if not pick:
        new_pick = Pick(media=media, user=user, pick_date=pick_date, pick_method=pick_method)
        db.session.add(new_pick)
        media.deletion_date = None
        media.expiry_date = None
        db.session.commit()
        added_to_db = True
    return Pick.query.filter_by(media=media, user=user).first(), added_to_db

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

def import_requests_from_ombi():
    test_services()

    added_users = 0
    added_movies = 0
    added_movie_picks = 0
    added_tv_shows = 0
    added_tv_show_picks = 0

    app_settings = AppSettings.query.first()

    ombi_base_url = "http://"+app_settings.ombi_host+":"+f'{app_settings.ombi_port}'
    ombi_headers = {'ApiKey' : app_settings.ombi_api_key}


    movie_requests_response = requests.get(ombi_base_url+"/api/v1/Request/movie", headers=ombi_headers)
    movie_requests = movie_requests_response.json()

    for movie_request in movie_requests:
        request_date = movie_request["requestedDate"]
        #Weird bug with Ombi where sometimes the requested date is wrong?
        if (request_date == "0001-01-01T00:00:00"):
            request_date_mod = datetime.min
        else:
            request_date_mod = datetime.strptime(request_date.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")

        #If this request was made after the last media import, we import it
        if request_date_mod >= app_settings.last_media_import:
            title = movie_request["title"]
            TMDB_id = movie_request["theMovieDbId"]
            requester_email = movie_request["requestedUser"]["email"]
            requester_alias = movie_request["requestedUser"]["userAlias"]
            ombi_id = movie_request["id"]

            requester, added_user = check_user_creation(requester_email, requester_alias)
            movie, added_movie = check_movie_creation(TMDB_id, ombi_id, title)
            moviePick, added_movie_pick = check_pick_creation(movie, requester, request_date_mod, "Ombi Request")

            if added_user:added_users+=1
            if added_movie:added_movies+=1
            if added_movie_pick:added_movie_picks+=1


    tv_requests_response = requests.get(ombi_base_url+"/api/v1/Request/tv", headers=ombi_headers)
    tv_requests = tv_requests_response.json()

    for tv_request in tv_requests:
        request_date = tv_request["childRequests"][0]["requestedDate"]
        #Weird bug with Ombi where sometimes the requested date is wrong?
        if (request_date == "0001-01-01T00:00:00"):
            request_date_mod = datetime.min
        else:
            request_date_mod = datetime.strptime(request_date.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")

        if request_date_mod >= app_settings.last_media_import:
            title = tv_request["title"]
            theTVDB_id = tv_request["tvDbId"]
            requester_email = tv_request["childRequests"][0]["requestedUser"]["email"]
            requester_alias = tv_request["childRequests"][0]["requestedUser"]["userAlias"]
            ombi_id = tv_request["id"]

            requester, added_user = check_user_creation(requester_email, requester_alias)
            tv_show, added_tv_show = check_tv_show_creation(theTVDB_id, ombi_id, title)
            tv_show_pick, added_tv_show_pick = check_pick_creation(tv_show, requester, request_date_mod, "Ombi Request")

            if added_user:added_users+=1
            if added_tv_show:added_tv_shows+=1
            if added_tv_show_pick:added_tv_show_picks+=1

    response = "Imported \n"+str(added_users)+" Users.\n"+str(added_movies)+" Movies.\n"+str(added_movie_picks)+" Movie Picks.\n"+str(added_tv_shows)+" TV Shows.\n"+str(added_tv_show_picks)+" TV Show Picks"
    app_settings.last_media_import = datetime.utcnow()
    db.session.commit()
    return response

def delete_media_everywhere(media):
    test_services()

    app_settings = AppSettings.query.first()
    radarr_base_url = "http://"+app_settings.radarr_host+":"+f'{app_settings.radarr_port}'
    radarr_headers = {'X-Api-Key' : app_settings.radarr_api_key}

    sonarr_base_url = "http://"+app_settings.sonarr_host+":"+f'{app_settings.sonarr_port}'
    sonarr_headers = {'X-Api-Key' : app_settings.sonarr_api_key}

    ombi_base_url = "http://"+app_settings.ombi_host+":"+f'{app_settings.ombi_port}'
    ombi_headers = {'ApiKey' : app_settings.ombi_api_key}

    if media.type == "movie":
        requests.delete(ombi_base_url+"/api/v1/Request/movie/"+str(media.ombi_id), headers=ombi_headers)
        requests.delete(radarr_base_url+"/api/v3/movie/"+str(media.radarr_id)+"?deleteFiles=true", headers=radarr_headers)
        message = "Deleted"+media.title+"from Radarr and Ombi"
    else:
        requests.delete(ombi_base_url+"/api/v1/Request/tv/"+str(media.ombi_id), headers=ombi_headers)
        requests.delete(sonarr_base_url+"/api/v3/series/"+str(media.sonarr_id)+"?deleteFiles=true", headers=sonarr_headers)
        message = "Deleted"+media.title+"from Sonarr and Ombi"
    db.session.delete(media)
    db.session.commit()
    return message

def update_media_infos():
    all_movies = Movie.query.all()
    app_settings = AppSettings.query.first()
    radarr_base_url = "http://"+app_settings.radarr_host+":"+f'{app_settings.radarr_port}'
    radarr_headers = {'X-Api-Key' : app_settings.radarr_api_key}
    sonarr_base_url = "http://"+app_settings.sonarr_host+":"+f'{app_settings.sonarr_port}'
    sonarr_headers = {'X-Api-Key' : app_settings.sonarr_api_key}

    all_movies = Movie.query.all()
    for movie in all_movies:
        print("Updating "+str(movie))
        radarr_get_movie = requests.get(radarr_base_url+"/api/v3/movie?tmdbid="+str(movie.TMDB_id), headers=radarr_headers)
        radarr_infos = radarr_get_movie.json()
        if radarr_infos:
            movie.radarr_id = radarr_infos[0]["id"]
            movie.total_size = radarr_infos[0]["sizeOnDisk"]
            db.session.commit()

    all_shows = TVShow.query.all()
    for show in all_shows:
        print("Updating "+str(show))
        sonarr_response = requests.get(sonarr_base_url+"/api/v3/series?tvdbId="+str(show.theTVDB_id), headers=sonarr_headers)
        sonarr_infos = sonarr_response.json()
        if sonarr_infos:
            show.sonarr_id = sonarr_infos[0]["id"]
            show.total_size = sonarr_infos[0]["statistics"]["sizeOnDisk"]
            db.session.commit()