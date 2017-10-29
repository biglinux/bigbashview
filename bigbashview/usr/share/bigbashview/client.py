from bbv.main import Main
from sys import argv
from bbv import globals as globaldata

if __name__ == "__main__":
    if len(argv) < 2:
        print 'usage: %s ip:port'
        exit()
    
    ip,port = argv[1].split(':')
    del argv[1]
    globaldata.ADDRESS = lambda: ip
    globaldata.PORT = lambda: port
    
    app = Main()
    app.run(server=False)