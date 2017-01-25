import logging
import ListController
import random
log = logging.getLogger('Init')

'''
Test module to show off the features
@author: th0r
'''

def main():
	
	#Init everything, yes this is necessary!!!
	ListController.init()
	
	#Testing code for existing user	
	#Get remote data
	ListController.updateLocalFile()
	
	#Increase count
	ListController.addCoffee4User('54fea7ef')
	ListController.addMilk4User('54fea7ef')
	#get some info	
	log.info(ListController.getUsername('54fea7ef'))
	log.info('Coffee:' + ListController.getCoffeeAmount('54fea7ef'))
	log.info('Milk: ' + ListController.getCoffeeAmount('54fea7ef'))
	
	#Upload changed data
	ListController.updateRemoteFile()
	
	
	randomInt = str(random.randint(1,1000)) #Yeah I know, sometimes it'll hit an existing
	ListController.addCoffee4User('54fea7efT'+ randomInt)	
	log.info(ListController.getUsername('54fea7efT'+ randomInt))
	log.info("Coffees: " + ListController.getCoffeeAmount('54fea7efT'+ randomInt))
	log.info("Milks: " + ListController.getCoffeeAmount('54fea7efT'+ randomInt))
	
	ListController.updateRemoteFile()

	
			
if __name__ == '__main__':
	main()
