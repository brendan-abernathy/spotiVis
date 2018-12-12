import spotipy
import spotipy.oauth2 as oauth2
import gui
import urllib3
http = urllib3.PoolManager()
import os
import random
from javazoom.jl.converter import Converter
convert = Converter()
from music import *

#purpose: gets the width of the computer screen the program is being displayed on
#arguments: none
#returns: screen width
def getScreenWidth():
  return gui.Toolkit.getDefaultToolkit().getScreenSize().width

#purpose: gets the height of the computer screen the program is being displayed on
#arguments: none
#returns: none
def getScreenHeight():
  return gui.Toolkit.getDefaultToolkit().getScreenSize().height

class AlbumTrack:
   def __init__(self,json):
      self.data = json
      self.name = json["name"]
      self.number = json["track_number"]
      self.trackID = json["id"]
      self.songURL = json["preview_url"]
   def __repr__(self):
      return str(self.name) + " " + str(self.trackID)

class Album:
   global window
   albums = []
   def __init__(self,json):
      path = os.path.dirname(os.path.realpath(__file__))
      self.data = json
      self.name = json["name"]
      maxNameLength = 17
      if(len(self.name)>maxNameLength):
         self.name = self.name[0:maxNameLength] + "..."
      self.nameLabel = gui.Label(self.name,gui.LEFT,gui.Color(255,255,255))
      self.nameLabel.setFont(gui.Font("Futura", gui.Font.ITALIC, 18))
      getImage(json["images"][1]["url"], "albumArtCache.jpg")
      self.art = gui.Icon(path + "/cache/albumArtCache.jpg",60)
      self.totalTracks = json["total_tracks"]
      self.releaseDate = str(json["release_date"])
      self.albumID = str(json["id"])
      self.albumTracksSearch = spotify.album_tracks(self.albumID, limit=50, offset=0)
      self.tracks = []
      for trackData in self.albumTracksSearch["items"]:
         newTrack = AlbumTrack(trackData)
         self.tracks.append(newTrack)
      self.aSample = None
      self.art.onMouseDown(self.previewSong)
      Album.albums.append(self)
      if(len(Album.albums)<=3):
         window.add(self.art,50,325+(len(Album.albums)-1)*75)
         window.add(self.nameLabel, 125, 350 +(len(Album.albums)-1)*75)
   
   def removeSelf(self):
      window.remove(self.art)
      window.remove(self.nameLabel)
      Album.albums.remove(self)
   
   def previewSong(self,x,y):
      path = os.path.dirname(os.path.realpath(__file__))
      if(self.aSample != None):
         if(self.aSample.isPlaying()):
            self.aSample.stop()
         else:
            getSong(random.choice(self.tracks).songURL, "previewCache.mp3")
            convert.convert(path + "/cache/previewCache.mp3", path + "/cache/previewCache.wav")
            self.aSample=AudioSample(path + "/cache/previewCache.wav")
            self.aSample.play()
      else:
         getSong(random.choice(self.tracks).songURL, "previewCache.mp3")
         convert.convert(path + "/cache/previewCache.mp3", path + "/cache/previewCache.wav")
         self.aSample=AudioSample(path + "/cache/previewCache.wav")
         self.aSample.play()
      
   #def update(self):
   
   #purpose: retrieve artist name 
   #arguments: self
   #returns: artist name as a string and the total artist tracks as a string
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

#purpose: take the image of the desired artist to input into the display
#argumentsL url, saveName
#returns: True or False
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

def getSong(url,saveName):
   getRequest = http.request('GET', url, preload_content=False)
   with open("./cache/" + saveName, 'wb') as out:
      while True:
         data = getRequest.read(16)
         if not data:
            return False
         out.write(data)
   getRequest.release_conn()
   return True

#purpose: returns the most popular artist in the search results based on the artistKey inputted by the user
#arguments: search
#returns: most popular artist
def getMostPopularArtist(search):
   if(len(search["artists"]["items"]) <= 0):
      window.close()
      return -1
   #Get the most popular artist
   popularArtist = search["artists"]["items"][0]
   return popularArtist

def main():
   global window, requestWindow, artistField, removables
   cleanup()
   requestWindow.close()
   searchButton = gui.Button("New Artist", searchRequest)
   window.add(searchButton, getScreenWidth()-155, 15)
   removables.append(searchButton)
   #Search for the artist on spotify
   searchName = artistField.getText()
   artistSearch = spotify.search(q='artist:' + searchName, type='artist')
   artist = getMostPopularArtist(artistSearch)
   
   
   #Get number of followers
   artistFollowers = str(artist["followers"]["total"])
   
   #Get their icon
   artistImageURL = str(artist["images"][0]["url"])
   
   #Pulls the image from the internet. Use this format for anything relating to downloading something from the internet.
   getImage(artistImageURL, "artistImageCache.jpg")
   
   path = os.path.dirname(os.path.realpath(__file__))
   
   artistName = str(artist["name"])
   maxNameLength = 16
   if(len(artistName)>maxNameLength):
      artistName = artistName[0:maxNameLength] + "..."
      
   followerCount = gui.Label("Followers: "+ artistFollowers, gui.LEFT, gui.Color(255, 255, 255))
   followerCount.setFont(gui.Font("Futura", gui.Font.ITALIC, 24))
   artistImage = gui.Icon(path + "/cache/artistImageCache.jpg",300)
   artistLabel = gui.Label(artistName, gui.LEFT, gui.Color(255, 255, 255))
   artistLabel.setFont(gui.Font("Futura", gui.Font.BOLD, 100))
   genreLabel = gui.Label("Genre: " + str(artist["genres"][0]).title(), gui.LEFT, gui.Color(255, 255, 255))
   genreLabel.setFont(gui.Font("Futura", gui.Font.ITALIC, 36))
   
   window.add(artistImage, getScreenWidth() - 350, 50)
   window.add(artistLabel, 50, 20)
   window.add(genreLabel, 50, 150)
   window.add(followerCount, 50, 215)
   removables.append(artistImage)
   removables.append(artistLabel)
   removables.append(genreLabel)
   removables.append(followerCount)
   
   albumLabel = gui.Label("Top Albums:", gui.LEFT, gui.Color(255, 255, 255))
   albumLabel.setFont(gui.Font("Futura", gui.Font.BOLD, 20))
   window.add(albumLabel, 50, 275)
   removables.append(albumLabel)
   
   spotifyLogo = gui.Icon(path + "/spotifyLogo.png", 100)
   window.add(spotifyLogo, 50, getScreenHeight() - 250)
   removables.append(spotifyLogo)
   
   #track search function - Patrick will comment

   #add label for top tracks
   relatedArtistLabel = "Related Artists:"
   relatedLabel = gui.Label(relatedArtistLabel, gui.LEFT, gui.Color(255, 255, 255))
   relatedLabel.setFont(gui.Font("Futura", gui.Font.BOLD, 28))
   window.add(relatedLabel, getScreenWidth() - 550, 525)
   removables.append(relatedLabel)
   relatedArtistSearch = spotify.artist_related_artists(artist["id"])
   relatedArtistSearch = relatedArtistSearch["artists"]
   relatedArtists = []
   relatedArtistCount = None
   for relatedArtist in relatedArtistSearch:
      relatedArtists.append(relatedArtist)
   if(len(relatedArtists) >= 5):
         artistCount = 5
   else:
      artistCount = len(relatedArtists)
   for i in range(artistCount):
      getImage(relatedArtists[i]["images"][0]["url"],"relatedArtistCache.jpg")
      relatedArtistIcon = gui.Icon(path + "/cache/relatedArtistCache.jpg",100)
      window.add(relatedArtistIcon, getScreenWidth() - 225 - i*125, 625)
      removables.append(relatedArtistIcon)
      relatedArtistName = relatedArtists[i]["name"]
      maxNameLength = 10
      if(len(relatedArtistName)>maxNameLength):
         relatedArtistName = relatedArtistName[0:maxNameLength] + "..."
      relatedArtistNameLabel = gui.Label(relatedArtistName, gui.LEFT, gui.Color(255, 255, 255))
      window.add(relatedArtistNameLabel, getScreenWidth() - 225 - i*125, 600)
      removables.append(relatedArtistNameLabel)
   
   topTrackLabel="Top Tracks:"
   topLabel=gui.Label(topTrackLabel,gui.LEFT,gui.Color(255,255,255))
   topLabel.setFont(gui.Font("Futura",gui.Font.BOLD,20))
   window.add(topLabel, getScreenWidth()-1050, 275)
   removables.append(topLabel)
   #Use the spotipy function to get JSON data for the artist's top tracks
   artistTrackSearch=spotify.artist_top_tracks(artist["id"],country='US')
   artistTracks=[]
   trackCount=None
   #Append all of the artist's top tracks to the list artistTracks
   for i in artistTrackSearch['tracks']:
      track= i
      artistTracks.append(i)
   #This loop is a safety in case the artist has less than 5 tracks released
   #Sets the number of tracks displayed to 5 unless there are less than 5, then set it to that number
   if(len(artistTracks)>=5):
      trackCount=5
   else:
      trackCount= len(artistTracks)
   #Incorporates GUI elemnts
   for i in range(trackCount):
      #pulls individual track names from the list artistTracks and gives them a number based on popularity
      trackName=str(i+1) + ". " + artistTracks[i]['name']
      maxNameLength = 25
      if(len(trackName)>maxNameLength):
         trackName = trackName[0:maxNameLength] + "..."
      trackNameLabel = gui.Label(trackName,gui.RIGHT,gui.Color(255,255,255))
      trackNameLabel.setFont(gui.Font("Futura", gui.Font.ITALIC, 20))
      window.add(trackNameLabel, getScreenWidth()-1050, 325 +i*50)
      removables.append(trackNameLabel)
   
            
   artistAlbumSearch = spotify.artist_albums(artist["id"], album_type=None, country="US",limit=20,offset=0)
   artistAlbumSearch = artistAlbumSearch["items"]
   #print(artistAlbumSearch)
   
   for albumData in artistAlbumSearch:
      Album(albumData)
   
   return 0

def cleanup():
   global removables, window
   for removable in removables:
      window.remove(removable)
   for i in range(len(Album.albums)):
      Album.albums[0].removeSelf()
   

#purpose: set up the initial window asking for the user to input the desired artist
#arguments: message, arbitraryFunction
#returns: none
def searchRequest(message="What artist are you interested in?", arbitraryFunction=main):
   global requestWindow, artistField
   requestWindow = gui.Display("Choose Artist",300,100,(getScreenWidth()/2)-150, (getScreenHeight()/2)-100)
   requestWindow.add(gui.Label(message), 25, 15)
   artistField = gui.TextField("What Artist?", 8)
   requestWindow.add(artistField, 25, 40)
   okButton = gui.Button("OK", arbitraryFunction)
   requestWindow.add(okButton, 215, 60)

searchRequest("What artist are you interested in?", main)
