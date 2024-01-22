
import os
from time import sleep
from tkinter import font
from tkinter.constants import DISABLED
from tkinter.constants import NORMAL
import PlayMusic ##
import tkinter as tk
from tkinter import ttk
from threading import Thread
from PIL import Image
from PIL import ImageTk
from time import time

from tkinter.messagebox import showerror

try:
    os.makedirs('Music')    
except OSError as e:
    pass


class settings_data:
    firts_color = "#222222"
    second_color = "#222222"

    auto_minuature = False
    Muisc_path = "Music/"


class menu:

    def __init__(self) -> None:

        def Play_muisc_thread_maker(start_index: int):
            self.play_song.place_forget()
            self.pause_song.place(x=540, y=300)

            if self.random_play:
                pass
            else:
                hilo = Thread(target=PlayMusic.play_music, daemon=True, args=(
                    1, start_index, self.listbox, self.thumb, self,))
                hilo.start()

        def skip_l_button_command() -> None:
            if self.skip_timeout < time():
                if PlayMusic.current_song != None:
                    next_index = self.songs.index(PlayMusic.current_song) + 1
                else:
                    next_index = 1

                if next_index > len(self.songs)-1:
                    next_index = 0

                stop_song_command()
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(next_index)
                play_song_command(c_index=next_index)
                self.listbox.see(next_index)
                self.skip_timeout = time() + 0.5

        def skip_r_button_command() -> None:
            if self.skip_timeout < time():
                if PlayMusic.current_song != None:
                    next_index = self.songs.index(PlayMusic.current_song) - 1
                else:
                    next_index = len(self.songs)-1

                
                if next_index <= -1:
                    next_index = len(self.songs)-1

                print(next_index,len(self.songs))
                stop_song_command()
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(next_index)
                play_song_command(c_index=next_index)
                self.listbox.see(next_index)
                self.skip_timeout = time() + 0.5

        def stop_song_command() -> None:
            self.started = False
            self.kill_reproduct = True
            sleep(0.05)
            self.kill_reproduct = False
            self.play_song.place(x=540, y=300)
            self.pause_song.place_forget()

        def play_song_command(c_index: int = None) -> None:
            self.play_song.place_forget()
            self.pause_song.place(x=540, y=300)

            try:
                song_index = self.listbox.curselection()[0]
                if c_index != None:
                    song_index = c_index
            except Exception as p:
                print(p)
                song_index = 0
                self.listbox.selection_set(0)

            if self.started == False or PlayMusic.current_song != self.songs[song_index]:
                stop_song_command()
                Play_muisc_thread_maker(song_index)
                self.started = True
            else:
                PlayMusic.mixer.music.unpause()

        def pause_song_command() -> None:
            PlayMusic.mixer.music.pause()
            self.pause_song.place_forget()
            self.play_song.place(x=540, y=300)

        def list_update(e) -> None:
            if PlayMusic.mixer.music.get_busy() == 1:
                if PlayMusic.current_song != self.songs[self.listbox.curselection()[0]]:
                    self.started = False
                    self.kill_reproduct = True
                    sleep(0.1)
                    self.kill_reproduct = False
                    play_song_command()
                    #self.skip_timeout = time() + 0.01
                    self.listbox.config(state=tk.DISABLED)

        def list_update_2(e):
            self.root.update()
            sleep(0.05)
            self.listbox.config(state=tk.NORMAL)
            self.root.update()

        def lb_on_leave(e) -> None:
            self.listbox.itemconfig(self.late_post, bg="#333333")

        def lb_on_enter(event) -> None:
            index = self.listbox.index("@%s,%s" % (event.x, event.y))
            if index != self.late_post:
                self.listbox.itemconfig(index, bg="#4f4f4f")
                self.listbox.itemconfig(self.late_post, bg="#333333")
                self.late_post = index

        def settings():
            top_window = tk.Toplevel()
            top_window.geometry("300x300")
            top_window.configure(bg="#222222")
            top_window.resizable(False, False)

            def close_window(e=0):
                print(":D")
                sleep(1)
                top_window.destroy()

            def toggle_button_miniature():
                if settings_data.auto_minuature:
                    toggle_miniature.config(image=Toggle_off)
                    settings_data.auto_minuature = False
                else:
                    settings_data.auto_minuature = True
                    toggle_miniature.config(image=Toggle_on)

            Toggle_on = tk.PhotoImage(file="Asets/Toggle_on.png")
            Toggle_on = Toggle_on.subsample(6, 6)

            Toggle_off = tk.PhotoImage(file="Asets/Toggle_off.png")
            Toggle_off = Toggle_off.subsample(6, 6)

            top_window.protocol("WM_DELETE_WINDOW", close_window)

            if settings_data.auto_minuature:
                toggle_miniature = tk.Button(top_window, command=toggle_button_miniature, image=Toggle_on,
                                             borderwidth=0, background="#222222", activebackground="#222222")
            else:
                toggle_miniature = tk.Button(top_window, command=toggle_button_miniature, image=Toggle_off,
                                             borderwidth=0, background="#222222", activebackground="#222222")
                                             
            toggle_miniature.place(x=170, y=10)
            tk.Label(top_window, text="Auto Find Miniature ", background="#222222", 
                        font=("Arial CE", 11, "bold")).place(x=10, y=25)

        self.settings_data = settings_data
        self.current_song = PlayMusic.current_song
        self.random_play = False
        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#222222')
        self.root.title("Music Player")
        self.root.wm_attributes("-transparentcolor", '#111111')
        self.started = False
        self.kill_reproduct = False

        self.current_song_label = tk.Label(
            self.root, bg="#222222", text="", font=("Calibri", 16, "bold"))
        self.current_song_label.place(x=245, y=70)

        self.l = 0
        self.progres_style = ttk.Style()
        self.progres_style.theme_use("clam")
        self.progres_style.configure("red.Horizontal.TProgressbar", foreground='#5100ff',
                                     lightcolor="#5100ff", background='#5100ff',
                                     bordercolor="#5100ff", troughcolor="#222222", darkcolor="#5100ff")

        self.progress_song = ttk.Progressbar(self.root, orient="horizontal",
                                             length=390, mode="determinate", style="red.Horizontal.TProgressbar")
        self.progress_song.place(x=240, y=144, height=15)

        self.start_time_label = tk.Label(self.root, text="0:00", bg="#222222")
        self.start_time_label.place(x=238, y=123)

        self.end_time_label = tk.Label(self.root, text="0:00", bg="#222222")
        self.end_time_label.place(x=605, y=123)
        self.skip_timeout = 0

        image = Image.open("Asets/default.png")
        self.Thmb = ImageTk.PhotoImage(image.resize((190, 109)))

        #image = Image.open("Asets/default.png")
        #image = image.resize((190, 109), Image.ANTIALIAS)   
        #photo = PhotoImage(width=image.width, height=image.height)
        #photo.putdata(list(image.getdata()))


        self.thumb = tk.Label(self.root, image=self.Thmb,
                              background="#5100ff", borderwidth=2)
        self.thumb.place(x=20, y=45)
        self.songs = PlayMusic.songs
        self.listbox = tk.Listbox(self.root, bg="#333333", foreground="#e1ddeb",
                                  borderwidth=0, highlightbackground="#5100ff",
                                  selectbackground="#5100ff", selectforeground="#d6d6d6",
                                  activestyle="none", highlightthickness=1,
                                  selectborderwidth=0, highlightcolor="#5100ff")
        self.listbox.bind('<<ListboxSelect>>', list_update)
        self.listbox.bind('<ButtonRelease>', list_update_2)
        self.listbox.bind('<Motion>', lb_on_enter)
        self.listbox.bind("<Leave>", lb_on_leave)

        self.late_post = 0
        self.listbox.place(x=20, y=205, width=400, height=275)

        for l, i in enumerate(self.songs):
            self.listbox.insert(l, str(l+1)+". "+i)

        self.Play_image = tk.PhotoImage(file="Asets/Play.png")
        self.Play_image = self.Play_image.subsample(17, 17)

        self.Pause_image = tk.PhotoImage(file="Asets/Pause.png")
        self.Pause_image = self.Pause_image.subsample(17, 17)

        self.skip_l = tk.PhotoImage(file="Asets/Skip_left.png")
        self.skip_l = self.skip_l.subsample(17, 17)

        self.skip_r = tk.PhotoImage(file="Asets/Skip_right.png")
        self.skip_r = self.skip_r.subsample(17, 17)
        
        self.settings_image = tk.PhotoImage(file="Asets/Settings.png")
        self.settings_image = self.settings_image.subsample(20, 20)

        self.skip_l_button = tk.Button(self.root, image=self.skip_r, borderwidth=0, command=skip_l_button_command,
                                       background="#222222", activebackground="#222222")
        self.skip_l_button.place(x=580, y=300)

        self.skip_r_button = tk.Button(self.root, image=self.skip_l, borderwidth=0, command=skip_r_button_command,
                                       background="#222222", activebackground="#222222")
        self.skip_r_button.place(x=500, y=300)



        self.play_song = tk.Button(self.root, command=play_song_command, image=self.Play_image,
                                   borderwidth=0, background="#222222", activebackground="#222222")

        self.play_song.place(x=540, y=300)

        self.pause_song = tk.Button(self.root, command=pause_song_command, image=self.Pause_image,
                                    borderwidth=0, background="#222222", activebackground="#222222")

        self.settings_button = tk.Button(self.root, command=settings, image=self.settings_image,
                                         borderwidth=0, background="#222222", activebackground="#222222")

        self.settings_button.place(x=665, y=5)
        # elf.stop_song = tk.Button(self.root, command=stop_song_command, image=self.Stop_image,
        #                borderwidth=0, background="#222222", activebackground="#222222")

        #self.stop_song.place(x=540, y=300)

        PlayMusic.update(self.songs[0], self.thumb)
        self.listbox.selection_set(0)
        if len(self.songs[0]) > 40:
            self.current_song_label.config(
                text=self.songs[0].replace(".mp3", "")[:40]+" ...")
        else:
            self.current_song_label.config(
                text=self.songs[0].replace(".mp3", ""))

    def start(self) -> None:
        self.root.mainloop()
        print("Window Close")


try:  # try 1
    Window = menu()
    Window.start()

except Exception as e:
    showerror(title="ERROR", message="ERROR: "+str(e)+" --Try 1")
