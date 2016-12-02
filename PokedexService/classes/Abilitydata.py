# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/Pokedex/

from datetime import date, datetime

class Abilitydata:
	"""Container for all move data"""

	def __init__(self, response=None):
		""" Constructor/object model """
		self.daysValid = 31 # Number of days the data is considered valid

		self.id = 0
		self.name = ""
		self.flavorText = ""
		self.updateTime = date.today()
		
		if response != None:
			self.id = response['id']
			self.name = response['names'][0]['name'] # Because regions
			self.flavorText = response['effect_entries'][0]['effect']
			self.flavorText.replace("\n", " ")	## A lot of the source data have way too many linebreaks. 

	def formatResponse(self):
		""" 
			Returns a string describing the move. 
		"""
		response = self.flavorText
		response += "\nData was last updated: " + str(self.updateTime) + ".\n"

		return response


	def isValid(self):
		""" Checks if the data can be considered valid """
		delta = date.today() - self.updateTime

		if delta.days < self.daysValid:
			return True
		else:
			return False