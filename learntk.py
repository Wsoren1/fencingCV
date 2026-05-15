#!/usr/bin/env python3

import tkinter as tk

root = tk.Tk()
root.title('FencingCV - A Measurement Platform by Karina')

lbl = tk.Label(root, text="label 1")
lbl.grid(row = 0, column = 0)

def on_click():
    lbl.config(text='button clicked')

    
btn = tk.Button(root, text='button1', command=on_click)
btn.grid(row = 0, column = 1)


root.mainloop()

