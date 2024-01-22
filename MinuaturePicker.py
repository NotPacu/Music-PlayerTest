import requests
from PIL import Image , ImageTk
import io
from youtube_search import YoutubeSearch
from json import loads
import PlayMusic
import eyed3
from youtubesearchpython import VideosSearch
from time import sleep

"""
def ImageSong(song,labeltk=None):
    PlayMusic.current_updates += 1
    mp3 = stagger.read_tag("Music/"+song)
    
    if mp3.picture != "":
        try:
            by_data = mp3[stagger.id3.APIC][0].data
            im = io.BytesIO(by_data)
            image = Image.open(im)
            Thmb = ImageTk.PhotoImage(image.resize((190,109)))
            labeltk.configure(image=Thmb)
            labeltk.image = Thmb
        except:
            image = Image.open("Asets/default.png")
            Thmb = ImageTk.PhotoImage(image.resize((190,109)))
            labeltk.configure(image=Thmb)
            labeltk.image = Thmb
    else:
        try:
            song = song.replace(".mp3","")
            videosSearch = YoutubeSearch(song+" song", max_results=1).to_json()
            
            videosSearch = loads(videosSearch)["videos"][0]['thumbnails'][0]
            print(videosSearch,song)
            img = requests.get(videosSearch,timeout=2).content
            image = Image.open(io.BytesIO(img))
            Thmb = ImageTk.PhotoImage(image.resize((190,109)))
            labeltk.configure(image=Thmb)
            labeltk.image = Thmb
        except Exception as e:
            print(e)
            image = Image.open("Asets/default.png")
            Thmb = ImageTk.PhotoImage(image.resize((190,109)))
            labeltk.configure(image=Thmb)
            labeltk.image = Thmb
    PlayMusic.current_updates -= 1


    
"""
def ImageSong(song, labeltk=None):
    PlayMusic.current_updates += 1
    
    audiofile = eyed3.load("Music/" + song)
    
    if audiofile.tag and audiofile.tag.images:
        try:
            by_data = audiofile.tag.images[0].image_data
            im = io.BytesIO(by_data)
            image = Image.open(im)
            Thmb = ImageTk.PhotoImage(image.resize((190, 109)))
            labeltk.configure(image=Thmb)
            labeltk.image = Thmb
        except Exception as e:
            print(e)
            # Handle exception as needed
    else:
        try:
            song = song.replace(".mp3", "")
            videosSearch = VideosSearch(song + " song", max_results=1)
            video_data = videosSearch.result()["result"][0]["thumbnails"][0]
            img = requests.get(video_data["url"], timeout=2).content
            image = Image.open(io.BytesIO(img))
            Thmb = ImageTk.PhotoImage(image.resize((190, 109)))
            labeltk.configure(image=Thmb)
            labeltk.image = Thmb
        except Exception as e:
            print(e)
            # Handle exception as needed
            image = Image.open("Asets/default.png")
            Thmb = ImageTk.PhotoImage(image.resize((190, 109)))
            labeltk.configure(image=Thmb)
            labeltk.image = Thmb

    PlayMusic.current_updates -= 1