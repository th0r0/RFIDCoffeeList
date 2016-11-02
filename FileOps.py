import logging
import csv

'''
This module deals with all file related operations like storing/reading data.
@author: th0r
'''

#Set up logging
logging = logging.getLogger('FileOps')


def printCsv(filePath):
	'''Prints the csv file given to the log (info)
	'''
	with open(filePath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			logging.info(row['ID'], row['CoffeeAmount'], row['Name'], row['Email'],row['Cost'])

def csvToArray(filePath):
	'''Reads a given csv file and returns an array of lists'''
	with open(filePath) as csvfile:
		#reader = csv.DictReader(csvfile)
		reader = csv.reader(csvfile)
		values = [l for l in reader]
	return values

def csvToDict(filePath):
	'''Reads a given csv file and returns a dictionary of lists'''
	values={}
	with open(filePath) as csvfile:
		reader = csv.DictReader(csvfile)		
		#add tuple to dictionary
		for row in reader:
			key = row.pop('ID')
			if key in values:
				# implement your duplicate row handling here
				pass
			values[key]=row
	return values

def arrayToCsv(filePath, array):
	'''Writes an array of lists to the specified filepath as csv'''
	with open(filePath, "wb") as f:
		writer = csv.writer(f)
		writer.writerows(array)
		

'''def main():
	logging.info('------------------------------------------------')
	logging.info('Starting up...')	
	#printCsv('./testread - Users.csv')
	values = csvToArray('./testread - Users.csv')
	arrayToCsv('./testread - Users_NEW.csv', values)
			
if __name__ == '__main__':
	main()
'''