import logging
import ConfMod
import CloudOps
import ListOps
import FileOps

'''
Controlling module. Functions in this module can be used to access other features easily. 
In order to initialize the backend system call init() before performing any other operations.
@author: th0r
'''

log = logging.getLogger('Init')
initialized = False

def setupLog():    
    '''Set up logging facilities'''
    # set up logging to file
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='./log/CloudCoffee.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    
    # tell the handler to use this format
    console.setFormatter(formatter)
    
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

def init(): 
    '''Initialize list handling (i.e. setup the log, read config)'''    
    #Initialize config
    config = ConfMod.getConfig('')
    
    #Init logging      
    setupLog()
    
    log.info('------------------------------------------------')
    log.info('Starting up...')
    init = True
    
def updateLocalFile():
    '''Update the local csv file with cloud data'''
    CloudOps.updateLocalCsv()
    
def updateRemoteFile():
    '''Update cloud spreadsheet with local data'''
    CloudOps.updateCloudCsv()
    
def printCsv():
    '''Print the current local csv data'''
    FileOps.printCsv(ConfMod.getCsvFilePath())    
    
def addCoffee4User(userId):
    '''Increase the amount of coffees consumed for given user
    userId -- The userid requesting a coffee'''
    ListOps.consumeCoffee(userId)
    
def getUsername(userId):
    '''Returns the real name of the given user id'''
    return ListOps.getUsername(userId)
    
def getCoffeeAmount(userId):
    '''Return the amount of coffee consumed for given user id'''
    return ListOps.getCoffeeAmount(userId)
