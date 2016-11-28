# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/Pokedex/

from datetime import date
from collections import Counter

class Pokedata:
	"""Container for all pokemon data"""

	def __init__(self, response=None):
		"""Constructor/Object model"""
		self.daysValid = 31 # Number of days the data is considered valid

		self.spriteURL = "http://img.pokemondb.net/artwork/"
		self.id = 0						
		self.name = ""					
		self.sprite = ""				
		self.types = []					
		self.weaknesses = []			
		self.immunities = []			
		self.resistances = []
		self.abilities = []			
		self.hiddenAbilities = []		
		self.locations = []				
		self.updateTime = date.today()

		if response != None:
			self.id = response['id']
			self.name = response['name']
			self.sprite = self.spriteURL + self.name

			## Exceptions because... reasons...
			if self.name == 'hoopa':
				self.sprite += "-confined.jpg"
			elif self.name == 'volcanion':
				self.sprite = 'http://img.pokemondb.net/sprites/x-y/normal/volcanion.png'
			elif self.name == 'keldeo':
				self.sprite += "-ordinary.jpg"
			else:
				self.sprite += ".jpg"

			for pokeType in response['types']:
				self.types.append(pokeType['type']['name'])

			for ability in response['abilities']:
				if ability['is_hidden'] == True:
					self.hiddenAbilities.append(ability['ability']['name'])
				else:
					self.abilities.append(ability['ability']['name'])

			# Do something about locations, species, breed, evolution chains?

		self.sortLists()

	def sortLists(self):
		""" Sort all lists alphabetically """
		self.immunities.sort()
		self.resistances.sort()
		self.weaknesses.sort()

	def determineTypeEffectiveness(self, types):
		""" Check immunities, resistances and weaknesses for occurences that cancel out """			

		## Add in type specific information
		for pokeType in types:
			self.weaknesses.extend(pokeType.weaknesses)
			self.resistances.extend(pokeType.resistances)
			self.immunities.extend(pokeType.immunities)

		## Check for duplicates
		for resistance in self.resistances:						## Check all resistances up against all immunities.
			for immunity in self.immunities:
				if resistance == immunity:						## Pokemon is immune, remove resistance from list. 
					self.resistances.remove(resistance)
		for weakness in self.weaknesses:						## Check all weaknesses up against all immunities
			for immunity in self.immunities:
				if weakness == immunity:						## Pokemon is immune, remove weakness from list. 
					self.weaknesses.remove(weakness)
		for weakness in self.weaknesses:						## Check all weakness up against all resistances
			for resistance in self.resistances:
				if weakness == resistance:						## 1/2 x 2x == 1x, they cancel out. 
					self.weaknesses.remove(weakness)
					self.resistances.remove(resistance)

		self.sortLists()

	def isValid(self): 
		""" Checks if the data can be considered valid """
		delta = date.today() - self.updateTime

		if delta.days < self.daysValid: # If valid
			return True
		else:
			return False

	def buildResponseString(self):
		""" Returns a string describing the pokemon """
		## Some nice string formatting code incoming... bleugh
		response = ""
		
		# types
		typeString = self.name.title() + " has type"
		length = len(self.types)
		count = 0
		if length > 1:
			typeString += "s: "
		else:
			typeString += ": "

		for pokeType in self.types:
			typeString += pokeType.title()
			count += 1
			if count == length:
				typeString += ".\n"
			else:
				typeString += " and "
		response += typeString

		# weaknesses
		weaknessString = ""
		length = len(self.weaknesses)
		if length == 0:
			weaknessString = "It is _*not*_ weak against damage of any type.\n"
		elif length == 1:
			weaknessString = "It takes _*double*_ damage from _" + self.weaknesses[0] + "_ type attacks.\n"
		else:
			weaknessString = "It takes _*increased*_ damage from " 

			cnt = Counter(self.weaknesses)
			length = len(cnt)
			count = 0
			for weakness, num in cnt.most_common():
				if num > 1:
					weaknessString += "_*" + weakness.title() + "*_" # Italic bold
				else:
					weaknessString += "_" + weakness.title() + "_" # italic
				count += 1
				if count < length:
					if count == (length - 1):
						if length > 2:
							weaknessString += ", and "
						else:
							weaknessString += " and "
					else:
						weaknessString += ", "
				else:
					weaknessString += " type attacks.\n"
		response += weaknessString
		
		# resistances
		resistanceString = ""
		length = len(self.resistances)
		if length == 0:
			resistanceString = "It is _*not*_ resistant to damage of any type.\n"
		elif length == 1:
			resistanceString = "It takes _*halved*_ damage from _" + self.resistances[0] + "_ type attacks.\n"
		else:
			resistanceString = "It takes _*decreased*_ damage from "

			cnt = Counter(self.resistances)
			length = len(cnt)
			count = 0
			for resistance, num in cnt.most_common():
				if num > 1:
					resistanceString += "_*" + resistance.title() + "*_"	# Italic bold
				else:
					resistanceString += "_" + resistance.title() + "_"		# italic
				count += 1
				if count < length:
					if count == (length - 1):
						if length > 2:
							resistanceString += ", and "
						else:
							resistanceString += " and "
					else:
						resistanceString += ", "
				else:
					resistanceString += " type attacks.\n"
		response += resistanceString

		# immunities
		checked = []
		immunityString = ""
		length = len(self.immunities)
		if length == 0:
			immunityString = "It is *not* immune to damage of any type.\n"
		elif length == 1:
			immunityString = "It is immune to damage from _" + self.immunities[0] + "_ type moves.\n"
		else:
			immunityString = "It is immune to damage from "
			count = 0
			for immunity in self.immunities:
				if immunity not in checked:
					immunityString += "_" + immunity.title() + "_"
					count += 1
					checked.append(immunity)
					if count == length:
						immunityString += " type moves.\n"
					else:
						if count == (length - 1):
							if length > 2:
								immunityString += ", and "
							else:
								immunityString += " and "
						else:
							immunityString += ", "
		response += immunityString

		# hidden abilities
		hiddenString = "It has "
		length = len(self.hiddenAbilities)
		if length == 0:
			hiddenString += "*no* possible hidden abillities.\n"
		elif length == 1:
			hiddenString += "the following potential hidden ability: "
		else:
			hiddenString += "the following potential hidden abilities: "

		count = 0
		for hidden in self.hiddenAbilities:
			hiddenString += hidden.title()
			count += 1
			if count == length:
				hiddenString += ".\n"
			else:
				hiddenString += ", "
		response += hiddenString

		# non-hidden abilities
		abilityString = "It has "
		length = len(self.abilities)
		if length == 0:
			abilityString += "*no* possible non-hidden abilities.\n"
		elif length == 1:
			abilityString += "the following potential non-hidden ability: "
		else:
			abilityString += "the following potential non-hidden abilities: "

		count = 0
		for ability in self.abilities:
			abilityString += ability.title()
			count += 1

			if count == length:
				abilityString += ".\n"
			else:
				abilityString += ", "
		response += abilityString
 
		# Additional
		response += "\nTypes marked in *bold* signify double effect (4x weakness or 1/4x resistance).\n"
		response += "Data was last updated: " + str(self.updateTime) + "\n"

		return response


	
