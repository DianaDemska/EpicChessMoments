from flask import Blueprint
import os
from datetime import timedelta, datetime


import googleapiclient.discovery
import googleapiclient.errors

youtubeTimeStamps = Blueprint('youtubeTimeStamps', __name__)
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def getVideoInfo(idVideo):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    api_key = os.environ.get("DEVELOPER_KEY")
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    request = youtube.videos().list(
        part="snippet, liveStreamingDetails",
        id=idVideo
    )
    response = request.execute()

    return response


def liveStream(stream, games):
    table = []
    for item in games:
        isWhite = item.white == stream.userName
        isBlack = item.black == stream.userName
        if item.winner:
            if isWhite and (item.winner != 'white'):
                time = datetime.now().astimezone() - item.createdAt
                table.append(str(timedelta(seconds=time.seconds)))
            if isBlack and (item.winner != 'black'):
                time = datetime.now().astimezone() - item.createdAt
                table.append(str(timedelta(seconds=time.seconds)))
        else:
            if item.whiteRatingDiff or item.blackRatingDiff:
                if isWhite and (int(item.whiteRatingDiff) < 0):
                    time = datetime.now().astimezone() - item.createdAt
                    table.append(str(timedelta(seconds=time.seconds)))
                if isBlack and (int(item.blackRatingDiff) < 0):
                    time = datetime.now().astimezone() - item.createdAt
                    table.append(str(timedelta(seconds=time.seconds)))
    return table


def timming(stream, games):
    table = []
    for item in games:
        isWhite = item.white == stream.userName
        isBlack = item.black == stream.userName
        if item.winner:
            if isWhite and (item.winner != 'white'):
                time = item.createdAt - stream.startTime
                table.append(str(timedelta(seconds=time.seconds)))
            if isBlack and (item.winner != 'black'):
                time = item.createdAt - stream.startTime
                table.append(str(timedelta(seconds=time.seconds)))
        else:
            if item.whiteRatingDiff or item.blackRatingDiff:
                if isWhite and (int(item.whiteRatingDiff) < 0):
                    time = item.createdAt - stream.startTime
                    table.append(str(timedelta(seconds=time.seconds)))
                if isBlack and (int(item.blackRatingDiff) < 0):
                    time = item.createdAt - stream.startTime
                    table.append(str(timedelta(seconds=time.seconds)))
    return table
