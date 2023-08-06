from tkinter import *
from tkinter import filedialog
from pyetf.finance.portfolio import Portfolio
from pyetf.frames.vs_index.vs_index_page import VsIndexPage
from tkinter import ttk


class MenuBar:
    """Class representing the menu bar and rredirecting to the different pages"""

    def __init__(self, app):
        """
        Initialization of the menu.
        """
        self.app = app
        self.curr_page = self.app.curr_page
        self.menu = Menu(app.root)
        self.fileMenu = Menu(self.menu)
        self.portfolioMenu = Menu(self.menu)
        self.menu.add_cascade(menu=self.fileMenu, label='File')
        self.fileMenu.add_command(label='Open...', command=self.openFile)
        self.menu.add_cascade(menu=self.portfolioMenu, label='Portafoglio')
        self.portfolioMenu.add_command(label='vs Indici', command=self.vs_indexes)
        app.root['menu'] = self.menu

    def openFile(self):
        """
        Change the Info file for the portfolio.
        :return None
        """
        filename = filedialog.askopenfilename()
        self.app.p = Portfolio(filename, self.app.server)
        self.curr_page.left_frame.p = self.app.p
        self.curr_page.right_frame.p = self.app.p
        self.curr_page.right_frame.etf_list.p = self.app.p
        self.curr_page.right_frame.etf_list.refresh()
        self.curr_page.right_frame.add_etf.p = self.app.p
        self.curr_page.right_frame.sell_etf.p = self.app.p
        self.curr_page.left_frame.last_day()
    
    def vs_indexes(self):
        """
        Change page to the page where you can confront indexes with your portfolio.
        :return None
        """
        self.app.new_page()
        self.app.curr_page = VsIndexPage(self.app)
        