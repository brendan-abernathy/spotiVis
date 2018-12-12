import spotipy
import spotipy.oauth2 as oauth2
import gui
import urllib3
#Needed for http access.
http = urllib3.PoolManager()
import os
import random
from javazoom.jl.converter import Converter
#Needed to convert MP3 files to .wav files.
jlConverter = Converter()
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

#AlbumTrack: Contains and stores data on tracks inside an album.
class AlbumTrack:
   #__init__: Initializes the AlbumTrack object and parses the JSON for necessary data, such as song name and number.
   #Arguments: json, type Dictionary: The JSON data output from the Spotify API for the track.
   #Returns: type AlbumTrack: The AlbumTrack object.
   def __init__(self,json):
      self.data = json
      self.name = json["name"]
      self.number = json["track_number"]
      self.trackID = json["id"]
      self.songURL = json["preview_url"]
   
   #__repr__: Defines what is printed when someone attempts to print an AlbumTrack object, used for debugging.
   #Arguments: None
   #Returns: type String: The name of the song, plus its Spotify ID.
   def __repr__(self):
      return str(self.name) + " " + str(self.trackID)

class Album:
   global window
   #Keep a class-scoped instance of all initialized Album objects.
   albums = []
   
   #__init__: Initializes the Album object and parses the JSON for necessary data, such as album name and tracklist.
   #Arguments: json, type Dictionary: The JSON data output from the Spotify API for the track.
   #Returns: type Album: The Album object.
   def __init__(self,json):
      #For convenience
      path = os.path.dirname(os.path.realpath(__file__))
      #Keep references to all important information
      self.data = json
      self.name = json["name"]
      #Limit the length of the artist name.
      maxNameLength = 17
      if(len(self.name)>maxNameLength):
         self.name = self.name[0:maxNameLength] + "..."
      #Create the labels for use later
      self.nameLabel = gui.Label(self.name,gui.LEFT,gui.Color(255,255,255))
      self.nameLabel.setFont(gui.Font("Futura", gui.Font.ITALIC, 18))
      #Download and create an icon for the album art.
      getImage(json["images"][1]["url"], "albumArtCache.jpg")
      self.art = gui.Icon(path + "/cache/albumArtCache.jpg",60)
      self.totalTracks = json["total_tracks"]
      self.releaseDate = str(json["release_date"])
      self.albumID = str(json["id"])
      #Search and store the entire tracklist of the album.
      self.albumTracksSearch = spotify.album_tracks(self.albumID, limit=50, offset=0)
      self.tracks = []
      for trackData in self.albumTracksSearch["items"]:
         newTrack = AlbumTrack(trackData)
         self.tracks.append(newTrack)
      #Create an empty space for an AudioSample to go in later.
      self.aSample = None
      #Set up an event handler to the method previewSong.
      self.art.onMouseDown(self.previewSong)
      #Keep a reference to this object in the class.
      Album.albums.append(self)
      #Make sure we display only 3 albums.
      if(len(Album.albums)<=3):
         #Display the album!
         window.add(self.art,50,325+(len(Album.albums)-1)*75)
         window.add(self.nameLabel, 125, 350 +(len(Album.albums)-1)*75)
   
   #removeSelf: Cleans up the displayed form of the album and deletes the reference to it.
   #Arguments: None
   #Returns: None
   def removeSelf(self):
      window.remove(self.art)
      window.remove(self.nameLabel)
      Album.albums.remove(self)
   
   #previewSong: Downloads, converts, and plays a 30 second sample of a random song on the album.
   #Arguments: x,y: The x and y location of the click, unused.
   #Returns: None
   def previewSong(self,x,y):
      #For convenience
      path = os.path.dirname(os.path.realpath(__file__))
      if(self.aSample != None):
         if(self.aSample.isPlaying()):
            #If we're already playing the song, stop playing instead.
            self.aSample.stop()
         else:
            #Download a random song and use jLayer to convert it to wav
            getSong(random.choice(self.tracks).songURL, "previewCache.mp3")
            jlConverter.convert(path + "/cache/previewCache.mp3", path + "/cache/previewCache.wav")
            #Load and play the song using jythonMusic
            self.aSample=AudioSample(path + "/cache/previewCache.wav")
            self.aSample.play()
      else:
         #Download a random song and use jLayer to convert it to wav
         getSong(random.choice(self.tracks).songURL, "previewCache.mp3")
         convert.convert(path + "/cache/previewCache.mp3", path + "/cache/previewCache.wav")
         #Load and play the song using jythonMusic
         self.aSample=AudioSample(path + "/cache/previewCache.wav")
         self.aSample.play()

   #__repr__: Defines what is printed when someone attempts to print an Album object, used for debugging.
   #Arguments: None
   #Returns: type String: The name of the album, plus its Spotify ID.
   def __repr__(self):
      return str(self.name) + " " + str(self.albumID)

#The Spotify API client ID and secret.
client_id = "7660f65e20dc492fa7a784d5a8118d51"
client_secret = "4577008c88a84b2b83a072533ec7780a"

#Define an oauth2 compatible credential set to pass to the Spotify API.
credentials = oauth2.SpotifyClientCredentials(
        client_id=client_id,  
        client_secret=client_secret)

#Use the credentials to generate an access token, then use that token to initialize and authorize a new spotipy.Spotify object.
token = credentials.get_access_token()
spotify = spotipy.Spotify(auth=token)

#Initialize global variables.
window = None
requestWindow = None
artistField = None
removables = []

#getImage: Download the image of the desired artist to input into the display
#Arguments: url, The URL of the image to download. saveName, The name the file should be cached as.
#Returns: type Boolean, Returns true if the download is successful, false if it doesn't.
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

#getSong: Download the song of the desired artist to input into the display
#Arguments: url, The URL of the song to download. saveName, The name the file should be cached as.
#Returns: type Boolean, Returns true if the download is successful, false if it doesn't.
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

#getMostPopularArtist: Returns the most popular artist in the search results based on the artistKey inputted by the user.
#Arguments: search, The dictionary returned by the Spotify API.
#Returns: type Dictionary, The data on the most popular artist.
def getMostPopularArtist(search):
   if(len(search["artists"]["items"]) <= 0):
      window.close()
      return -1
   #Get the most popular artist
   popularArtist = search["artists"]["items"][0]
   return popularArtist

def main():
   global window, requestWindow, artistField, removables
   if(window == None):
      window = gui.Display("spotiVis", getScreenWidth(), getScreenHeight(),0,0, gui.Color(60,60,60))
   #Run cleanup first, to make sure we have a clean slate to display on.
   cleanup()
   #Close the request window, the user shouldn't be asked to search once they already have!
   requestWindow.close()
   
   #Add a search button for future searches.
   searchButton = gui.Button("New Artist", searchRequest)
   window.add(searchButton, getScreenWidth()-155, 15)
   removables.append(searchButton)
   #Search for the artist on spotify
   searchName = artistField.getText()
   artistSearch = spotify.search(q='artist:' + searchName, type='artist')
   #If there aren't any results, start over!
   if(getMostPopularArtist(artistSearch) == -1):
      window = None
      searchRequest("That artist returned no results!", main)
      return -1
   artist = getMostPopularArtist(artistSearch)
   
   #Get number of followers
   artistFollowers = str(artist["followers"]["total"])
   
   #Get their icon
   artistImageURL = str(artist["images"][0]["url"])
   
   #Pulls the image from the internet. 
   getImage(artistImageURL, "artistImageCache.jpg")
   path = os.path.dirname(os.path.realpath(__file__))
   
   #Shorten the artists name if it happens to be too long
   artistName = str(artist["name"])
   maxNameLength = 15
   if(len(artistName)>maxNameLength):
      artistName = artistName[0:maxNameLength] + "..."
   
   #Add all static information to the window
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

   relatedArtistLabel = "Related Artists:"
   relatedLabel = gui.Label(relatedArtistLabel, gui.LEFT, gui.Color(255, 255, 255))
   relatedLabel.setFont(gui.Font("Futura", gui.Font.BOLD, 28))
   window.add(relatedLabel, getScreenWidth() - 550, 525)
   removables.append(relatedLabel)
   
   topTrackLabel="Top Tracks:"
   topLabel=gui.Label(topTrackLabel,gui.LEFT,gui.Color(255,255,255))
   topLabel.setFont(gui.Font("Futura",gui.Font.BOLD,20))
   window.add(topLabel, getScreenWidth()-1050, 275)
   removables.append(topLabel)
   
   #Find related artists from Spotify API
   relatedArtistSearch = spotify.artist_related_artists(artist["id"])
   relatedArtistSearch = relatedArtistSearch["artists"]
   relatedArtists = []
   #Only ever display 5 related artists, but allow fewer too.
   relatedArtistCount = None
   for relatedArtist in relatedArtistSearch:
      relatedArtists.append(relatedArtist)
   if(len(relatedArtists) >= 5):
         artistCount = 5
   else:
      artistCount = len(relatedArtists)
   #Display each related artist in a line, as well as their pictures.
   for i in range(artistCount):
      getImage(relatedArtists[i]["images"][0]["url"],"relatedArtistCache.jpg")
      relatedArtistIcon = gui.Icon(path + "/cache/relatedArtistCache.jpg",100)
      window.add(relatedArtistIcon, getScreenWidth() - 225 - i*125, 625)
      removables.append(relatedArtistIcon)
      relatedArtistName = relatedArtists[i]["name"]
      #Limit the length of the related artist name.
      maxNameLength = 10
      if(len(relatedArtistName)>maxNameLength):
         relatedArtistName = relatedArtistName[0:maxNameLength] + "..."
      relatedArtistNameLabel = gui.Label(relatedArtistName, gui.LEFT, gui.Color(255, 255, 255))
      window.add(relatedArtistNameLabel, getScreenWidth() - 225 - i*125, 600)
      removables.append(relatedArtistNameLabel)
   
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
   
   
   #Get the artists most recent albums in order.  
   artistAlbumSearch = spotify.artist_albums(artist["id"], album_type=None, country="US",limit=20,offset=0)
   artistAlbumSearch = artistAlbumSearch["items"]
   
   #Create a new Album object for each of these albums.
   for albumData in artistAlbumSearch:
      Album(albumData)
   
   #Return 0 if we are successful!
   return 0

#cleanup: Clean up the main window to keep everything clear for the next search.
#Arguments: None
#Returns: None
def cleanup():
   global removables, window
   #As long as the window exists, delete everything from the window.
   if(window!=None):
      for removable in removables:
         window.remove(removable)
   #Get every album to remove itself from the window, and delete its own reference.
   for i in range(len(Album.albums)):
      Album.albums[0].removeSelf()
   

#searchRequest: Set up the initial window asking for the user to input the desired artist
#Arguments: message, The message asked to the user. arbitraryFunction, The funtion to be called after acquiring user input.
#Returns: none
def searchRequest(message="What artist are you interested in?", arbitraryFunction=main):
   global requestWindow, artistField
   requestWindow = gui.Display("Choose Artist",300,100,(getScreenWidth()/2)-150, (getScreenHeight()/2)-100)
   requestWindow.add(gui.Label(message), 25, 15)
   artistField = gui.TextField("What Artist?", 8)
   requestWindow.add(artistField, 25, 40)
   okButton = gui.Button("OK", arbitraryFunction)
   requestWindow.add(okButton, 215, 60)

#Set it all off!
searchRequest("What artist are you interested in?", main)
