import json
import re
import urllib.request
from flask import request, Flask, jsonify

from pytube import YouTube 

api_key = "AIzaSyAKkGJ78S330UDgvqQ6E04hmhCTGNygf7Q"

app = Flask(__name__)
app.config['DEBUG']= True

def youtubeSearch(keyword): 
    try : 
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&order=viewCount&q="+keyword+"&key="+api_key
        json_url= urllib.request.urlopen(url)
        data = json.loads(json_url.read())
        res = []
        for item in data['items'] : 
            result  = {
                'title' : item['snippet']['title'], 
                'publishedAt' : item['snippet']['publishedAt']
            }
            res.append(result)
        return jsonify(res)
    except : 
        req = "Video Not Found."
        return req

@app.route('/', methods=['GET'])
def index(): 
    return youtubeSearch(request.args.get('keyword'))

if __name__ == "__main__" : 
    app.run()
