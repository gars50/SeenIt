import requests, datetime
from app.models import User, Movie, TVShow, TVShowSeason, AppSettings, MoviePick, TVShowSeasonPick
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

def check_moviePick_creation(movie, requester, pickDate):
    addedToDB= False
    moviePick = MoviePick.query.filter_by(movie=movie, owner=requester)
    if not moviePick:
        newMoviePick = MoviePick(movie=movie, owner=requester, pick_date=pickDate)
        db.session.add(newMoviePick)
        db.session.commit()
        addedToDB= True
    return MoviePick.query.filter_by(movie_id=movie.id, owner_id=requester.id), addedToDB

def check_tvShow_creation(title, tvDbID, tvDbURL, ombiID):
    addedToDB= False
    show = TVShow.query.filter_by(tvDbID=tvDbID).first()
    if not show:
        newTVRequest = TVShow(title=title, tvDbID=tvDbID, tvDbURL=tvDbURL, ombiID=ombiID)
        db.session.add(newTVRequest)
        db.session.commit()
        addedToDB= True
    return TVShow.query.filter_by(tvDbID=tvDbID).first(), addedToDB

def check_tvShowSeason_creation(tvShow, seasonNumber, ombiID):
    addedToDB = False
    season = TVShowSeason.query.filter_by(tvShow=tvShow, seasonNumber=seasonNumber, ombiID=ombiID)
    if not season:
        newSeason = TVShowSeason(tvShow=tvShow, seasonNumber=seasonNumber, ombiID=ombiID)
        db.session.add(newSeason)
        db.session.commit()
        addedToDB = True
    return TVShowSeason.query.filter_by(tvShow=tvShow), addedToDB

def check_tvShowSeasonPick_creation(tvShow, seasonNumber, requester, pickDate):
    addedToDB= False
    seasonPick = TVShowSeasonPick.query.filter_by(tvShow=tvShow, seasonNumber=seasonNumber, owner=requester).first()
    if not seasonPick:
        newSeasonPick = TVShowSeasonPick(tvShow=tvShow, seasonNumber=seasonNumber, owner=requester, pick_date=pickDate)
        db.session.add(newSeasonPick)
        db.session.commit()
        addedToDB= True
    return TVShowSeasonPick.query.filter_by(tvShow=tvShow, seasonNumber=seasonNumber, owner=requester).first(), addedToDB

def test_services():
    appSettings = AppSettings.query.first()

    radarrBaseURL = "http://"+appSettings.radarrHost+":"+f'{appSettings.radarrPort}'
    radarrHeaders = {'X-Api-Key' : appSettings.radarrApiKey}

    sonarrBaseURL = "http://"+appSettings.sonarrHost+":"+f'{appSettings.sonarrPort}'
    sonarrHeaders = {'X-Api-Key' : appSettings.sonarrApiKey}

    ombiBaseUrl = "http://"+appSettings.ombiHost+":"+f'{appSettings.ombiPort}'
    ombiHeaders = {'ApiKey' : appSettings.ombiApiKey}
    try:
        radarrResult = requests.get(radarrBaseURL+"/api/v3/system/status", headers=radarrHeaders)
        sonarrResult = requests.get(sonarrBaseURL+"/api/v3/system/status", headers=sonarrHeaders)
        ombiResult = requests.get(ombiBaseUrl+"/api/v1/Status", headers=ombiHeaders)
    except Exception as err:
        raise Exception(str(err))


def import_all_requests():
    test_services()
    addedUsers = 0
    addedMovies = 0
    addedMoviePicks = 0
    addedTVShows = 0
    addedTVShowSeasons = 0
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

        releaseDateMod = datetime.datetime.strptime(releaseDate.replace("T", " "), "%Y-%m-%d %H:%M:%S")
        pickDateMod = datetime.datetime.strptime(pickDate.replace("T", " "), "%Y-%m-%d %H:%M:%S")

        requester, addedUser = check_user_creation(requesterEmail, requesterAlias)
        movie, addedMovie = check_movie_creation(title, theMovieDbID, theMovieDbURL, releaseDateMod, ombiID)
        moviePick, addedMoviePick = check_moviePick_creation(movie, requester, pickDateMod)

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
        pick_date = None

        requester, addedUser = check_user_creation(requesterEmail, requesterAlias)
        tvShow, addedTVShow = check_tvShow_creation(title, tvDbID, tvDbURL, ombiID)
        tvShowSeason, addedTVShowSeason = check_tvShowSeason_creation(tvShow)
        tvShowSeasonPick, addedTVShowPick = check_tvShowSeasonPick_creation(tvShowSeason, requester, pick_date)

        if addedUser:addedUsers+=1
        if addedTVShow:addedTVShows+=1
        if addedTVShowSeason:addedTVShowSeasons+=1
        if addedTVShowPick:addedTVShowPicks+=1
        


    response = "Imported all picks"
    return response