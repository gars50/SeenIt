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

def import_all_requests():
    print("Running import_data")
    appSettings = AppSettings.query.first()
    ombiBaseURL = "http://"+appSettings.ombiHost+":"+f'{appSettings.ombiPort}'
    headers = {'ApiKey' : appSettings.ombiApiKey}

    movieRequestsResponse = requests.get(ombiBaseURL+"/api/v1/Request/movie", headers=headers)
    movieRequests = movieRequestsResponse.json()

    for movieRequest in movieRequests:
        theMovieDbId = movieRequest["theMovieDbId"]
        title = movieRequest["title"]
        releaseDate = movieRequest["releaseDate"]
        requesterEmail = movieRequest["requestedUser"]["email"]
        requesterAlias = movieRequest["requestedUser"]["userAlias"]
        ombiID = movieRequest["id"]

        releaseDateMod = datetime.datetime.strptime(releaseDate.replace("T", " "), "%Y-%m-%d %H:%M:%S")
        requester = check_user_creation(requesterEmail, requesterAlias)
        newMovieRequest = Movie(theMovieDbId=theMovieDbId, title=title, releaseDate=releaseDateMod, ombiID=ombiID, owner_id=requester.id)
        db.session.add(newMovieRequest)
        db.session.commit()


    TVRequestsResponse = requests.get(ombiBaseURL+"/api/v1/Request/tv", headers=headers)
    TVRequests = TVRequestsResponse.json()

    for TVRequest in TVRequests:
        tvDbId = TVRequest["tvDbId"]
        title = TVRequest["title"]

        requesterEmail = TVRequest["childRequests"][0]["requestedUser"]["email"]
        requesterAlias = TVRequest["childRequests"][0]["requestedUser"]["userAlias"]
        ombiID = TVRequest["id"]

        requester = check_user_creation(requesterEmail, requesterAlias)
        newTVRequest = TVShow(tvDbId=tvDbId, title=title, ombiID=ombiID, owner_id=requester.id)
        db.session.add(newTVRequest)
        db.session.commit()


    response = "Data OK"
    return response

#Get all requests from Ombi
#For each request, check if the request already exists. If not, create a request, associate the user with the email address. If user does not exist, create it.