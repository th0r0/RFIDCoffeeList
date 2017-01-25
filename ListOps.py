from FileOps import arrayToCsv, csvToArray, csvToDict
import logging
from time import strftime
import ConfMod

'''
This module is used to interact with the user coffee list. Any changes will be written to disk immediately
@author: th0r
'''

#Column mapping
COLUMN_ID = 0
COLUMN_COFFEE = 1
COLUMN_MILK = 2
COLUMN_NAME = 3


#Set up logging
log = logging.getLogger('ListOps')

def consumeCoffee(userId):
    '''Increments the coffee counter for the given user 
    Keyword arguments:    
    userId -- the users id as stored in the spreadsheet
    '''
    return _incrementCount(userId, COLUMN_COFFEE)        

def addMilk(userId):
    '''Increments the milk counter for the given user 
    Keyword arguments:    
    userId -- the users id as stored in the spreadsheet
    '''
    return _incrementCount(userId, COLUMN_MILK)

def _incrementCount(userId, sheetcolumn):
    '''Actually performs incrementation of the value for given user id
    Keyword arguments:    
    userId -- the users id as stored in the spreadsheet
    sheetcolumn -- the column value to be increased (e.g. ListOps.COLUMN_COFFEE or ListOps.COLUMN_MILK)
    '''
    #Get the value array
    values = csvToArray(ConfMod.getCsvFilePath())
    log.debug("Spreadsheet data received")
    
    #Clean the id if it contains ':'
    if ':' in userId :
        userId = str(userId).replace(':','')
        print('cleaned Id: ' + str(userId))
        
    log.debug("Trying to increment counter for user " + str(userId))
    if not values:        
        log.error('No data found!')
    else:#Iterate rows to find correct user
        notfound = True
        #iterate the value[][]
        for i in range(1,len(values)):            
            #When Id is found increment the counter
            if str(values[i][COLUMN_ID]) == str(userId):                
                values[i][sheetcolumn] = int(values[i][sheetcolumn])+1                            
                userName = values[i][COLUMN_NAME]
                userValue = values[i][sheetcolumn]
                log.info("Increased count for user " + str(userName) + " ("+str(userId)+")" ". Current count " + str(userValue))                
                notfound = False
                break
        if notfound:
            log.info('User with id '+ str(userId) +' could not be found')
            timestamp = strftime("%Y-%m-%d_%H:%M:%S")
            #appending new entry for user
            values.append([userId,1,0,userId])
             
    #Store in csv
    log.debug('Updating spreadsheet')            
    arrayToCsv(ConfMod.getCsvFilePath(), values)
    log.debug('Update complete')
    return None   


def getUsername(userId):
    values = csvToDict(ConfMod.getCsvFilePath())  
    user = values.get(userId,{'Name:':'UserId could not be found'})
    return user.get('Name','No name found')

def getCoffeeAmount(userId):
    values = csvToDict(ConfMod.getCsvFilePath())  
    user =  values.get(userId,{'Name:':"UserId could not be found"})
    return user.get('CoffeeAmount','No value found')

def getMilkAmount(userId):
    values = csvToDict(ConfMod.getCsvFilePath())  
    user =  values.get(userId,{'Name:':"UserId could not be found"})
    return user.get('MilkAmount','No value found')

