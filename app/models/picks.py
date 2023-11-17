from app.extensions import db

class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pick_date = db.Column(db.DateTime)
    media_type = db.Column(db.String(50))

    #Relations
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    pick_type_id = db.Column(db.Integer, db.ForeignKey('pick_type.id'))

    user = db.relationship('User', back_populates='picks')
    media = db.relationship('Media', back_populates='picks')
    pick_type = db.relationship('PickType')

    #Ensures that a new pick has all its information, and the correct media type is set
    def __init__(self, user, media, pick_date, pick_type):
        self.user = user
        self.media = media
        self.media_type = media.type
        self.pick_date = pick_date
        self.pick_type = PickType.query.filter_by(name=pick_type).first()

    def __repr__(self) -> str:
        return f'Pick: {self.media} assigned to {self.user} on {self.pick_date} through {self.pick_type.name}'
    
    def to_dict(self) :
        if self.media.type == "movie":
            media_db_url = self.media.TMDB_url
            full_title = f'{self.media.title} ({self.media.year})'
        else:
            media_db_url = self.media.theTVDB_url
            full_title = self.media.title
        return {
            'media_title': full_title,
            'media_db_url': media_db_url,
            'poster_url': self.media.poster_url,
            'pick_type': self.pick_type.name,
            'pick_date': self.pick_date,
            'media_size': self.media.total_size,
            'pick_id': self.id,
            'media_type': self.media.type
        }

class PickType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name
    
    def __repr__(self) -> str:
        return f'Pick Type: {self.name}'
    
    @staticmethod
    def insert_pick_types():
        types = [
            "Watched",
            "Picked up",
            "Requested",
            "Assigned"
        ]

        for type in types:
            pick_type = PickType.query.filter_by(name=type).first()
            if not pick_type:
                new_pick_type = PickType(name=type)
                db.session.add(new_pick_type)
            db.session.commit()