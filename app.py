# API BY ZALIKHA ADIERA GAMBETTA - 18217027 #

import json
import spotipy
import spotipy.util as util
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
mysql = MySQL()
app.config['DEBUG'] = True

# configure db mysql #
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
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

# get data from spotify #
@app.route('/api/playlist', methods=['POST'])
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

# delete playlist data #
@app.route('/api/playlist', methods=['DELETE'])
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

# execute the app #
if __name__ == '__main__':
    app.run()