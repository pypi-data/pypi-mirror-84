from pyetf.frames.main_page.right_frame import RightFrame
from pyetf.frames.main_page.left_frame import LeftFrame
from pyetf.functions import *
from tkinter import ttk


class MainPage:

    def __init__(self, app):
        self.app = app
        self.p = app.p

        self.central_frame = ttk.Frame(app.mainframe)

        self.left_frame = LeftFrame(app.mainframe, self)
        self.left_frame.grid(row=0, column=0, sticky=(W, N, S, E), padx=15)

        ttk.Separator(app.mainframe, orient=VERTICAL).grid(row=0, column=1, sticky='nswe')
        self.central_frame.grid(row=0, column=2, columnspan=5, sticky=(E, W, N, S), padx=15)

        ttk.Separator(app.mainframe, orient=VERTICAL).grid(row=0, column=7, sticky='nswe')

        self.right_frame = RightFrame(app.mainframe, self)
        self.right_frame.grid(row=0, column=8, columnspan=2, sticky=(E, N, S, W), padx=15)

        configure(app.mainframe, 1, 8)
        
        self.left_frame.last_day()

    def new_central_frame(self):
        """
        Creates a new central frame in order to be able to show new things on it.
        :reeturn ttk.Frame
        """
        self.central_frame.destroy()
        self.central_frame = ttk.Frame(self.app.mainframe)
        self.central_frame.grid(row=0, column=2, columnspan=5, sticky=(E, W, N, S), padx=15)
        return self.central_frame
