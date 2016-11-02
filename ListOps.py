from FileOps import arrayToCsv, csvToArray, csvToDict
import logging
from time import strftime
import ConfMod

'''
This module is used to interact with the user coffee list. Any changes will be written to disk immediately
@author: th0r
'''

#Set up logging
log = logging.getLogger('ListOps')

def consumeCoffee(userId):
    '''Increments the coffee counter for the given user 
    Keyword arguments:    
    userId -- the users id as stored in the spreadsheet
    '''
    #Get the value array
    values = csvToArray(ConfMod.getCsvFilePath())
    log.debug("Spreadsheet data received")
    
    #Clean the id if it contains ':'
    if ':' in userId :
        userId = str(userId).replace(':','')
        print('cleaned Id: ' + str(userId))
    
    log.debug("Trying to increment coffeecounter for user " + str(userId))
    if not values:        
        log.error('No data found!')
    else:#Iterate rows to find correct user
        notfound = True
        #iterate the value[][]
        for i in range(1,len(values)):            
            #When Id is found increment the coffee counter
            if str(values[i][0]) == str(userId):                
                values[i][1] = int(values[i][1])+1                            
                userName = values[i][2]
                userValue = values[i][1]
                log.info("Increased coffee count for user " + str(userName) + " ("+str(userId)+")" ". Current count " + str(userValue))
                #log.info("Increased coffee count for user " + str(userId))
                #User has been found: change flag to false
                notfound = False
                break
        if notfound:
            log.info('User with id '+ str(userId) +' could not be found')
            timestamp = strftime("%Y-%m-%d_%H:%M:%S")
            #appending new entry for user
            values.append([userId,1])                 
            
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

