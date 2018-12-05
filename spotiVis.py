import spotipy
import spotipy.oauth2 as oauth2


client_id = "7660f65e20dc492fa7a784d5a8118d51" #fill this in
client_secret = "4577008c88a84b2b83a072533ec7780a" #fill this in

credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,  
        client_secret=client_secret)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

results = spotify.search(q='artist:' + "Queen", type='artist')
print(results)