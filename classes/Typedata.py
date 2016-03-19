# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

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
	
	def sortLists(self):
		""" Sort all lists alphabetically """
		self.immunities.sort()
		self.resistances.sort()
		self.weaknesses.sort()
		self.halfDamageTo.sort()
		self.noDamageTo.sort()
