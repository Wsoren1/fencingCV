#!/usr/bin/env python3

import tkinter as tk
import vlc
import platform
from PIL import Image
from PIL import ImageTk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

import sys
import glob
import pickle

def main(runDir):
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title('FencingCV - A Measurement Platform')

    # Create a Frame to act as the video container
    video_frame = tk.Frame(root, bg="black")
    video_frame.pack(fill=tk.BOTH, expand=True)


    fig = Figure(figsize=(14,6), dpi=70)

    t, left_pos, right_pos = pickle.load(open(f'{runDir}/twofencerposdata.p', 'rb'))

    ax = fig.add_subplot(111)
    ax.plot(t, left_pos, label='FOTL')
    ax.plot(t, right_pos, label='FOTR')
    ax.set_ylabel('Fencer Position (pixels from left)')
    ax.set_xlabel('Time (s)')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False)
    
    def on_key_press(event):
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect("key_press_event", on_key_press)


    # Initialize VLC player
    instance = vlc.Instance('--input-repeat=999999')
    player = instance.media_player_new()

    # Link VLC to the Tkinter Frame
    win_id = video_frame.winfo_id()
    player.set_xwindow(win_id)

    # Load media and play
    files = glob.glob(f'{runDir}/*.mp4')
    
    media = instance.media_new(files[0])

    player.set_media(media)
    player.play()
    global player_playing
    player_playing = True

    def on_play_pause_click(event=None):
        global player_playing
        if player_playing:
            player.pause()
        else:
            player.play()
        player_playing = not player_playing

    root.bind('<space>', on_play_pause_click)

    play_pause = tk.Button(video_frame, text='Play/Pause', command=on_play_pause_click)
    play_pause.pack(side='top')
    root.mainloop()

if __name__ == "__main__":

    main(sys.argv[1])
