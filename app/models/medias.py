from flask import current_app
from app.extensions import db
from .application_settings import AppSettings
from datetime import datetime
from dateutil.relativedelta import relativedelta

def default_TMDB_url(context):
    return f'https://www.themoviedb.org/movie/{context.get_current_parameters()["TMDB_id"]}'

def default_theTVDB_url(context):
    return f'https://www.thetvdb.com/?id={context.get_current_parameters()["theTVDB_id"]}&tab=series'

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    title = db.Column(db.String(100), nullable = False)

    ombi_id = db.Column(db.Integer, nullable = False)
    total_size = db.Column(db.BigInteger)
    poster_url = db.Column(db.String(100))

    abandoned_date = db.Column(db.DateTime)
    expiry_date = db.Column(db.DateTime)
    deletion_date = db.Column(db.DateTime)

    #Relations
    picks = db.relationship('Pick', back_populates='media', cascade='all, delete')

    __mapper_args__ = {
        'polymorphic_identity': 'media',
        'polymorphic_on': type
    }

    def to_dict(self) :
        if self.type == "movie":
            media_db_url = self.TMDB_url
            full_title = f'{self.title} ({self.year})'
        else:
            media_db_url = self.theTVDB_url
            full_title = self.title
        num_picks = len(self.picks)
        return {
                'title': full_title,
                'media_db_url': media_db_url,
                'poster_url': self.poster_url,
                'media_size': self.total_size,
                'abandoned_date': self.abandoned_date,
                'deletion_date': self.deletion_date,
                'num_picks': num_picks,
                'media_id': self.id,
                'media_type': self.type
            }

    def update_abandoned_details(self):
        if self.picks:
            self.abandoned_date = None
            self.expiry_date = None
            self.deletion_date = None
        else:
            self.abandoned_date = datetime.utcnow()
            self.update_deletion_details()
        db.session.add(self)
        db.session.commit()

    def update_deletion_details(self):
        current_app_settings = AppSettings.query.first()
        self.expiry_date = self.abandoned_date + relativedelta(**{current_app_settings.expiry_time_unit: current_app_settings.expiry_time_number})
        current_app.logger.debug(f'Expiry date of {self} set to {self.expiry_date}')
        delete_time = current_app_settings.next_delete
        if (delete_time < self.expiry_date):
            #Find the next deletion date that lands after the expiration date
            deletion_delta = relativedelta(**{current_app_settings.deletion_time_unit: current_app_settings.deletion_time_number})
            while delete_time < self.expiry_date:
                delete_time += deletion_delta
            #There should be a faster way to calculate this, but I do not know it
            #It shouldn't have a big impact anyway.
            #This method does not work because division of relativedelta is not doable.
            #deltaMulti = math.ceil(relativedelta(media.expiryDate, delete_time)/deletion_delta)
            #delete_time = deltaMulti * deletion_delta
        self.deletion_date = delete_time
        current_app.logger.debug(f'Deletion date of {self} set to {self.deletion_date}')
        db.session.add(self)
        db.session.commit()
    
    def is_abandoned(self):
        return (not self.picks)

    @staticmethod
    def update_all_deletion_details():
        for media in Media.query.all():
            if media.is_abandoned():
                media.update_deletion_details()

class Movie(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    TMDB_id = db.Column(db.Integer, nullable=False, unique=True)
    TMDB_url = db.Column(db.String(100), default=default_TMDB_url)
    radarr_id = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "movie",
    }

    def __repr__(self) -> str:
        return f'Movie: {self.title} ({self.year})'


class TVShow(Media):
    id = db.Column(db.Integer, db.ForeignKey('media.id'), primary_key=True)
    theTVDB_id = db.Column(db.Integer, nullable=False, unique=True)
    theTVDB_url = db.Column(db.String(100), default=default_theTVDB_url)
    sonarr_id = db.Column(db.Integer)

    __mapper_args__ = {
        "polymorphic_identity": "tv_show",
    }

    def __repr__(self) -> str:
        return f'TV Show: {self.title}'