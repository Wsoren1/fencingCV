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
from matplotlib.animation import FuncAnimation

import numpy as np

import sys
import glob
import pickle
import time
import csv
import os
user_is_typing = False

def main(runDir):
    root = tk.Tk()
    root.geometry("1920x1080")
    root.title('FencingCV - A Measurement Platform')

    # Create a Frame to act as the video container
    video_frame = tk.Frame(root, bg="black")
    video_frame.pack(fill=tk.BOTH, expand=True)

    fig = Figure(figsize=(14,6), dpi=70)

    t, left_pos, right_pos = pickle.load(open(f'{runDir}/twofencerposdata.p', 'rb'))
    
    
    ax = fig.add_subplot(211)
    ax.plot(t, left_pos, label='FOTL')
    ax.plot(t, right_pos, label='FOTR')
    ax.legend()
    ax.set_ylabel('Fencer Position (pixels from left)')
    ax.set_xlabel('Time (s)')
    
    t, left_extension, right_extension = pickle.load(open(f'{runDir}/extensiondata.p', 'rb'))
    ax2 = fig.add_subplot(212)
    ax2.plot(t, left_extension, label='FOTL')
    ax2.plot(t, right_extension, label='FOTR')
    ax2.legend()
    ax2.set_ylabel('P(Extension) of Fencer')
    ax2.set_xlabel('Time (s)')

    
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
    media.add_option(":avcodec-hw=none")

    player.set_media(media)
    player.play()

    def draw_vline(ax):
        v_line1 = ax.axvline(x=player.get_time()/1000, color='red', linestyle='--')
        v_line2 = ax2.axvline(x=player.get_time()/1000, color='red', linestyle='--')
        canvas.draw()
        v_line1.remove()
        v_line2.remove()
 
    
    def on_play_pause_click(event=None):
        global user_is_typing
        if user_is_typing:
            return
        player.pause()

    def frame_scrub_back(ax):
        global user_is_typing
        if user_is_typing:
            return
        player.set_pause(1)
        fps = player.get_fps() or 25.0
        mspf = int(1000 // fps)

        current_time = player.get_time()
        player.set_time(current_time - mspf)

        draw_vline(ax)
        
    def frame_scrub_forward(ax):
        global user_is_typing
        if user_is_typing:
            return
        player.set_pause(1)
        fps = player.get_fps() or 25.0  
        mspf = int(1000 // fps)
    
        current_time = player.get_time()
        player.set_time(current_time + mspf)
        draw_vline(ax)
        
    root.bind('<comma>', lambda x : frame_scrub_back(ax))
    root.bind('<period>', lambda x : frame_scrub_forward(ax))
    root.bind('<space>', on_play_pause_click)
    root.bind('<m>', lambda x : handle_mark(time_check))

    # play_pause = tk.Button(video_frame, text='Play/Pause', command=on_play_pause_click)
    # play_pause.pack(side='bottom')

    def scale_scrub(value, ax):
        player.set_pause(1)
        player.set_position(int(value)/1000)

        draw_vline(ax)
        
    scrubber_val = tk.IntVar(value=0)
    scrubber = tk.Scale(video_frame, variable = scrubber_val, from_=0, to=1000, orient=tk.HORIZONTAL, command=lambda event : scale_scrub(event, ax))
    scrubber.pack(side='bottom', fill=tk.BOTH)

    
    time_table = tk.Frame(video_frame)

    time_table_title = tk.Label(time_table, text='Time Table (\'m\' to mark durations)')
    time_table_title.grid(row=0, column=0, columnspan=3)
    
    time_1 = tk.Label(time_table, text='t1')
    time_2 = tk.Label(time_table, text='t2')

    time_1_v = tk.Label(time_table, text='00:00:000')
    time_2_v = tk.Label(time_table, text='00:00:000')

    time_1.grid(row=1, column=1)
    time_2.grid(row=1, column=2)
    time_1_v.grid(row=2, column=1)
    time_2_v.grid(row=2, column=2)

    duration_label = tk.Label(time_table, text='Duration:')
    duration_value = tk.Label(time_table, text='00:00:000')

    duration_label.grid(row=3, column=1)
    duration_value.grid(row=3, column=2)

    def on_focus_in(event):
        global user_is_typing
        user_is_typing = True

    def on_focus_out(event):
        global user_is_typing
        user_is_typing = False

    note_label = tk.Label(time_table, text='Note:')
    note_label.grid(row=4)
    note_entry = tk.Entry(time_table)
    note_entry.grid(row=4, column=1, columnspan=2)

    note_entry.bind("<FocusIn>", on_focus_in)
    note_entry.bind("<FocusOut>", on_focus_out)

    time_check = [-1, -1]

    def format_ms(ms):
        seconds, milliseconds = divmod(ms, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    def handle_mark(time_check):
        global user_is_typing
        if user_is_typing:
            return

        t1 = time_check[0]
        t2 = time_check[1]
        
        if time_check[0] != -1 and time_check[1] != -1:
            time_check[0] = -1
            time_check[1] = -1
            time_1_v.config(text='00:00:000')
            time_2_v.config(text='00:00:000')
            duration_value.config(text='00:00:000')
        
        if time_check[0] == -1:
            time_check[0] = player.get_time()
            time_1_v.config(text=format_ms(time_check[0]))
            return
        else:
            time_check[1] = player.get_time()
            time_2_v.config(text=format_ms(time_check[1]))
            duration_value.config(text=format_ms(time_check[1] - time_check[0]))
            return

        return

    def write_times_to_file(times):
       root.focus_set()
       if not os.path.isfile(f'{runDir}/user_review_data.csv'):
           with open(f'{runDir}/user_review_data.csv', 'w') as f:
               writer = csv.writer(f)
               writer.writerow(['Start', 'End', 'Duration', 'Note'])

       with open(f'{runDir}/user_review_data.csv', 'a', newline='') as f:
           writer = csv.writer(f)

           writer.writerow([times[0], times[1], times[1] - times[0], note_entry.get()])


    save_button = tk.Button(time_table, text='Save', command=lambda : write_times_to_file(time_check))
    save_button.grid(row=5, column=1, columnspan=3)

    time_table.pack(side='right')


    def update_scrubber(value, ax):
        draw_vline(ax)
        scrubber_val.set(player.get_position() * 1000)
        
    player.event_manager().event_attach(vlc.EventType.MediaPlayerTimeChanged, update_scrubber, ax)

        
    root.mainloop()

if __name__ == "__main__":

    main(sys.argv[1])
