from tkinter import *
from tkinter import ttk
from pyetf.functions import configure, graph, date_to_text, date_from_text

class VsIndexPage:
    """Class representing the page where you can confront your portfolio against other index"""

    def __init__(self, app):
        """
        Initialization of the page.
        """
        self.app = app
        self.portfolio = app.p

        self.centralFrame = ttk.Frame(app.mainframe)

        self.left_frame_init()
        self.leftFrame.grid(row=0, column=0, sticky=(W, N, S, E), padx=15)

        ttk.Separator(app.mainframe, orient=VERTICAL).grid(row=0, column=1, sticky='nswe')
        self.centralFrame.grid(row=0, column=2, columnspan=5, sticky=(E, W, N, S), padx=15)

        ttk.Separator(app.mainframe, orient=VERTICAL).grid(row=0, column=7, sticky='nswe')

        self.right_frame_init()
        self.rightFrame.grid(row=0, column=8, columnspan=2, sticky=(E, N, S, W), padx=15)

        configure(app.mainframe, 1, 8)

        self.equity_graph(index='SPY')
    
    def left_frame_init(self):
        """
        Initialization of the left frame.
        :return None
        """
        self.leftFrame = ttk.Frame(self.app.mainframe)

        # Selezione Indice --> Combobox e Label
        ttk.Label(self.leftFrame, text='Portafoglio vs', justify='center').grid(row=0, column=0, columnspan=2, pady=(20,0))
        indexToTicker = {'S&P 500': 'SPY', 'NASDAQ': '^IXIC', 'DAX': '^GDAXI', 'DOW JONES': '^DJI', 'NIKKEI 225': '^N225', 'FTSE MIB': 'FTSEMIB.MI'}
        self.index = StringVar(value='S&P 500')
        self.combo = ttk.Combobox(self.leftFrame, textvariable=self.index, width=14, justify='center', state='readonly', values=list(indexToTicker.keys()))
        self.combo.grid(row=1, column=0, columnspan=2, pady=(0,20))
        self.combo.bind('<<ComboboxSelected>>', lambda _: self.combo.selection_clear())

        # Separator
        ttk.Separator(self.leftFrame, orient=HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky='nswe', padx=(20, 0))

        # Data Iniziale --> Entry e Label
        ttk.Label(self.leftFrame, text="Data iniziale").grid(row=3, column=0)
        dIni = self.portfolio.data.index[0]
        self.dateIni = StringVar(value=date_to_text(dIni))
        ttk.Entry(self.leftFrame, textvariable=self.dateIni, width=10, justify='center').grid(row=3, column=1)

        # Bottone per rimettere il primo giorno --> Button
        ttk.Button(self.leftFrame, text='Inizio', command=lambda: self.dateIni.set(date_to_text(dIni))).grid(row=4, column=0, columnspan=2, pady=(0,20))

        # Data Finale --> Entry e Label
        ttk.Label(self.leftFrame, text="Data finale").grid(row=5, column=0, pady=(20,0))
        dFin = self.portfolio.data.index[-1]
        self.dateFin = StringVar(value=date_to_text(dFin))
        ttk.Entry(self.leftFrame, textvariable=self.dateFin, width=10, justify='center').grid(row=5, column=1, pady=(20,0))

        # Bottone per rimettere l'ultimo giorno --> Button
        ttk.Button(self.leftFrame, text='Fine', command=lambda: self.dateFin.set(date_to_text(dFin))).grid(row=6, column=0, columnspan=2)

        # Separator
        ttk.Separator(self.leftFrame, orient=HORIZONTAL).grid(row=7, column=0, columnspan=2, sticky='nswe', padx=(20, 0))
        
        # Bottone per aggiornare --> Button
        iniChoice = lambda: date_from_text(self.dateIni.get())
        finChioce = lambda: date_from_text(self.dateFin.get())
        refreshGraph = lambda: self.equity_graph(index=indexToTicker[self.index.get()], dateIni=iniChoice(), dateFin=finChioce())
        ttk.Button(self.leftFrame, text='Aggiorna', command=refreshGraph).grid(row=8, column=0, columnspan=2, pady=(0,30))

        configure(self.leftFrame, 9, 2)
    
    def right_frame_init(self):
        """
        Initialization of the right frame.
        :return None
        """
        self.rightFrame = ttk.Frame(self.app.mainframe)
        ttk.Button(self.rightFrame, text='Pagina Iniziale', command=self.app.initial_page).grid(row=0, column=0)
        ttk.Button(self.rightFrame, text='Chiudi', command=self.app.mainframe.quit).grid(row=1, column=0)
        configure(self.rightFrame, 2, 1)

    def equity_graph(self, **kwargs):
        """
        Draws the equity graph on the central frame based on the arguments passed as parameters.
        :param kwargs: dict
        :return None
        """
        self.centralFrame = ttk.Frame(self.app.mainframe)
        self.centralFrame.grid(row=0, column=2, columnspan=5, sticky=(E, W, N, S), padx=15)
        #clear_selection('PortfolioGraphs', self)
        fig, ax = self.portfolio.equity_line(pct=True, **kwargs)
        # frame = ttk.Frame(self.c_frame)
        # frame.pack(side=BOTTOM)
        # ttk.Checkbutton(frame, text='Percentuale', variable=pct, onvalue=True, offvalue=False, command=lambda: self.equity_graph(pct=pct.get(), sp500=sp500.get())).grid(row=0, column=0, pady=20, padx=20)
        # ttk.Checkbutton(frame, text='S&P500', variable=sp500, onvalue=True, offvalue=False, command=lambda: self.equity_graph(pct=pct.get(), sp500=sp500.get())).grid(row=0, column=2, pady=20, padx=20)
        # configure(frame, 0, 3)
        graph(fig, self.centralFrame)