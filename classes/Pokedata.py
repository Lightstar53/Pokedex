# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

class Pokedata:
	"""Container for all pokemon data"""

	def __init__(self):
		"""Constructor/Object model"""
		self.name = ""					# 
		self.dexId = 0					# 
		self.types = []					# typename
		self.weaknesses = []			# typename
		self.immunities = []			# typename
		self.resistances = []			# typename
		self.hiddenAbilities = []		# 
		self.locations = []				# "Route 404"

		## Sort ##
	def SortImmunities(self):
		self.immunities.sort()
	def SortWeaknesses(self):
		self.weaknesses.sort()
	def SortResistances(self):
		self.resistances.sort()