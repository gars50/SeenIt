from app.models.connections import RadarrConnection, SonarrConnection, OmbiConnection
from app.extensions import db

db.session.add(RadarrConnection())
db.session.add(SonarrConnection())
db.session.add(OmbiConnection())

db.session.commit()