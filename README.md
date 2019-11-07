# applemusic2spotify_backend
Backend for Spotify web app that handles playlist conversion from Apple Music to Spotify. 
Lambda function recieves input from AWS API Gateway Post Request after user has authorized web app with spotify and generated an access token: 

Post Request Body: 
  {
    "txtFile" : 
    "playlistName" :
    "accessToken"
 }
 
 Lambda Function: 
  1. Parses text file and then makes Spotify API Search calls to find the corresponding Spotify Track URI
  2. Creates playlist in users context under playlistName
  3. Populates playlist with tracks extracted from input txtFile
    
 To Do: 
  1. More error handling
  2. Make sure CORS is working as expected
  3. Generate stats on how accurate playlist conversion is: how many tracks are incorrectly identified, how many tracks are not found, what can make search queries more accurate? 
