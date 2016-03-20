# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from datetime import date

class Pokedata:
	"""Container for all pokemon data"""

	def __init__(self):
		"""Constructor/Object model"""
		self.name = ""					# 
		self.sprite = ""
		self.dexId = 0					# 
		self.types = []					# typename
		self.weaknesses = []			# typename
		self.immunities = []			# typename
		self.resistances = []			# typename
		self.hiddenAbilities = []		# 
		self.locations = []				# "Route 404"
		self.evolutions = []
		self.updateTime = date.today()

		self.sortLists()

	def sortLists(self):
		""" Sort all lists alphabetically """
		self.immunities.sort()
		self.resistances.sort()
		self.weaknesses.sort()