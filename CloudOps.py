from __future__ import print_function
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import logging
from FileOps import arrayToCsv, csvToArray
import ConfMod
import FileOps
import string


'''
This module deals with all cloud related operations like connecting, retrieving and uploading data etc.
Values are generally read from a config file @see ConfMod.py
@author: th0r
'''

#Set up logging
log = logging.getLogger('FileOps')

def _getService():
	'''Returns a service object'''
	return _getHttpSheetService(_getPKeyAuthCredentials(ConfMod.getPkFilePath()))
	
def _getPKeyAuthCredentials(pkFile):
	credentials = ServiceAccountCredentials.from_json_keyfile_name(pkFile, scopes=ConfMod.getScope())
	delegated_credentials = credentials.create_delegated(ConfMod.getAccountName())
	return delegated_credentials

def _get_credentialsCHANGEME():
	"""Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    
    #CHANGEME
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'
    flags = None
	#CHANGEME
	
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    """
	return 0 

def _getHttpSheetService(credentials):
	'''Creates a sheet service object for the given credentials'''
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	return service

def _getSheetDataFromCloud(sheetId, sheetRange):
	'''Retrieves data from the cloudbased spreadsheet given 
    Keyword arguments:    
    sheetId -- the id of the spreadsheet (typically taken from the URL)
    sheetRange -- Cells to be downloaded
    '''	
	#connect to cloud
	service = _getService()
	
	#Get the spreadsheet	
	result = service.spreadsheets().values().get(spreadsheetId=sheetId, range=sheetRange).execute()
	values = result.get('values', [])
	log.debug("Spreadsheet data received")	
	
	return values
	
def _uploadSheetToCloud(values, sheetId, sheetRange, upOrApp):
	'''Uploades given values to the cloudbased spreadsheet. 
    Keyword arguments:    
    values -- Array of lists containing the values
    sheetId -- the id of the spreadsheet (typically taken from the URL)
    sheetRange -- target range of cells 
    upOrApp -- 'UPDATE' or 'APPEND' depending on use case (for now, just use 'UPDATE')
    '''	
	#connect to cloud
	service = _getService()
	
	#create upload payload
	#Since only 2 columns should be uploaded, the array is resized
	#Apparently I'm to stupid for numpy, so this is kinda ugly.. 
	upValues = []
	for i in values:
		upValues.append(i[0:2])
		

	body = {'values': upValues}
	
	#Upload changed valueset to cloud
	if upOrApp.upper() == 'UPDATE':
			log.debug('Updating spreadsheet')			
			result = service.spreadsheets().values().update(spreadsheetId=sheetId, range=sheetRange,valueInputOption='USER_ENTERED', body=body).execute()
			log.debug('Update complete')
	elif upOrApp.upper() == 'APPEND':
		#Appending entry to spreadsheet
		log.debug('Appending new user')			
		result = service.spreadsheets().values().append(spreadsheetId=sheetId, range=sheetRange,valueInputOption='USER_ENTERED', body=body).execute()
		log.debug('Append operation succesful')
	else:
		log.warn('Upload method not specified, no data written!')
	
	return result

def updateLocalCsv():
	''' Updates the locally stored information with data from the cloudbased google spreadsheet
	''' 
	#Before starting, we need to make sure that no data is overwritten with empty strings
	#Get remote data   
	valuesCloud = _getSheetDataFromCloud(ConfMod.getSheetId(), ConfMod.getSheetRangeDown())
	#Get local data 
	valuesLocal = FileOps.csvToArray(ConfMod.getCsvFilePath())
	
	#Compare
	for row in valuesCloud:
		for rowL in valuesLocal:
			if row[0]==rowL[0]:#if corresponding id found
				try:
					if len(row)>2:#remote has name -> indexlen is >2?
						if len(rowL)>2:#if a value is set locally
							rowL[2]=row[2]
					else:
						log.debug("No remote value for name found")
				except IndexError:
						log.error("There was an error while checking the usernames")
							 
						
	
	arrayToCsv(ConfMod.getCsvFilePath(), valuesLocal)
	return 0

def updateCloudCsv():
	''' Update the cloud stored spreadsheet with local data'''
	values = csvToArray(ConfMod.getCsvFilePath())
	_uploadSheetToCloud(values, ConfMod.getSheetId(), ConfMod.getSheetRangeUp(), 'UPDATE')
	return 0













#Main for development and testing purpose
#-----------------------------------------------------------------------------------------


'''def main():
	log.info('------------------------------------------------')
	log.info('Starting up...')	
	
	values = getSheetDataFromCloud(ConfMod.getSheetId(), ConfMod.getSheetRange())
	print(values)
	
			
if __name__ == '__main__':
	main()
'''