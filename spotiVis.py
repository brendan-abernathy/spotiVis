import spotipy
import spotipy.oauth2 as oauth2


client_id = "7660f65e20dc492fa7a784d5a8118d51" #fill this in
client_secret = "4577008c88a84b2b83a072533ec7780a" #fill this in

credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,  
        client_secret=client_secret)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)
#artists related to drake
artists = spotify.search(q='artist:' + "Drake", type='artist')
#drake's album
albums= spotify.artist_albums("3TVXtAsR1Inumwj472S9r4", album_type=None, country=None,limit=20,offset=0)
#information about the tracks in scorpion
tracks=spotify.album_tracks("1ATL5GLyefJaxhQzSPVrLX", limit=50, offset=0)
#prints drakes top tracks
topTracks=spotify.artist_top_tracks("3TVXtAsR1Inumwj472S9r4", country='US')
print(topTracks)