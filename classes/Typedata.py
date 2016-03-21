# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from datetime import date, datetime

class Typedata:
	""" Container for type data """

	def __init__(self, response=None):
		""" Build data structure from API response """
		self.immunities = []
		self.resistances = []
		self.weaknesses = []
		self.halfDamageTo = []
		self.noDamageTo = []
		self.updateTime = None
		self.name = ""
		self.id = 0
		self.updateTime = date.today()
		
		if response != None:
			self.name = response['name']
			self.id = response['id']
		
			for immunity in response['damage_relations']['no_damage_from']:
				self.immunities.append(immunity['name'])

			for resistance in response['damage_relations']['half_damage_from']:
				self.resistances.append(resistance['name'])

			for weakness in response['damage_relations']['double_damage_from']:
				self.weaknesses.append(weakness['name'])

			for resisted in response['damage_relations']['half_damage_to']:
				self.halfDamageTo.append(resisted['name'])

			for ineffective in response['damage_relations']['no_damage_to']:
				self.noDamageTo.append(ineffective['name']) 

		
		self.sortLists()

	def sortLists(self):
		""" Sort all lists alphabetically """
		self.immunities.sort()
		self.resistances.sort()
		self.weaknesses.sort()
		self.halfDamageTo.sort()
		self.noDamageTo.sort()


