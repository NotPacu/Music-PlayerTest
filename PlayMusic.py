import random
from tkinter.constants import END
from tkinter.constants import NO
from pygame import mixer
from os import listdir
from time import sleep
from tkinter.messagebox import showerror
from MinuaturePicker import ImageSong ##
from threading import Thread
from mutagen.mp3 import MP3


mixer.init()
songs = listdir("Music/")
current_song = None
Max_time = None
current_updates = 0


def update(song: str, label: object) -> None:
    hilo = Thread(target=ImageSong, daemon=True, args=(song, label))
    hilo.start()


def play_music(mode: int = 1, start_index: int = -1, listbox: object = None, label: object = None, par: object = False):
    global Max_time
    global current_song

    if label == None:
        showerror(title="ERROR", message="ERROR: Label is None type")
        raise "ERROR: Label  is None type"

    elif listbox == None:
        showerror(title="ERROR", message="ERROR: Listbox is None type")
        raise "ERROR: Listbox  is None type"

    elif start_index > len(songs)-1:
        showerror(title="ERROR", message="ERROR: Start index is than song range")
        raise "ERROR: Start index is more than song range"
    
    
    elif start_index > -1:
        try:
            current_song = songs[start_index]
            update(current_song, label)
            Max_time = MP3("Music/"+current_song).info.length

            mixer.music.load("Music/"+current_song)
            mixer.music.play()
            if (Max_time%60)+1 >= 10:
                par.end_time_label.config(text=str(int(Max_time/60))+":"+str(int(Max_time%60)+1))
            else:
                par.end_time_label.config(text=str(int(Max_time/60))+":0"+str(int(Max_time%60)+1))
            print(current_song,Max_time)
            if len(current_song) > 40:
                par.current_song_label.config(text=current_song.replace(".mp3","")[:40]+" ...")
            else:
                par.current_song_label.config(text=current_song.replace(".mp3",""))
            
            par.progress_song['value'] = 0

            while mixer.music.get_pos() != -1:

                if par.kill_reproduct == True:
                    mixer.music.stop()
                    par.progress_song['value'] = 0
                    return None

                par.progress_song['value'] = (
                    mixer.music.get_pos()/1000) / Max_time * 100 + 1
                
                sleep(0.05)
        except Exception as p:
            showerror(title="ERROR",message="ERROR: "+str(p)+" Try -- 2")

    if mode == 1:
        start_index += 1

        if start_index >= len(songs):
            start_index = 0

        while True:
            for i in songs[start_index:]:
                try:
                    par.progress_song['value'] = 0
                    index = songs.index(i)
                    current_song = i

                    listbox.selection_clear(0, END)
                    listbox.selection_set(index)

                    update(current_song, label)
                    mixer.music.load("Music/"+i)
                    mixer.music.play()

                    print(i)
                    Max_time = MP3("Music/"+current_song).info.length
                    if (Max_time%60) + 1 >= 10:
                        par.end_time_label.config(text=str(int(Max_time/60))+":"+str(int(Max_time%60)+1))
                    else:
                        par.end_time_label.config(text=str(int(Max_time/60))+":0"+str(int(Max_time%60)+1))
                    if len(i) > 40:
                        par.current_song_label.config(text=i.replace(".mp3","")[:40]+" ...")
                    else:
                        par.current_song_label.config(text=i.replace(".mp3",""))

                    while mixer.music.get_pos() != -1:

                        if par.kill_reproduct == True:
                            mixer.music.stop()
                            par.progress_song['value'] = 0
                            return None
                        par.progress_song['value'] = (
                            mixer.music.get_pos()/1000) / Max_time * 100 + 1
                        sleep(0.05)
                except Exception as p:
                    showerror(title="ERROR",message="ERROR: "+str(p)+" Try -- 3")
            start_index = 0

    elif mode == 2:
        selectec = random.choice(songs)

        if start_index > -1:
            selectec_ = random.choice(songs)

            while selectec == selectec_:
                selectec_ = random.choice(songs)
            selectec = selectec_

        while True:
            current_song = (songs.index(selectec))
            update(current_song, label)

            mixer.music.load("Music/"+selectec)
            mixer.music.play()

            print(selectec)

            while mixer.music.get_pos() != -1:

                if par.kill_reproduct == True:
                    mixer.music.stop()
                    return None
                sleep(0.05)

            selectec_ = random.choice(songs)

            while selectec == selectec_:
                selectec_ = random.choice(songs)

            selectec = selectec_
            
    else:
        showerror(title="ERROR",message="ERROR: Mode "+str(mode)+"  Start_index: "+str(start_index))