from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Stream(db.Model):
    __tablename__ = "Streams"
    idVideo = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    endTime = db.Column(db.DateTime(timezone=True), nullable=False)
    startTime = db.Column(db.DateTime(timezone=True), nullable=False)
    userName = db.Column(db.String(128), nullable=False)
    Games = db.relationship("Games", cascade="all,delete", backref="Streams")
    result = db.Column(db.String(556), nullable=True)

    def __init__(self, idVideo, name, endTime, startTime, userName, result):
        self.idVideo = idVideo
        self.name = name
        self.endTime = endTime
        self.startTime = startTime
        self.userName = userName
        self.result = result


class Games(db.Model):
    __tablename__ = "Games"
    id = db.Column(db.String(128), primary_key=True)
    idVideo = db.Column(db.String(128), db.ForeignKey('Streams.idVideo', ondelete="CASCADE"), nullable=False)
    createdAt = db.Column(db.DateTime(timezone=True), nullable=False)
    white = db.Column(db.String(128), nullable=False)
    black = db.Column(db.String(128), nullable=False)
    winner = db.Column(db.String(128), nullable=True)
    whiteRatingDiff = db.Column(db.String(128), nullable=True)
    blackRatingDiff = db.Column(db.String(128), nullable=True)

    def __init__(self, id, idVideo, createdAt, white, black, winner, whiteRatingDiff, blackRatingDiff):
        self.id = id
        self.idVideo = idVideo
        self.createdAt = createdAt
        self.white = white
        self.black = black
        self.winner = winner
        self.whiteRatingDiff = whiteRatingDiff
        self.blackRatingDiff = blackRatingDiff
