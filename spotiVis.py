import spotipy
import spotipy.oauth2 as oauth2
import gui
import urllib3
http = urllib3.PoolManager()
import os

def getScreenWidth():
  return gui.Toolkit.getDefaultToolkit().getScreenSize().width

def getScreenHeight():
  return gui.Toolkit.getDefaultToolkit().getScreenSize().height

client_id = "7660f65e20dc492fa7a784d5a8118d51"
client_secret = "4577008c88a84b2b83a072533ec7780a"

credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,  
        client_secret=client_secret)

token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

window = gui.Display("spotiVis", getScreenWidth(), getScreenHeight(),0,0, gui.Color(60,60,60))
requestWindow = None
artistField = None

def searchRequest(message, arbitraryFunction):
   global requestWindow, artistField
   requestWindow = gui.Display("Choose Artist",300,100,(getScreenWidth()/2)-150, (getScreenHeight()/2)-100)
   requestWindow.add(gui.Label(message), 25, 15)
   artistField = gui.TextField("What Artist?", 8)
   requestWindow.add(artistField, 25, 40)
   okButton = gui.Button("OK", arbitraryFunction)
   requestWindow.add(okButton, 215, 60)

def getImage(url,saveName):
   getRequest = http.request('GET', url, preload_content=False)
   with open("./cache/" + saveName, 'wb') as out:
      while True:
         data = getRequest.read(16)
         if not data:
            return False
         out.write(data)
   getRequest.release_conn()
   return True

def getMostPopularArtist(search):
   if(len(search["artists"]["items"]) <= 0):
      window.close()
      return -1
   #Get the most popular artist
   popularArtist = search["artists"]["items"][0]
   return popularArtist

#artists related to drake
#artists = spotify.search(q='artist:' + "Drake", type='artist')
#drake's album
#albums= spotify.artist_albums("3TVXtAsR1Inumwj472S9r4", album_type=None, country=None,limit=20,offset=0)
#information about the tracks in scorpion
#tracks=spotify.album_tracks("1ATL5GLyefJaxhQzSPVrLX", limit=50, offset=0)
#prints drakes top tracks
#topTracks=spotify.artist_top_tracks("3TVXtAsR1Inumwj472S9r4", country='US')
#print(topTracks)

def main():
   global window, requestWindow, artistField
   requestWindow.close()
   #Search for the artist on spotify
   searchName = artistField.getText()
   artistSearch = spotify.search(q='artist:' + searchName, type='artist')
   artist = getMostPopularArtist(artistSearch)
   
   #Get their icon
   artistImageURL = str(artist["images"][0]["url"])
   
   #Pulls the image from the internet. Use this format for anything relating to downloading something from the internet.
   getImage(artistImageURL, "artistImageCache.jpg")
   
   path = os.path.dirname(os.path.realpath(__file__))
   
   artistImage = gui.Icon(path + "/cache/artistImageCache.jpg",300)
   artistLabel = gui.Label(str(artist["name"]), gui.LEFT, gui.Color(255, 255, 255))
   artistLabel.setFont(gui.Font("Courier", gui.Font.BOLD, 136))
   genreLabel = gui.Label("Genre: " + str(artist["genres"][0]).title(), gui.LEFT, gui.Color(255, 255, 255))
   genreLabel.setFont(gui.Font("Courier", gui.Font.BOLD, 36))
   
   window.add(artistImage, getScreenWidth() - 350, 50)
   window.add(artistLabel, 50, 30)
   window.add(genreLabel, 50, 170)
   
   return 0

searchRequest("What artist are you interested in?", main)