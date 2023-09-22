import requests
from flask import current_app
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.models import User, Movie, TVShow, AppSettings, Pick, Media
from app.extensions import cache_session
from app import db

def api_ombi(method, url_end):
    app_settings = AppSettings.query.first()
    ombi_base_url = "http://"+app_settings.ombi_host+":"+f'{app_settings.ombi_port}'
    ombi_headers = {'ApiKey' : app_settings.ombi_api_key}
    return cache_session.request(method,ombi_base_url+url_end, headers=ombi_headers)

def api_radarr(method, url_end):
    app_settings = AppSettings.query.first()
    radarr_base_url = "http://"+app_settings.radarr_host+":"+f'{app_settings.radarr_port}'
    radarr_headers = {'X-Api-Key' : app_settings.radarr_api_key}
    return cache_session.request(method,radarr_base_url+url_end, headers=radarr_headers)

def api_sonarr(method, url_end):
    app_settings = AppSettings.query.first()
    sonarr_base_url = "http://"+app_settings.sonarr_host+":"+f'{app_settings.sonarr_port}'
    sonarr_headers = {'X-Api-Key' : app_settings.sonarr_api_key}
    return cache_session.request(method, sonarr_base_url+url_end, headers=sonarr_headers)

def check_user_creation(email, alias):
    added_to_db = False
    current_app.logger.debug("Checking if user "+email+" exists")
    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(email=email, alias=alias)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info("Created user "+str(new_user))
        added_to_db = True
    return User.query.filter_by(email=email).first(), added_to_db

def check_movie_creation(TMDB_id, ombi_id=0, title=""):
    added_to_db = False
    current_app.logger.debug("Checking if movie "+str(TMDB_id)+" exists")
    movie = Movie.query.filter_by(TMDB_id=TMDB_id).first()
    if not movie:
        current_app.logger.debug("It does not. Creating it.")
        #Get the required info from Radarr
        radarr_get_movie = api_radarr("GET", "/api/v3/movie?tmdbid="+str(TMDB_id))
        radarr_infos = radarr_get_movie.json()
        if radarr_infos:
            current_app.logger.debug("Movie is already in Radarr, processing its information")
            title = radarr_infos[0]["title"]
            year = radarr_infos[0]["year"]
            radarr_id = radarr_infos[0]["id"]
            poster_url = None
            total_size = radarr_infos[0]["sizeOnDisk"]
            for image in radarr_infos[0]["images"]:
                if image["coverType"] == "poster":
                    poster_url = image["remoteUrl"]
        else:
            current_app.logger.debug("Movie is not in Radarr, have to look up its information")
            radarr_id = -1
            total_size = 0
            year = 0
            radarr_lookup = api_radarr("GET","/api/v3/movie/lookup/tmdb?tmdbid="+str(TMDB_id))
            if radarr_lookup.status_code == 500:
                year = 0
                poster_url = None
            else:
                radarr_infos = radarr_lookup.json()
                title = radarr_infos["title"]
                year = radarr_infos["year"]
                poster_url = None
                for image in radarr_infos["images"]:
                    if image["coverType"] == "poster":
                        poster_url = image["url"]

        new_movie = Movie(title=title, TMDB_id=TMDB_id, year=year, ombi_id=ombi_id, total_size=total_size, radarr_id=radarr_id, poster_url=poster_url)
        db.session.add(new_movie)
        db.session.commit()
        current_app.logger.info("Created "+str(new_movie))
        added_to_db = True
    return Movie.query.filter_by(TMDB_id=TMDB_id).first(), added_to_db

def check_tv_show_creation(theTVDB_id, ombi_id=0, title=""):
    added_to_db = False
    current_app.logger.debug("Checking if tv show "+str(theTVDB_id)+" exists")
    show = TVShow.query.filter_by(theTVDB_id=theTVDB_id).first()
    if not show:
        sonarr_response = api_sonarr("GET","/api/v3/series?tvdbId="+str(theTVDB_id))
        sonarr_infos = sonarr_response.json()
        if sonarr_infos:
            current_app.logger.debug("Show is already in Sonarr, process its information")
            title = sonarr_infos[0]["title"]
            sonarr_id = sonarr_infos[0]["id"]
            total_size = sonarr_infos[0]["statistics"]["sizeOnDisk"]
            poster_url = None
            for image in sonarr_infos[0]["images"]:
                if image["coverType"] == "poster":
                    poster_url = image["remoteUrl"]
        else:
            current_app.logger.debug("Show is not in Sonarr, have to look up its information")
            sonarr_id = -1
            total_size = 0
            sonarr_lookup = api_sonarr("GET","/api/v3/series/lookup?term=tvdbid:"+str(theTVDB_id))
            if sonarr_lookup.status_code == 500:
                poster_url = None
            else:
                sonarr_infos = sonarr_lookup.json()
                title = sonarr_infos[0]["title"]
                poster_url = None
                for image in sonarr_infos[0]["images"]:
                    if image["coverType"] == "poster":
                        poster_url = image["remoteUrl"]
                
        new_show = TVShow(title=title, theTVDB_id=theTVDB_id, ombi_id=ombi_id, sonarr_id=sonarr_id, total_size=total_size, poster_url=poster_url)
        db.session.add(new_show)
        db.session.commit()
        current_app.logger.info("Created "+str(new_show))
        added_to_db = True
    return TVShow.query.filter_by(theTVDB_id=theTVDB_id).first(), added_to_db

def check_pick_creation(media, user, pick_date, pick_method):
    added_to_db = False
    current_app.logger.debug("Checking if pick for "+str(media)+" by "+str(user)+" exists")
    pick = Pick.query.filter_by(media=media, user=user).first()
    if not pick:
        new_pick = Pick(media=media, user=user, pick_date=pick_date, pick_method=pick_method)
        db.session.add(new_pick)
        media.deletion_date = None
        media.expiry_date = None
        media.abandonned_date = None
        db.session.commit()
        current_app.logger.info("Created "+str(new_pick))
        added_to_db = True
    return Pick.query.filter_by(media=media, user=user).first(), added_to_db

def test_ombi(ombi_host, ombi_port, ombi_api_key):
    ombi_base_url = "http://"+ombi_host+":"+f'{ombi_port}'
    ombi_headers = {'ApiKey' : ombi_api_key, 'Cache-Control': 'no-cache'}

    try:
        response = requests.get(ombi_base_url+"/api/v1/Status", headers=ombi_headers)
    except Exception as err:
        raise Exception(str(err))
    else:
        if response:
            current_app.logger.debug("Test to Ombi successful.")
            return {
                "message" : "Test to Ombi successful"
            } 
        else:
            return {
                "error" : "Could not connect to Ombi"
            }, 500

def test_radarr(radarr_host, radarr_port, radarr_api_key):
    radarr_base_url = "http://"+radarr_host+":"+f'{radarr_port}'
    radarr_headers = {'X-Api-Key' : radarr_api_key, 'Cache-Control': 'no-cache'}
    try:
        response = requests.get(radarr_base_url+"/api/v3/System/Status", headers=radarr_headers)
    except Exception as err:
        raise Exception(str(err))
    else:
        if response:
            current_app.logger.debug("Test to Radarr successful.")
            return {
                "message" : "Test to Radarr successful"
            } 
        else:
            return {
                "error" : "Could not connect to Radarr"
            }, 500

def test_sonarr(sonarr_host, sonarr_port, sonarr_api_key):
    sonarr_base_url = "http://"+sonarr_host+":"+f'{sonarr_port}'
    sonarr_headers = {'X-Api-Key' : sonarr_api_key, 'Cache-Control': 'no-cache'}

    try:
        response = requests.get(sonarr_base_url+"/api/v3/System/Status", headers=sonarr_headers)
    except Exception as err:
        raise Exception(str(err))
    else:
        if response:
            current_app.logger.debug("Test to Sonarr successful.")
            return {
                "message" : "Test to Sonarr successful"
            } 
        else:
            return {
                "error" : "Could not connect to Sonarr"
            }, 500

def test_services():
    app_settings = AppSettings.query.first()

    test_ombi(app_settings.ombi_host, app_settings.ombi_port, app_settings.ombi_api_key)
    test_radarr(app_settings.radarr_host, app_settings.radarr_port, app_settings.radarr_api_key)
    test_sonarr(app_settings.sonarr_host, app_settings.sonarr_port, app_settings.sonarr_api_key)

def import_requests_from_ombi():
    test_services()

    added_users = 0
    added_movies = 0
    added_movie_picks = 0
    added_tv_shows = 0
    added_tv_show_picks = 0

    app_settings = AppSettings.query.first()
    start_time = datetime.utcnow()

    movie_requests_response = api_ombi("GET","/api/v1/Request/movie")
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

            current_app.logger.debug("Processing movie "+title+", requested by "+requester_email)

            requester, added_user = check_user_creation(requester_email, requester_alias)
            movie, added_movie = check_movie_creation(TMDB_id, ombi_id, title)
            moviePick, added_movie_pick = check_pick_creation(movie, requester, request_date_mod, "Ombi Request")

            if added_user:added_users+=1
            if added_movie:added_movies+=1
            if added_movie_pick:added_movie_picks+=1


    tv_requests_response = api_ombi("GET","/api/v1/Request/tv")
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
    app_settings.last_media_import = start_time
    db.session.commit()
    return response

def import_movies_from_radarr():
    radarr_response = api_radarr("GET", "/api/v3/movie")
    radarr_infos = radarr_response.json()
    for movie in radarr_infos:
        movie, added_to_db = check_movie_creation(movie["tmdbId"])
        if (added_to_db):
            permanent_user = User.query.filter_by(email="permanent").first()
            check_pick_creation(movie, permanent_user, datetime.utcnow(), "Added from Radarr")

def import_shows_from_sonarr():
    sonarr_response = api_sonarr("GET", "/api/v3/series")
    sonarr_infos = sonarr_response.json()
    for show in sonarr_infos:
        tv_show, added_to_db = check_tv_show_creation(show["tvdbId"])
        if (added_to_db):
            permanent_user = User.query.filter_by(email="permanent").first()
            check_pick_creation(tv_show, permanent_user, datetime.utcnow(), "Added from Sonarr")

def delete_media_from_ombi(media):
    if media.type == "movie":
        api_ombi("DELETE","/api/v1/Request/movie/"+str(media.ombi_id))
    else:
        api_ombi("DELETE","/api/v1/Request/tv/"+str(media.ombi_id))
    current_app.logger.info(str(media)+" deleted from Ombi.")

def delete_media_from_radarr(media):
    api_radarr("DELETE", "/api/v3/movie/"+str(media.radarr_id)+"?deleteFiles=true")
    current_app.logger.info(str(media)+" deleted from Radarr.")

def delete_media_from_sonarr(media):
    api_sonarr("DELETE", "/api/v3/series/"+str(media.sonarr_id)+"?deleteFiles=true")
    current_app.logger.info(str(media)+" deleted from Sonarr.")

def delete_media_from_media_manager(media):
    if media.type == "movie":
        delete_media_from_radarr(media)
    elif media.type == "tv_show":
        delete_media_from_sonarr(media)

def delete_media_everywhere(media):
    test_services()

    app_settings = AppSettings.query.first()

    if app_settings.safe_mode:
        message = "Deleted "+media.title+" from the database only."
        current_app.logger.info(str(media)+" deleted from the database only.")
    else:
        delete_media_from_ombi(media)
        delete_media_from_media_manager(media)
        message = "Deleted "+media.title+" everywhere."
    db.session.delete(media)
    db.session.commit()
    return message

def update_media_infos():

    current_app.logger.debug("Updating movie infos from Radarr.")
    radarr_response = api_radarr("GET", "/api/v3/movie")
    radarr_infos = radarr_response.json()
    for radarr_movie in radarr_infos:
        seenit_movie = Movie.query.filter_by(TMDB_id=str(radarr_movie["tmdbId"])).one()
        if seenit_movie:
            current_app.logger.debug("Processing movie " + seenit_movie.title + " from Radarr.")
            seenit_movie.radarr_id = radarr_movie["id"]
            seenit_movie.total_size = radarr_movie["sizeOnDisk"]
            for image in radarr_movie["images"]:
                if image["coverType"] == "poster":
                    seenit_movie.poster_url = image["remoteUrl"]
            db.session.commit()

    current_app.logger.debug("Updating show infos from Sonarr.")
    sonarr_response = api_sonarr("GET", "/api/v3/series")
    sonarr_infos = sonarr_response.json()
    for sonarr_show in sonarr_infos:        
        seenit_show = TVShow.query.filter_by(theTVDB_id=sonarr_show["tvdbId"]).one()
        if seenit_show:
            current_app.logger.debug("Processing show " + seenit_show.title + " from Sonarr.")
            seenit_show.radarr_id = sonarr_show["id"]
            seenit_show.total_size = sonarr_show["statistics"]["sizeOnDisk"]
            for image in sonarr_show["images"]:
                if image["coverType"] == "poster":
                    seenit_show.poster_url = image["remoteUrl"]
            db.session.commit()

def modify_deletion_date(medias):
    app_settings = AppSettings.query.first()
    for media in medias:
        current_app.logger.debug("Changing "+str(media))
        media.expiry_date = media.abandonned_date + relativedelta(**{app_settings.expiry_time_unit: app_settings.expiry_time_number})
        current_app.logger.debug("Expiry date of "+str(media)+" set to "+str(media.expiry_date))
        delete_time = app_settings.next_delete
        if (delete_time < media.expiry_date):
            #Find the next deletion date that lands after the expiration date
            deletion_delta = relativedelta(**{app_settings.deletion_time_unit: app_settings.deletion_time_number})
            while delete_time < media.expiry_date:
                delete_time += deletion_delta
            #There should be a faster way to calculate this, but I do not know it
            #It shouldn't have a big impact anyway.
            #This method does not work because division of relativedelta is not doable.
            #deltaMulti = math.ceil(relativedelta(media.expiryDate, delete_time)/deletion_delta)
            #delete_time = deltaMulti * deletion_delta
        media.deletion_date = delete_time
        db.session.commit()
        current_app.logger.debug("Deletion date of "+str(media)+" set to "+str(media.deletion_date))

def check_if_abandonned(media, user=None):
    abandonned = (not media.picks)
    #If this was the last pick that was just deleted, we need to set the expiryDate and deletionDate
    if abandonned:
        media.abandonned_date = datetime.utcnow()
        modify_deletion_date([media])
        current_app.logger.info(str(media)+" has been abandonned.")
        media.last_user = user
        db.session.commit()
    return abandonned

def update_free_space_info():
    #Get disk space remaining from Radarr with a movie
    #Need to change this for deployment, but it will do for now.
    app_settings = AppSettings.query.first()
    
    radarr_response = api_radarr("GET", "/api/v3/movie")
    radarr_infos = radarr_response.json()
    root_drive = radarr_infos[0]["rootFolderPath"][0:3]
    
    radarr_response = api_radarr("GET", "/api/v3/diskspace")
    radarr_infos = radarr_response.json()
    for drive in radarr_infos:
        if (drive["path"]==root_drive):
            fixed_free_space = drive["freeSpace"]/1024**3*1000**3
            app_settings.free_space = fixed_free_space
            db.session.commit()
            current_app.logger.debug("Free space is now "+ str(app_settings.free_space))

def update_user_storage_usage():
    for user in User.query.all():
        current_app.logger.debug("Updating storage for "+ str(user))

        total_user_movie_size = 0
        movie_picks = Pick.query.filter_by(user=user, media_type="movie")
        for movie_pick in movie_picks:
            total_user_movie_size += movie_pick.media.total_size
        user.movie_storage_usage = total_user_movie_size

        total_user_tv_show_size = 0
        tv_show_picks = Pick.query.filter_by(user=user, media_type="tv_show")
        for tv_show_pick in tv_show_picks:
            total_user_tv_show_size += tv_show_pick.media.total_size
        user.show_storage_usage = total_user_tv_show_size
        db.session.commit()

def delete_expired_medias():
    medias_to_delete = Media.query.filter(Media.deletion_date < datetime.utcnow()).all()
    for media in medias_to_delete:
        delete_media_everywhere(media)

def delete_pick_and_check_abandonned(pick):
    media = pick.media
    user = pick.user
    if pick.pick_method == "Ombi Request":
        #Should we delete the ombi request at this point and avoid double data in the db?
        current_app.logger.debug("Deleting Ombi Request for "+str(pick.media))
    db.session.delete(pick)
    db.session.commit()
    abandonned = check_if_abandonned(media, user)
    return abandonned