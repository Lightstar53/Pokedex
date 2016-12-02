# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/Pokedex/

from datetime import date, datetime

class Movedata:
	"""Container for all move data"""

	def __init__(self, response=None):
		""" Constructor/object model """
		self.daysValid = 31 # Number of days the data is considered valid

		self.id = 0
		self.name = ""
		self.basePP = 0
		self.flavorText = ""
		self.accuracy = 0
		self.power = 0
		self.target = ""
		self.critRate = 0
		self.type = None
		self.updateTime = date.today()

		if response != None:
			self.id = response['id']
			self.name = response['names'][0]['name']
			self.basePP = response['pp']
			self.flavorText = response['effect_entries'][0]['effect']
			self.accuracy = response['accuracy']
			self.power = response['power']
			self.target = response['target']['name']
			self.critRate = response['meta']['crit_rate']
			self.type = response['type']['name']


	def formatResponse(self):
		""" 
			Returns a string describing the move. 
		"""
		PPString = "*Base PP:* " + str(self.basePP) + ".\n"
		accString = "*Accuracy:* " + str(self.accuracy) + ".\n"
		powerString = "*Power:* " + str(self.power) + ".\n"
		targetString = "*Target:* " + self.target + ".\n"

		response = PPString + accString + powerString + targetString
		response += "*Description:* " + self.flavorText + ".\n"
		response += "\nData was last updated: " + str(self.updateTime) + "\n"
		return response

	def isValid(self):
		""" Checks if the data can be considered valid """
		delta = date.today() - self.updateTime

		if delta.days < self.daysValid:
			return True
		else:
			return False