# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from datetime import date

class Typedata:
	""" Container for type data """

	def __init__(self):
		""" Object model """				# in DB
		self.name = ""						# Varchar
		self.id = 0							# int
		self.immunities = []				# array[]
		self.resistances = []				# array[]
		self.weaknesses = []				# array[]
		self.halfDamageTo = []				# array[]
		self.noDamageTo = []				# array[]
		self.updateTime	= None				# updateTime
		# self.pokemon = [] # Potentially a list of pokemon IDs that are of type self.name, but probably unnecessary
		# self.moves = [] # Potentially a list of *all* moves that are of type self.name

	def __init__(self, response):
		""" Build data structure from API response """
		self.name = response['name']
		self.id = response['id']
		self.immunities = []
		self.resistances = []
		self.weaknesses = []
		self.halfDamageTo = []
		self.noDamageTo = []
		self.updateTime = None

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

		self.updateTime = date.today()
		self.sortLists()

	def sortLists(self):
		""" Sort all lists alphabetically """
		self.immunities.sort()
		self.resistances.sort()
		self.weaknesses.sort()
		self.halfDamageTo.sort()
		self.noDamageTo.sort()

	
