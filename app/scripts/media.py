import requests
from datetime import datetime
from app.models import User, Movie, TVShow, AppSettings, Pick
from app import db

def check_user_creation(email, alias):
    addedToDB= False
    user = User.query.filter_by(email=email).first()
    if not user:
        newUser = User(email=email, alias=alias)
        db.session.add(newUser)
        db.session.commit()
        addedToDB= True
    return User.query.filter_by(email=email).first(), addedToDB

def check_movie_creation(title, theMovieDbID, theMovieDbURL, releaseDateMod, ombiID):
    addedToDB= False
    movie = Movie.query.filter_by(theMovieDbID=theMovieDbID).first()
    if not movie:
        newMovieRequest = Movie(title=title, theMovieDbID=theMovieDbID, theMovieDbURL=theMovieDbURL, releaseDate=releaseDateMod, ombiID=ombiID)
        db.session.add(newMovieRequest)
        db.session.commit()
        addedToDB= True
    return Movie.query.filter_by(theMovieDbID=theMovieDbID).first(), addedToDB

def check_tvShow_creation(title, tvDbID, tvDbURL, ombiID):
    addedToDB= False
    show = TVShow.query.filter_by(tvDbID=tvDbID).first()
    if not show:
        newShow = TVShow(title=title, tvDbID=tvDbID, tvDbURL=tvDbURL, ombiID=ombiID)
        db.session.add(newShow)
        db.session.commit()
        addedToDB= True
    return TVShow.query.filter_by(tvDbID=tvDbID).first(), addedToDB


def check_pick_creation(media, requester, pickDate, pickMethod):
    addedToDB= False
    pick = Pick.query.filter_by(media=media, user=requester).first()
    if not pick:
        new_pick = Pick(media=media, user=requester, pick_date=pickDate, pick_method=pickMethod)
        db.session.add(new_pick)
        db.session.commit()
        addedToDB= True
    return Pick.query.filter_by(media=media, user=requester).first(), addedToDB

def test_services():
    appSettings = AppSettings.query.first()

    radarrBaseURL = "http://"+appSettings.radarrHost+":"+f'{appSettings.radarrPort}'
    radarrHeaders = {'X-Api-Key' : appSettings.radarrApiKey}

    sonarrBaseURL = "http://"+appSettings.sonarrHost+":"+f'{appSettings.sonarrPort}'
    sonarrHeaders = {'X-Api-Key' : appSettings.sonarrApiKey}

    ombiBaseUrl = "http://"+appSettings.ombiHost+":"+f'{appSettings.ombiPort}'
    ombiHeaders = {'ApiKey' : appSettings.ombiApiKey}
    try:
        requests.get(radarrBaseURL+"/api/v3/system/status", headers=radarrHeaders)
        requests.get(sonarrBaseURL+"/api/v3/system/status", headers=sonarrHeaders)
        requests.get(ombiBaseUrl+"/api/v1/Status", headers=ombiHeaders)
    except Exception as err:
        raise Exception(str(err))


def import_all_requests():
    test_services()

    addedUsers = 0
    addedMovies = 0
    addedMoviePicks = 0
    addedTVShows = 0
    addedTVShowPicks = 0

    appSettings = AppSettings.query.first()
    ombiBaseURL = "http://"+appSettings.ombiHost+":"+f'{appSettings.ombiPort}'
    headers = {'ApiKey' : appSettings.ombiApiKey}


    movieRequestsResponse = requests.get(ombiBaseURL+"/api/v1/Request/movie", headers=headers)
    movieRequests = movieRequestsResponse.json()

    for movieRequest in movieRequests:
        title = movieRequest["title"]
        theMovieDbID = movieRequest["theMovieDbId"]
        theMovieDbURL = "https://www.themoviedb.org/movie/"+str(theMovieDbID)
        releaseDate = movieRequest["releaseDate"]
        requesterEmail = movieRequest["requestedUser"]["email"]
        requesterAlias = movieRequest["requestedUser"]["userAlias"]
        ombiID = movieRequest["id"]
        pickDate = movieRequest["requestedDate"]

        releaseDateMod = datetime.strptime(releaseDate.replace("T", " "), "%Y-%m-%d %H:%M:%S")
        #Weird bug with Ombi where sometimes the date is wrong?
        if (pickDate == "0001-01-01T00:00:00"):
            pickDateMod = datetime.min
        else:
            pickDateMod = datetime.strptime(pickDate.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")

        requester, addedUser = check_user_creation(requesterEmail, requesterAlias)
        movie, addedMovie = check_movie_creation(title, theMovieDbID, theMovieDbURL, releaseDateMod, ombiID)
        moviePick, addedMoviePick = check_pick_creation(movie, requester, pickDateMod, "Ombi Request")

        if addedUser:addedUsers+=1
        if addedMovie:addedMovies+=1
        if addedMoviePick:addedMoviePicks+=1


    TVRequestsResponse = requests.get(ombiBaseURL+"/api/v1/Request/tv", headers=headers)
    TVRequests = TVRequestsResponse.json()

    for TVRequest in TVRequests:
        title = TVRequest["title"]
        tvDbID = TVRequest["tvDbId"]
        tvDbURL = "https://www.thetvdb.com/?id="+str(tvDbID)+"&tab=series"

        requesterEmail = TVRequest["childRequests"][0]["requestedUser"]["email"]
        requesterAlias = TVRequest["childRequests"][0]["requestedUser"]["userAlias"]
        ombiID = TVRequest["id"]
        pickDate = TVRequest["childRequests"][0]["requestedDate"]

        pickDateMod = datetime.strptime(pickDate.replace("T", " "), "%Y-%m-%d %H:%M:%S.%f")

        requester, addedUser = check_user_creation(requesterEmail, requesterAlias)
        tvShow, addedTVShow = check_tvShow_creation(title, tvDbID, tvDbURL, ombiID)
        tvShowPick, addedTVShowPick = check_pick_creation(tvShow, requester, pickDateMod, "Ombi Request")

        if addedUser:addedUsers+=1
        if addedTVShow:addedTVShows+=1
        if addedTVShowPick:addedTVShowPicks+=1

    response = "Imported \n"+str(addedUsers)+" Users.\n"+str(addedTVShows)+" TV Shows.\n"+str(addedMovies)+" Movies.\n"+str(addedMoviePicks)+" Movie Picks.\n"+str(addedTVShowPicks)+" TV Show Picks"
    return response