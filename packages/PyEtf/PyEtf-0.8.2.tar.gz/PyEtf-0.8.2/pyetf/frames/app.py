from tkinter import ttk
from tkinter import filedialog
from tkinter import font
from pyetf.finance.portfolio import Portfolio
from pyetf.frames.right_frame import RightFrame
from pyetf.frames.left_frame import LeftFrame
from pyetf.functions import *

class App:

    def __init__(self, root, infoFile):
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

        self.p = Portfolio(infoFile)
        self.mainframe = ttk.Frame(root)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))


        self.central_frame = ttk.Frame(self.mainframe)

        self.left_frame = LeftFrame(self.mainframe, self)
        self.left_frame.grid(row=0, column=0, sticky=(W, N, S, E), padx=15)

        ttk.Separator(self.mainframe, orient=VERTICAL).grid(row=0, column=1, sticky='nswe')
        self.central_frame.grid(row=0, column=2, columnspan=5, sticky=(E, W, N, S), padx=15)

        ttk.Separator(self.mainframe, orient=VERTICAL).grid(row=0, column=7, sticky='nswe')

        self.right_frame = RightFrame(self.mainframe, self)
        self.right_frame.grid(row=0, column=8, columnspan=2, sticky=(E, N, S, W), padx=15)

        self.menu = Menu(root)
        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(menu=self.fileMenu, label='File')
        self.fileMenu.add_command(label='Open...', command=self.openFile)
        root['menu'] = self.menu

        configure(self.mainframe, 1, 8)
        
        self.left_frame.last_day()

    def new_central_frame(self):
        """
        Creates a new central frame in order to be able to show new things on it.
        :reeturn ttk.Frame
        """
        self.central_frame.destroy()
        self.central_frame = ttk.Frame(self.mainframe)
        self.central_frame.grid(row=0, column=2, columnspan=5, sticky=(E, W, N, S), padx=15)
        return self.central_frame
    
    def openFile(self):
        """
        Change the Info file for the portfolio.
        :return None
        """
        filename = filedialog.askopenfilename()
        self.p = Portfolio(filename)
        self.left_frame.p = self.p
        self.right_frame.p = self.p
        self.right_frame.etf_list.p = self.p
        self.right_frame.etf_list.refresh()
        self.right_frame.add_etf.p = self.p
        self.right_frame.sell_etf.p = self.p
        self.left_frame.last_day()