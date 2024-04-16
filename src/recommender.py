import requests
import json
import random
import yaml


with open('src/config/config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

API_KEY = config['Last_FM_API']['API_KEY']
USER_AGENT = config['Last_FM_API']['USER_AGENT']


headers = {
    'user-agent': USER_AGENT
}

def lastfm_getTopTracks(genre):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'https://ws.audioscrobbler.com/2.0/'
    payload = {}
    r = []

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'
    payload['tag'] = genre
    payload['method'] = 'tag.getTopTracks'
    payload['limit'] = '4'
    payload['page'] = random.randint(1, 2000)

    response = requests.get(url, headers=headers, params=payload) 
    data = json.loads(response.text)

    for i in data['tracks']['track']:
        r.append({"mbid": i['artist']['mbid'],
                  "artistName": i['artist']['name'],
                  "trackName": i['name']})

    return r


if(__name__ == '__main__'):
    r = lastfm_getTopTracks('jazz')

