import requests, datetime
from app.models import User, Movie, TVShow, AppSettings
from app import db

def check_user_creation(email, alias):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        user.alias = alias
        db.session.add(user)
        db.session.commit()
    return User.query.filter_by(email=email).first()

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

    appSettings = AppSettings.query.first()
    ombiBaseURL = "http://"+appSettings.ombiHost+":"+f'{appSettings.ombiPort}'
    headers = {'ApiKey' : appSettings.ombiApiKey}

    movieRequestsResponse = requests.get(ombiBaseURL+"/api/v1/Request/movie", headers=headers)
    movieRequests = movieRequestsResponse.json()

    importedMovies = 0
    for movieRequest in movieRequests:
        title = movieRequest["title"]
        theMovieDbID = movieRequest["theMovieDbId"]
        theMovieDbURL = "https://www.themoviedb.org/movie/"+str(theMovieDbID)
        releaseDate = movieRequest["releaseDate"]
        requesterEmail = movieRequest["requestedUser"]["email"]
        requesterAlias = movieRequest["requestedUser"]["userAlias"]
        ombiID = movieRequest["id"]
        releaseDateMod = datetime.datetime.strptime(releaseDate.replace("T", " "), "%Y-%m-%d %H:%M:%S")
        requester = check_user_creation(requesterEmail, requesterAlias)

        movie = Movie.query.filter_by(ombiID=ombiID).first()
        if not movie:
            importedMovies+=1
            newMovieRequest = Movie(title=title, theMovieDbID=theMovieDbID, theMovieDbURL=theMovieDbURL, releaseDate=releaseDateMod, ombiID=ombiID, owner_id=requester.id)
            db.session.add(newMovieRequest)
            db.session.commit()


    TVRequestsResponse = requests.get(ombiBaseURL+"/api/v1/Request/tv", headers=headers)
    TVRequests = TVRequestsResponse.json()

    importedShows = 0
    for TVRequest in TVRequests:
        title = TVRequest["title"]
        tvDbID = TVRequest["tvDbId"]
        tvDbURL = "https://www.thetvdb.com/?id="+str(tvDbID)+"&tab=series"

        requesterEmail = TVRequest["childRequests"][0]["requestedUser"]["email"]
        requesterAlias = TVRequest["childRequests"][0]["requestedUser"]["userAlias"]
        ombiID = TVRequest["id"]
        requester = check_user_creation(requesterEmail, requesterAlias)
        
        show = TVShow.query.filter_by(ombiID=ombiID).first()
        if not show:
            importedShows+=1
            newTVRequest = TVShow(title=title, tvDbID=tvDbID, tvDbURL=tvDbURL, ombiID=ombiID, owner_id=requester.id)
            db.session.add(newTVRequest)
            db.session.commit()

    response = "Imported "+str(importedMovies)+" movies and "+str(importedShows)+" TV Shows"
    return response