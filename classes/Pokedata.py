# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

class Pokedata:
	"""Container for all pokemon data"""

	def __init__(self):
		"""Constructor/Object model"""
		self.name = ""					# 
		self.dexId = 0					# 
		self.types = []					# typename, url
		self.weaknesses = []			# typename
		self.immunities = []			# typename
		self.resistances = []			# typename

		## Types
	def AddType(self, type):
		self.types.append(type)
	def GetTypes(self):
		return self.types
		
		## Weaknesses
	def AddWeakness(self, weakness):
		self.weaknesses.append(weakness)
	def GetWeaknesses(self):
		return self.weaknesses
	def RemoveWeakness(self, weakness):
		self.weaknesses.remove(weakness) 

		## Resistances
	def AddResistance(self, resistance):
		self.resistances.append(resistance)
	def GetResistances(self):
		return self.resistances
	def RemoveResistance(self, resistance):
		self.resistances.remove(resistance)

		## Immunities
	def AddImmunity(self, immunity):
		self.immunities.append(immunity)
	def GetImmunities(self):
		return self.immunities
		
		## GET/SET ##
	def SetName(self, name):
		self.name = name
	def SetDexId(self, dexId):
		self.dexId = dexId
	def GetName(self):
		return self.name
	def GetDexId(self):
		return self.dexId

		## Sort ##
	def SortImmunities(self):
		self.immunities.sort()
	def SortWeaknesses(self):
		self.weaknesses.sort()
	def SortResistances(self):
		self.resistances.sort()