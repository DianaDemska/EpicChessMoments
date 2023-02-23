from flask import render_template, Blueprint, url_for, redirect, flash, request
from werkzeug.utils import secure_filename
import os
from .youtubeTimeStamps import getVideoInfo, timming
from .crud import getStreamsInfo, getStreamInfo, editStreamInfo, delStreamInfo
from .crud import getGamesInfo, getGameInfo, editGamesInfo, delGamesInfo
from .models import Stream, Games

overview = Blueprint('overview', __name__)


# Streams


@overview.route("/allStreams", methods=['GET', 'POST'])
def allStreams():
    streams = getStreamsInfo()
    return render_template('overview.html', streams=streams)


@overview.route("/editStream/<string:id>", methods=['GET', 'POST'])
def editStream(id):
    stream = getStreamInfo(id)
    if not stream:
        flash('Not found')
        return redirect(url_for('overview.allStreams'))
    if request.method == 'POST':
        idVideo = id
        name = request.form['name']
        endTime = stream.endTime
        startTime = stream.startTime
        userName = stream.userName
        result = request.form['result']
        info = Stream(idVideo=idVideo, name=name, endTime=endTime, startTime=startTime, userName=userName, result=result)
        editStreamInfo(info)
        return redirect(url_for('overview.allStreams'))
    return render_template('editStream.html', stream=stream)


@overview.route('/deleteStream/<string:id>', methods=['GET', 'POST'])
def deleteStream(id):
    stream = Stream.query.get(id)
    if not stream:
        flash('Not found')
        return redirect(url_for('overview.allStreams'))
    delStreamInfo(stream)
    return redirect(url_for('overview.allStreams'))


# Games


@overview.route("/allGames/<string:id>", methods=['GET', 'POST'])
def allGames(id):
    games = getGamesInfo(id)
    if not games:
        flash('Not found')
        return redirect(url_for('overview.allStreams'))
    return render_template('games.html', games=games)


@overview.route("/editGame/<string:id>", methods=['GET', 'POST'])
def editGame(id):
    game = getGameInfo(id)
    if not game:
        flash('Not found')
        return redirect(url_for('overview.allGames', id=game.idVideo))
    if request.method == 'POST':
        id = id
        idVideo = game.idVideo
        createdAt = game.createdAt
        white = game.white
        black = game.black
        winner = request.form['winner']
        whiteRatingDiff = game.whiteRatingDiff
        blackRatingDiff = game.blackRatingDiff
        info = Games(id=id, idVideo=idVideo, createdAt=createdAt, white=white, black=black, winner=winner, whiteRatingDiff=whiteRatingDiff, blackRatingDiff=blackRatingDiff)
        editGamesInfo(info)
        return redirect(url_for('overview.allGames', id=idVideo))
    return render_template('editGame.html', game=game)


@overview.route('/deleteGame/<string:id>', methods=['GET', 'POST'])
def deleteGame(id):
    game = getGameInfo(id)
    if not game:
        flash('Not found')
        return redirect(url_for('overview.allStreams'))
    delGamesInfo(game)
    return redirect(url_for('overview.allStreams'))


@overview.route('/viewResult/<string:id>', methods=['GET', 'POST'])
def viewResult(id):
    stream = getStreamInfo(id)
    if not stream:
        flash('Not found')
        return redirect(url_for('overview.allStreams'))
    return render_template('result.html', result=stream.result)
