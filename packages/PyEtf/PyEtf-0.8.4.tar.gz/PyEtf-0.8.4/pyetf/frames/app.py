from tkinter import ttk
from tkinter import *
from tkinter import font
from pyetf.finance.portfolio import Portfolio
from pyetf.frames.main_page.main_page import MainPage
from pyetf.frames.vs_index.vs_index_page import VsIndexPage
from pyetf.frames.menu.menu_bar import MenuBar

class App:

    def __init__(self, root, infoFile, server):
        textFont = font.Font(family='Helvetica', name='TextFont', size=15)
        titleFont = font.Font(family='Helvetica', name='TitleFont', size=30)
        boldFont = font.Font(family='Helvetica', name='BoldFont', size=15)
        dateFont = font.Font(family='Helvetica', name='DateFont', size=17, weight='bold', slant='italic')
        numberFont = font.Font(family='Helvetica', name='NumberFont', size=15)
        numberFontS = font.Font(family='Helvetica', name='NumberFontS', size=12)
        numberFontBold = font.Font(family='Helvetica', name='NumberBoldFont', size=15, weight='bold')
        titleStyle = ttk.Style()
        titleStyle.configure('Title.TLabel', foreground='#0a4ac9', font=titleFont)
        titleStyle.configure('Head.TLabel',foreground='#2464e3', font=boldFont)
        titleStyle.configure('Text.TLabel', font=textFont)
        titleStyle.configure('Date.TLabel', foreground='#2464e3', font=dateFont)
        titleStyle.configure('Positive.TLabel', foreground='#0b7028', font=numberFont)
        titleStyle.configure('Zero.TLabel', font=numberFont)
        titleStyle.configure('Negative.TLabel', foreground='#bd0909', font=numberFont)
        titleStyle.configure('PositiveS.TLabel', foreground='#0b7028', font=numberFontS)
        titleStyle.configure('ZeroS.TLabel', font=numberFontS)
        titleStyle.configure('NegativeS.TLabel', foreground='#bd0909', font=numberFontS)
        titleStyle.configure('PositiveBold.TLabel', foreground='#0b7028', font=numberFontBold)
        titleStyle.configure('NegativeBold.TLabel', foreground='#bd0909', font=numberFontBold)

        self.server = server
        self.root = root
        self.p = Portfolio(infoFile, server)
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.curr_page = MainPage(self)

        MenuBar(self)
    
    def initial_page(self):
        """
        Functions that returns to the initial page.
        :return None 
        """
        self.curr_page = MainPage(self)

    def new_page(self):
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))