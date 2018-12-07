import spotipy
import spotipy.oauth2 as oauth2
import gui
import urllib3
http = urllib3.PoolManager()
import os


client_id = "7660f65e20dc492fa7a784d5a8118d51"
client_secret = "4577008c88a84b2b83a072533ec7780a"

credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,  
        client_secret=client_secret)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

window = gui.Display("spotiVis", 100, 100)
requestWindow = None
artistField = None

def searchRequest(message, arbitraryFunction):
   global requestWindow, artistField
   requestWindow = gui.Display("Choose Artist",300,150)
   requestWindow.add(gui.Label(message), 25, 20)
   artistField = gui.TextField("What Artist?", 8)
   requestWindow.add(artistField, 25, 50)
   okButton = gui.Button("OK", arbitraryFunction)
   requestWindow.add(okButton, 75, 100)

def main():
   global window, requestWindow, artistField
   requestWindow.close()
   #Search for the artist on spotify
   searchName = artistField.getText()
   print(searchName)
   artistSearch = spotify.search(q='artist:' + searchName, type='artist')
   #print(artistSearch)
   
   #Get the most popular artist
   popularArtist = artistSearch["artists"]["items"][0]
   #Get their icon
   artistImageURL = str(popularArtist["images"][0]["url"])
   print(artistImageURL)
   
   #Pulls the image from the internet. Use this format for anything relating to downloading something from the internet.
   getRequest = http.request('GET', artistImageURL, preload_content=False)
   with open("./cache/artistImageCache.jpg", 'wb') as out:
      while True:
         data = getRequest.read(16)
         if not data:
            break
         out.write(data)
   getRequest.release_conn()
   
   path = os.path.dirname(os.path.realpath(__file__))
   
   artistImage = gui.Icon(path + "/cache/artistImageCache.jpg",100)
   window.add(artistImage)
   
searchRequest("What artist are you interested in?", main)
#artists related to drake
#artists = spotify.search(q='artist:' + "Drake", type='artist')
#drake's album
#albums= spotify.artist_albums("3TVXtAsR1Inumwj472S9r4", album_type=None, country=None,limit=20,offset=0)
#information about the tracks in scorpion
#tracks=spotify.album_tracks("1ATL5GLyefJaxhQzSPVrLX", limit=50, offset=0)
#prints drakes top tracks
#topTracks=spotify.artist_top_tracks("3TVXtAsR1Inumwj472S9r4", country='US')
#print(topTracks)