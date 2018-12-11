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

class AlbumTrack:
   def __init__(self,json):
      self.name = json["name"]
      self.number = json["track_number"]
      self.trackID = json["id"]
   def __repr__(self):
      return str(self.name) + " " + str(self.trackID)

class Album:
   global window
   albums = []
   def __init__(self,json):
      path = os.path.dirname(os.path.realpath(__file__))
      self.name = json["name"]
      maxNameLength = 17
      if(len(self.name)>maxNameLength):
         self.name = self.name[0:maxNameLength] + "..."
      self.nameLabel = gui.Label(self.name,gui.LEFT,gui.Color(255,255,255))
      self.nameLabel.setFont(gui.Font("Futura", gui.Font.PLAIN, 36))
      getImage(json["images"][1]["url"], "albumArtCache.jpg")
      self.art = gui.Icon(path + "/cache/albumArtCache.jpg",150)
      self.totalTracks = json["total_tracks"]
      self.releaseDate = str(json["release_date"])
      self.albumID = str(json["id"])
      self.albumTracksSearch = spotify.album_tracks(self.albumID, limit=50, offset=0)
      self.tracks = []
      for trackData in self.albumTracksSearch["items"]:
         newTrack = AlbumTrack(trackData)
         self.tracks.append(newTrack)
      #Todo: grab tracks and add them to here.
      Album.albums.append(self)
      if(len(Album.albums)<=3):
         window.add(self.art, 50, 225 + (len(Album.albums)-1)*200)
         window.add(self.nameLabel, 225, 225 + (len(Album.albums)-1)*200)
         
   #def update(self):
   
   
   def __repr__(self):
      return str(self.name) + " " + str(self.albumID)

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
removables = []

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
   
   artistName = str(artist["name"])
   maxNameLength = 17
   if(len(artistName)>maxNameLength):
      artistName = artistName[0:maxNameLength] + "..."
   
   artistImage = gui.Icon(path + "/cache/artistImageCache.jpg",200)
   artistLabel = gui.Label(artistName, gui.LEFT, gui.Color(255, 255, 255))
   artistLabel.setFont(gui.Font("Futura", gui.Font.BOLD, 72))
   genreLabel = gui.Label("Genre: " + str(artist["genres"][0]).title(), gui.LEFT, gui.Color(255, 255, 255))
   genreLabel.setFont(gui.Font("Futura", gui.Font.ITALIC, 36))
   
   window.add(artistImage, getScreenWidth() - 250, 50)
   window.add(artistLabel, 50, 30)
   window.add(genreLabel, 50, 125)
   
   artistAlbumSearch = spotify.artist_albums(artist["id"], album_type=None, country="US",limit=20,offset=0)
   artistAlbumSearch = artistAlbumSearch["items"]
   print(artistAlbumSearch)
   
   for albumData in artistAlbumSearch:
      Album(albumData)
   
   return 0

searchRequest("What artist are you interested in?", main)