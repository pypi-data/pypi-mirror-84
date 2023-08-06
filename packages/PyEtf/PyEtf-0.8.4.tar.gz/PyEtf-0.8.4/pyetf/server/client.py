import socket    


def connect():
    s = socket.socket()         
    host = '192.168.1.18' 
    port = 12345                 
    s.connect((host, port))
    return s 

def getFile(filePath, savePath):
    s = connect()
    s.send(filePath.encode('utf-8'))
    f = open(f'{savePath}.csv','wb')
    l = s.recv(1024)
    while (l):
        f.write(l)
        l = s.recv(1024)
    f.close()
    print("Receved " + filePath)
    s.shutdown(socket.SHUT_WR)
    s.close()                  

def buy_etf(etfData):
    etfData = 'buy,' + etfData
    s = connect()
    s.send(etfData.encode('utf-8'))
    ticker = etfData.split(',')[1]
    print(f'Comprato {ticker}')
    s.shutdown(socket.SHUT_WR)
    s.close()

def sell_etf(etfData):
    etfData = 'sell,' + etfData
    s = connect()
    s.send(etfData.encode('utf-8'))
    ticker = etfData.split(',')[1]
    print(f'Venduto {ticker}')
    s.shutdown(socket.SHUT_WR)
    s.close()   