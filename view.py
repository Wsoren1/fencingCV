#!/usr/bin/env python3

import tkinter as tk
import vlc
import platform

root = tk.Tk()
root.geometry("1920x1080")

# Create a Frame to act as the video container
video_frame = tk.Frame(root, bg="black")
video_frame.pack(fill=tk.BOTH, expand=True)

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
media = instance.media_new("annotated_thoughtfulScallopsNguniCattle.mp4") # Can be a local path or URL

player.set_media(media)
player.play()

root.mainloop()
