import requests
import boto3
import json
import text_parser
import authorization
import generate_playlist

def lambda_handler(event, context):
    try:
        content = json.loads(event['body'], strict = False)
        filename = content['txtFile']
        playlistName = content['playlistName']
        accessToken = content['accessToken']
    
    except:
        {"statusCode" : 502, "message" : "bad request input"}
        
    try:
        id_list = text_parser.create_track_list(filename)
    except:
        {"statusCode" : 502, "message" : "bad file input"}
    

    #Create headers for requests
    headers = {'Authorization': 'Bearer ' + accessToken, 'Content-Type': 'application/json', 'Accept': 'application/json'}

    #Generate List of Song ID's
    list_ids = generate_playlist.generate_id_list(id_list, headers)
    
    #Create Playlist
    try:
        status = generate_playlist.create_playlist(list_ids, playlistName, headers)
    except:
        return {"statusCode" : status}

