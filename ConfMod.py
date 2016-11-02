import ConfigParser
import logging

'''
This module handles the configuration of the application and offers a couple of functions to get config info easily.
If no config file is provided, ./conf/coffeeconf.properties is used as a standard
@author: th0r
'''

STDCONFPATH = './conf/coffeeconf.properties'
CONFIGITEM = ''

#Set up logging
log = logging.getLogger('Config')

def getConfig(configPath):
    '''Retrieves the ConfigParser item; will be stored as global variable ConfMod.CONFIGITEM'''
    if configPath == '':
        configPath = STDCONFPATH
                         
    config = ConfigParser.RawConfigParser()
    config.read(configPath)
    global CONFIGITEM
    CONFIGITEM = config    
    return config

def printConfig(config):
    '''Prints the content of the current config file to log (info-level)'''
    sections = config.sections()
    for section in sections:
        items = config.items(section)
        #print("[" + str(section) + "]")
        logging.info("[" + str(section) + "]")
        for item in items:
            #print(str(item))
            logging.info(str(item))    

def getSheetId():    
    if CONFIGITEM:
        return CONFIGITEM.get('CloudInfoSection','cloud.sheetid')
    else:
        log.warn("Cannot get SheetId: ConfigItem not initialized")
        return None
        
def getSheetRange():
    if CONFIGITEM:
        return CONFIGITEM.get('CloudInfoSection','cloud.sheetrange')
    else:
        log.warn("Cannot get SheetRange: ConfigItem not initialized")
        return None
        
def getPkFilePath():
    if CONFIGITEM:
        return CONFIGITEM.get('CloudInfoSection','cloud.pkeyfilepath')
    else:
        log.warn("Cannot get PkeyFilePath: ConfigItem not initialized")
        return None
        
def getCsvFilePath():
    if CONFIGITEM:
        return CONFIGITEM.get('LocalInfoSection','local.csvfilepath')
    else:
        log.warn("Cannot get CsvFilePath: ConfigItem not initialized")
        return None

def getAccountName():
    if CONFIGITEM:
        return CONFIGITEM.get('CloudInfoSection','cloud.accountname')
    else:
        log.warn("Cannot get AccountName: ConfigItem not initialized")
        return None
    
def getScope():
    if CONFIGITEM:
        return CONFIGITEM.get('CloudInfoSection','cloud.scope')
    else:
        log.warn("Cannot get Scope: ConfigItem not initialized")
        return None
        
            
    
    