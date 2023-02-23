from flask import Blueprint
from datetime import datetime

from .models import Stream, Games
from . import db

crud = Blueprint('crud', __name__)

# Stream


def addStreamInfo(info, userName):
    idVideo = info['items'][0]['id']
    name = info['items'][0]['snippet']['title']
    startTime = datetime.strptime(info['items'][0]['liveStreamingDetails']['actualStartTime'], "%Y-%m-%dT%H:%M:%SZ")
    time = info['items'][0].get('liveStreamingDetails', {}).get('actualEndTime')
    if time:
        endTime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    else:
        endTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    result = None

    item = getStreamInfo(idVideo)
    if item:
        return
    else:
        newStream = Stream(idVideo=idVideo, name=name, startTime=startTime, endTime=endTime, userName=userName, result=result)
        db.session.add(newStream)
        db.session.commit()


def getStreamInfo(idVideo):
    return Stream.query.filter_by(idVideo=idVideo).first()


def getStreamsInfo():
    return Stream.query.all()


def editStreamInfo(editInfo):
    stream = getStreamInfo(editInfo.idVideo)
    if stream:
        stream.name = editInfo.name
        stream.result = editInfo.result
        db.session.merge(stream)
        db.session.commit()


def updateResult(idVideo, result):
    item = getStreamInfo(idVideo)
    if item:
        item.result = result
        db.session.merge(item)
        db.session.commit()


def delStreamInfo(stream):
    db.session.delete(stream)
    db.session.commit()


# Games


def addGamesInfo(idVideo, listOfGames):
    for game in listOfGames:
        id = game['id']
        createdAt = game['createdAt']
        white = game['players']['white']['user']['name']
        black = game['players']['black']['user']['name']
        winner = game.get('winner')
        idVideo = idVideo
        whiteRatingDiff = game.get('players', {}).get('white', {}).get('ratingDiff')
        blackRatingDiff = game.get('players', {}).get('black', {}).get('ratingDiff')
        item = Games.query.filter_by(id=id).first()
        if item:
            continue
        else:
            newGame = Games(id=id, createdAt=createdAt, white=white, black=black, winner=winner, whiteRatingDiff=whiteRatingDiff, blackRatingDiff=blackRatingDiff, idVideo=idVideo)
            db.session.add(newGame)
            db.session.commit()


def getGamesInfo(idVideo):
    return Games.query.filter_by(idVideo=idVideo)


def getGameInfo(id):
    return Games.query.filter_by(id=id).one()


def editGamesInfo(editGame):
    game = getGameInfo(editGame.id)
    if game:
        game.winner = editGame.winner
        db.session.merge(game)
        db.session.commit()


def delGamesInfo(game):
    db.session.delete(game)
    db.session.commit()
