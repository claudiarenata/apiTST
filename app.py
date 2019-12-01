# API BY ZALIKHA ADIERA GAMBETTA - 18217027 
# API BY CLAUDIA RENATA MAHARANI D. - 18217048

import re
import urllib.request
import json
import spotipy
import spotipy.util as util
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'content-type'
app.config['CORS_RESOURCES'] = '*'
app.config['CORS_METHODS'] = "GET,POST,OPTIONS"


mysql = MySQL()
app.config['DEBUG'] = True

# configure db mysql #
app.config['MYSQL_DATABASE_HOST'] = '34.230.47.220'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'playlist'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
mysql.init_app(app)

# data yang didapat dari spotify :
#client id : 594b6025eefd434587568c7b090e3c6b
#client secret : c6f5c709eb834656b594da0c2938c557

# get token with spotipy #
CLIENT_ID = "594b6025eefd434587568c7b090e3c6b"
CLIENT_SECRET = "c6f5c709eb834656b594da0c2938c557"
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# get data from spotify #
@app.route('/api/playlist', methods=['POST', 'OPTIONS'])
@cross_origin()
def songs():
    global conn, cursor
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        pName = request.json.get('playlistName')
        # memasukan data ke table playlist #
        playtab = """INSERT INTO playlist(playlistName) VALUES (%s)"""
        data = (pName)
        cursor.execute(playtab, data)
        conn.commit()
        songs = request.json.get('songs')
        songsList = []
        # fetch playlistID #
        reqplayID = cursor.execute("SELECT playlistID FROM playlist WHERE playlistName=%s", pName)
        resplayID = cursor.fetchall()
        for x in songs:     
            sName = x.get('songsName')
            sart = x.get('songsArtist')
            psaved = sp.search(q=sName + " " + sart, limit=1, type='track')
            tracks = psaved['tracks']
            items = tracks['items']
            artist = items[0]['artists']
            artistList = []
            # memasukan data lagu ke tabel tracks #
            trackstab = """INSERT INTO tracks(songsName, songsURL, playlistID) VALUES (%s, %s, %s)"""
            data = (items[0]['name'], items[0]['uri'], resplayID[0])
            cursor.execute(trackstab, data)
            conn.commit()
            # fetch songsID #
            reqsongID = cursor.execute("SELECT songsID FROM tracks WHERE tracks.playlistID = %s ORDER BY songsID DESC limit 1", resplayID[0])
            ressongID = cursor.fetchall()
            for y in artist:
                nartist = y.get('name')
                artistList.append(nartist)
                # memasukan data artis ke tabel artists #
                artiststab = """INSERT INTO artists(artistsName, songsID) VALUES (%s, %s)"""
                data = (nartist, ressongID[0])
                cursor.execute(artiststab,data)
                conn.commit()
            hasil = {
                'songsName' : items[0]['name'],
                'songsURL' : items[0]['uri'],
                'songsArtist' : artistList
            }
            songsList.append(hasil)
        response = {
            'playlistName' : pName,
            'songList' : songsList
        }
    except Exception as e:
        return e
    finally:
        conn.close()
        cursor.close()
    return jsonify(response)

# read playlist saved in database #
@app.route('/api/playlist', methods=['GET'])
@cross_origin()
def playlist():
    global conn, cursor
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        pName = request.args.get('playlistName')
        playlistID = cursor.execute("SELECT playlistID FROM playlist WHERE playlistName = %s", pName)
        resPlaylist = cursor.fetchall()
        daftarlagu = cursor.execute("SELECT songsName, songsURL, songsID FROM tracks WHERE tracks.playlistID = %s", resPlaylist)
        resTracks = cursor.fetchall()
        tracksList = []
        for x in resTracks:
            artistsList = []
            daftarartis = cursor.execute("SELECT artistsName FROM artists WHERE artists.songsID = %s", x[2])
            resArtists = cursor.fetchall()
            for y in resArtists: {
                artistsList.append(y[0])
            }
            hasil = {
                'songsName': x[0],
                'songsURL' : x[1],
                'songsArtist' : artistsList
            }
            tracksList.append(hasil)
        response = {
            'playlistName' : pName,
            'tracks' : tracksList
        }
    except Exception as e:
        return e
    finally:
        conn.close()
        cursor.close()
    return jsonify(response)

# get all playlist in database
@app.route('/api/allplaylist', methods=['GET'])
@cross_origin()
def allplaylist():
    global conn, cursor
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlist")
    pList = cursor.fetchall()
    # resplaylist = []
    # for x in pList :
    #     resplaylist.append(x[1])
    response = {
        'playlist' : pList
    }
    return jsonify(response)
    conn.close()
    cursor.close()

# delete playlist data #
@app.route('/api/playlist', methods=['DELETE'])
@cross_origin()
def delete():
    global cursor, conn
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        pName = request.args.get('playlistName')
        playlistID = cursor.execute("SELECT playlistID FROM playlist WHERE playlistName = %s", pName)
        resPlaylist = cursor.fetchall()
        sqlplaylist = cursor.execute("DELETE FROM playlist WHERE playlistName=%s", pName)
        conn.commit()

        songsID = cursor.execute("SELECT songsID FROM tracks WHERE tracks.playlistID=%s", resPlaylist)
        resSongsID = cursor.fetchall()
        sqlsongs = cursor.execute("DELETE FROM tracks WHERE tracks.playlistID=%s", resPlaylist[0])
        conn.commit()
        
        for x in resSongsID:
            sqlartists = cursor.execute("DELETE FROM artists WHERE artists.songsID=%s", x[0])
            conn.commit()
        response = {
            'status' : 200,
            'message' : "Success delete data from playlist!"
        }
    except Exception as e:
        return e
    finally:
        cursor.close()
        conn.close()
    return jsonify(response)

# show charts of songs/artists from database #
@app.route('/api/charts', methods=['GET'])
@cross_origin()
def charts():
    global conn, cursor
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        artist = cursor.execute("SELECT * FROM artists")
        allartist = cursor.fetchall()
        response = {}
        for x in allartist:
            if hasattr(response, x[1]):
                response[x[1]] += 1
            else:
                response[x[1]] = 1
    except Exception as e:
        return e
    finally:
        conn.close()
        cursor.close()
    return jsonify(response)

# api audi
api_key = "AIzaSyAKkGJ78S330UDgvqQ6E04hmhCTGNygf7Q"

def youtubeSearch(keyword): 
    try : 
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&order=relevance&q="+keyword.replace(" ", "%20")+"&key="+api_key
        json_url= urllib.request.urlopen(url)
        data = json.loads(json_url.read())
        res = []
        
        for item in data['items'] : 
            result  = {
                'title' : item['snippet']['title'], 
                'publishedAt' : item['snippet']['publishedAt'],
                'url' : "https://m.youtube.com/watch?v="+item['id']['videoId']
            }
            res.append(result)
        return jsonify(res)
    except : 
        req = "Video Not Found."
        return req

@app.route('/api/youtubesearch', methods=['GET'])
@cross_origin()
def index():
    masukkan = request.args.get('keyword')
    return youtubeSearch(masukkan)

# execute the app #
if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port=6001)
