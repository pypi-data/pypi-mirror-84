#!/usr/bin/env python3

from tkinter import *
from pyetf.frames.app import App
import argparse

def main(file, server=False):
    root = Tk()
    root.title('Portfolio Manager by Dodo')
    root.geometry("1400x700+20+80")
    root.option_add('*tearOff', FALSE)
    try:
        img = PhotoImage(file='pyetf/frames/Icon.png')
        root.tk.call('wm', 'iconphoto', root._w, img)
    except:
        pass
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = App(root, file, server)
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Portafoglio Manager.')
    parser.add_argument('-f', '--file', type=str, required=False, default='Info.csv', help='Percorso per il file Info.csv del portafoglio')
    parser.add_argument('-s', '--server', required=False, action='store_true', help='Connect to server')
    args = parser.parse_args()
    main(args.file, args.server)