#!/usr/bin/env python3

import tkinter as tk
import vlc
import platform
from PIL import Image
from PIL import ImageTk

root = tk.Tk()
root.geometry("1920x1080")
root.title('FencingCV - A Measurement Platform by Karina')

# Create a Frame to act as the video container
video_frame = tk.Frame(root, bg="black")
video_frame.pack(fill=tk.BOTH, expand=True)



img = Image.open('figure.png')
img = img.resize((1920, int(1080/3)))
photo_img = ImageTk.PhotoImage(img)
label = tk.Label(root, image=photo_img)
label.pack(side="bottom")

# Initialize VLC player
instance = vlc.Instance('--input-repeat=999999')
player = instance.media_player_new()

# Link VLC to the Tkinter Frame
win_id = video_frame.winfo_id()
if platform.system() == "Windows":
    player.set_hwnd(win_id)
else:
    player.set_xwindow(win_id)

# Load media and play
media = instance.media_new("annotated_monday_practice.mp4") # Can be a local path or URL

player.set_media(media)
player.play()
player_playing = True

def on_play_pause_click(event):
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
