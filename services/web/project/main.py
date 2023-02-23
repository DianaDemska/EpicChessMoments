from flask import send_from_directory, request, render_template, Blueprint
from flask import flash
from werkzeug.utils import secure_filename
import os
from . import client
from .youtubeTimeStamps import getVideoInfo, timming, liveStream
from .crud import addStreamInfo, addGamesInfo, updateResult, getStreamInfo
from .crud import getGamesInfo


main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('main.html')


@main.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(main.config["STATIC_FOLDER"], filename)


@main.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(main.config["MEDIA_FOLDER"], filename)


@main.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(main.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """


@main.route("/getTimming", methods=["GET", "POST"])
def getTimming():
    if request.method == "POST":
        idViedo = request.form.get('idVideo')
        userName = request.form.get('userName')
        isLive = True if request.form.get('isLive') else False
        jsonFromyoutube = getVideoInfo(idViedo)
        if jsonFromyoutube['pageInfo']['totalResults'] == 0:
            flash('Video Not found')
        addStreamInfo(jsonFromyoutube, userName)
        infoStream = getStreamInfo(idViedo)
        listOfGames = list(client.games.export_by_player(infoStream.userName, since=int(infoStream.startTime.timestamp() * 1000), until=int(infoStream.endTime.timestamp() * 1000)))
        addGamesInfo(idViedo, listOfGames)
        storedGames = getGamesInfo(idViedo)
        if isLive:
            info = liveStream(infoStream, storedGames)
        else:
            info = timming(infoStream, storedGames)
        updateResult(idViedo, info)
        return render_template('main.html', info=info)
