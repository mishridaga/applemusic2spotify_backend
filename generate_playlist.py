import re
from difflib import SequenceMatcher
import requests
import json

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def generate_id_list(tracks_dict, headers):
    list_ids = []
    for track in tracks_dict:
        if not (track['Name'] or track['Artist']):
            continue;
        name = track['Name']
        name = re.sub(r'\(.*\)', "", name)
        name = re.sub(r'\[.*\]', "", name)
        artist = track['Artist'].split("&")[0]
        result = requests.get('https://api.spotify.com/v1/search?q=artist:'+artist+' track:'+name+'&type=track&limit=1', headers=headers)
        if result.json()['tracks']['items']:
            list_ids += [result.json()['tracks']['items'][0]['id']]
        else:
            result = requests.get('https://api.spotify.com/v1/search?q=track:'+name+'&type=track&limit=10', headers=headers)
            max_similarity = 0
            max_similarity_artist = None
            for r in result.json()['tracks']['items']:
                #calculate how similar the artist name is to what we want
                similarity = similar(r['album']['artists'][0]['name'], artist)
                if similarity >= max_similarity:
                    max_similarity = similarity
                    max_similarity_artist = r
            #if we find an artist name with relatively high similarity - go for it
            if max_similarity > .5:
                list_ids += [max_similarity_artist.json()['tracks']['items'][0]['id']]
    return list_ids
    
def create_playlist(track_ids, playlist_name, headers):
    result = requests.get("https://api.spotify.com/v1/me", headers=headers)
    username = result.json()['id']
    print(username)
    data = {'name' : playlist_name}
    result = requests.post('https://api.spotify.com/v1/users/' + username + '/playlists', data=json.dumps(data), headers=headers )
    print(result.content)
    print(result.status_code)
    playlist_id = result.json()['uri'].split(":")[-1]
    track_ids = ["spotify:track:" + x for x in track_ids]
    data = {'uris' : track_ids}
    result = requests.post('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', data=json.dumps(data), headers=headers)
    return result.status_code
    
