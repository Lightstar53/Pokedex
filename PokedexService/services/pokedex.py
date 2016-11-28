# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/Pokedex/

from flask import jsonify
from enum import Enum, unique
from datetime import date, datetime
import requests
import csv

from PokedexService.classes.DatabaseHandler import DatabaseHandler
from PokedexService.classes.Typedata import Typedata
from PokedexService.classes.Pokedata import Pokedata

@unique
class keywords(Enum):
	pokeType = 'type'
	pokemon = 'pokemon'
	dexList = 'list'
	ability = 'ability'

@unique
class occurenceType(Enum):
	pokeType = 'types'
	pokemon = 'pokemon'
	ability = 'abilities'

class PokedexRequestHandler:
	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None
		self.DB = DatabaseHandler(verbose)
		self.baseUrl = 'http://pokeapi.co/api/v2/'
		self.DataValidity = 14				## Number of days data is valid before re-retrieving
		self.totalNumberOfPokemon = 802		## As of generation 7 Sun/Moon	
		self.totalNumberOfTypes = 18		## As of generation 7 Sun/Moon
		self.generationStartPokemon = [1, 152, 252, 387, 494, 650, 722]	# Gen1 - 7
		self.notFound = 'Not found.'
		self.responseType = 'in_channel'
 
		self.colorLookup = {
			'normal': '#A8A77A', 'fire': '#EE8130', 'water': '#6390F0', 'electric': '#F7D02C',
			'grass': '#7AC74C', 'ice': '#96D9D6', 'fighting': '#C22E28', 'poison': '#A33EA1',
			'ground': '#E2BF65', 'flying': '#A98FF3', 'psychic': '#F95587', 'bug': '#A6B91A',
			'rock': '#B6A136', 'ghost': '#735797', 'dragon': '#6F35FC', 'dark': '#705746',
			'steel': '#B7B7CE', 'fairy': '#D685AD'}


	def populateDBFromCSV(self):
		""" Reads pokemon information for a .csv file, populating the DB.
			format is: id, name, sprite, types, hiddens, abilities """
		if not self.DB.connectToDatabase():
			return jsonify({"response_type": "ephemeral", "text": "Database connection error. Alert admin. "})

		with open('gen7.csv') as csvfile:
			reader = csv.DictReader(csvfile, delimiter=',', escapechar='|')
			for row in reader:
				pokedata = Pokedata()
				pokedata.id = row['num']
				pokedata.name = row['name'].lower()
				pokedata.sprite = row['sprite']
				pokedata.hiddenAbilities = row['hiddens'].split(',')
				pokedata.abilities = row['abilities'].split(',')
				pokedata.updateTime = date.today()
				pokedata.types = row['types'].split(',')
				pokedata.sortLists()
				
				internal = True							## Doing an internal query
				types = []					
				for pokeType in pokedata.types:			## Retrieving weaknesses, resistances, immunities for each type. 
					queryElements = []
					queryElements.append(pokeType)
					types.append(self.handleTypeRequest(queryElements, internal))

				pokedata.determineTypeEffectiveness(types)
				print("Storing: " + pokedata.id + ", " + pokedata.name)
				self.DB.storePokemon(pokedata)

	def populateDB(self):
		""" Populate the database with information """
		timestamp = datetime.now()

		for i in range(1, self.totalNumberOfPokemon + 1):
			self.handlePokedexRequest(str(i))

		for i in range(1, self.totalNumberOfTypes + 1):
			self.handlePokedexRequest("type" + str(i))

		timestamp2 = datetime.now()
		self.verboseprint("Populate took from: " + datetime.strftime(timestamp, '%H:%M:%S') 
						+ " to: " + datetime.strftime(timestamp2, '%H:%M:%S'))

	def handlePokedexRequest(self, query, response_url=None):
		""" Determine what kind of pokedex request is made, and delegate responsibility accordingly. """
		timestamp = datetime.now()
		self.verboseprint(datetime.strftime(timestamp, '%H:%M:%S') + ": Handling a /dex request with text: " + query)
		if not self.DB.connectToDatabase():
			return jsonify({"response_type": "ephemeral", "text": "Database connection error. Alert admin. "})

		query = query.lower()
		if query == "help":			# Oh snap! A user needs help
			return self.help()

		# Split the input string on whitespace " ".
		queryElements = query.split(" ")
		keyword = queryElements[0]
		
		# Does the user want this to be a private message?
		silent = queryElements[-1]
		if silent.lower() == 'silent':
			self.responseType = 'ephemeral'
			self.verboseprint("Response type set to silent!")
		else:
			self.responseType = 'in_channel'

		if keyword == keywords.pokeType.value:
			self.verboseprint("Keyword 'type' found!")
			return self.handleTypeRequest(queryElements[1:])

		elif keyword == keywords.pokemon.value:
			self.verboseprint("Keyword 'pokemon' found!")
			return self.handlePokemonRequest(queryElements[1:])

		else:			## Unknown keyword, assume pokemon
			self.verboseprint("Keyword is unknown.")
			return self.handlePokemonRequest(queryElements)

	def handlePokemonRequest(self, query):
		""" Handles any 'pokemon' request. First we have to check if it is currently known by our DB.
			If it is known, we have to determine if the data is too old and has to be re-acquired """

		## Exceptions, they do seem to love non-conforming pokemon
		if query[0] == 'deoxys':
			query[0] = 'deoxys-normal'
		elif query[0] == 'keldeo':
			query[0] = 'keldeo-ordinary'
		elif query[0] == 'oricorio':
			query[0] = 'oricorio-baile'
		elif query[0] == 'minior':
			query[0] = 'minior-meteor'
		elif query[0] == 'tapu':
			query[0] = 'tapu-koko'
		elif query[0] ==  'lycanroc':
			query[0] = 'lycanroc-midday'
		elif query[0] == 'type:' or query[0] == 'type:null' or query[0] == 'type: null':
			query[0] == 'type-null'


		knownPokemon = self.DB.getAllKnownPokemon()

		## Check for old data (and if we have to reacquire)
		for known in knownPokemon:
			if query[0] == known.name or query[0] == str(known.id):
				self.verboseprint("Pokemon found in DB!")

				if known.isValid():
					return jsonify(self.formatPokeString(known))
				else:
					self.DB.deleteOccurence(known, occurenceType.pokemon.value)
					break

		## If no data, or too old data, query the API for info.
		queryString = self.baseUrl + 'pokemon/' + query[0]
		response = self.makePokeAPIRequest(queryString)

		if response != False:
			pokedata = Pokedata(response)

			internal = True							## Doing an internal query
			types = []					
			for pokeType in pokedata.types:			## Retrieving weaknesses, resistances, immunities for each type. 
				queryElements = []
				queryElements.append(pokeType)
				types.append(self.handleTypeRequest(queryElements, internal))

			pokedata.determineTypeEffectiveness(types)
			self.DB.storePokemon(pokedata)

			return jsonify(self.formatPokeString(pokedata))

		return self.errorReply()

	def handleTypeRequest(self, query, internal=False):
		""" Handles any 'type' request. First we have to check if it is currently known by our DB.
			If it is known, we have to determine if the data is too old and has to be re-acquired """
		knownTypes = self.DB.getAllKnownTypes()

		if internal:			## Some other functions needs typedata, we don't want to return a prettyfied JSON string. 
			self.verboseprint("Handling an internal typeRequest: " + str(query))

		## Check for old data (and if we have to reacquire)
		for knownType in knownTypes:
			if query[0] == knownType.name or query[0] == str(knownType.id):
				self.verboseprint("Typematch found!")
				if knownType.isValid():
					if internal:
						return knownType
					return jsonify(self.formatTypeString(knownType))
				else:
					self.DB.deleteOccurence(knownType, occurenceType.pokeType.value)
					break

		## If no data has been found we need to query the API for potential new type (or BS)
		## Also run if data is too old. 
		queryString = self.baseUrl + 'type/' + query[0]
		response = self.makePokeAPIRequest(queryString)

		if response != False: # We found something useful
			typedata = Typedata(response)
			self.DB.storeType(typedata)

			if internal:
				return typedata

			return jsonify(self.formatTypeString(typedata))

		return self.errorReply()

	def makePokeAPIRequest(self, queryString ):
		""" Makes a request to pokeAPI with given argument """
		self.verboseprint("Querystring: " + queryString)
		timestamp = datetime.now()
		self.verboseprint(datetime.strftime(timestamp, '%H:%M:%S') + ": Making request")
		response = requests.get(queryString).json()
		timestamp2 = datetime.now()
		self.verboseprint(datetime.strftime(timestamp2, '%H:%M:%S') + ": Request finished.")

		if 'detail' in response.keys() and response['detail'] == self.notFound:
			self.verboseprint("Seems to be a 404. ")
			return False

		return response

	def stringBuilder(self, mList):
		## move internally to typedata?
		count = 0
		responseString = ""

		if len(mList) == 0:
			responseString += "None.\n"

		for thing in mList:
			responseString += thing.title()
			count += 1
			if count == len(mList):
				responseString += ".\n"
			else:
				responseString += ", "
		return responseString

	def formatPokeString(self, pokedata):
		""" Formats a 'pokemon' string for pretty return to slack """
		self.verboseprint("Formatting a pokemon string")
		header = "*Pokemon #" + str(pokedata.id) +":*\n"
		color = self.colorLookup[pokedata.types[0]]
		fallback = "Pokemon information for " + pokedata.name + "."

		responseString = pokedata.buildResponseString()

		response = {
			"text": header,
			"response_type": self.responseType,
			"attachments": [{
				"fallback": fallback,
				"color": color, 
				"title": pokedata.name.title(),
				"title_link": "https://github.com/Sidaroth/PokedexService",
				"text": responseString,
				"mrkdwn_in": ['text'],
				"thumb_url": pokedata.sprite
			}]
		}
		
		return response

	def formatTypeString(self, typedata):
		""" Formats a type string for pretty return to slack """
		self.verboseprint("Formatting type string!")
		header = "*Type #" + str(typedata.id) + ":*\n"
		color = self.colorLookup[typedata.name]
		fallback = "Type information for " + typedata.name + "."

		## String formatting for pretty print. 
		weaknessString    = "*Weaknesses*: "			+ self.stringBuilder(typedata.weaknesses)
		resistanceString  = "*Resistances*: "			+ self.stringBuilder(typedata.resistances)
		immunityString    = "*Immunities*: "			+ self.stringBuilder(typedata.immunities)
		resistedString    = "*Resisted by*: "			+ self.stringBuilder(typedata.halfDamageTo)
		ineffectiveString = "*Ineffective against*: "	+ self.stringBuilder(typedata.noDamageTo)

		responseString = weaknessString + resistanceString + immunityString + resistedString + ineffectiveString + "\n"
		responseString += "\nData was last updated: " + str(typedata.updateTime) + "\n"

		response = {
			"text": header,
			"response_type": self.responseType,
			"attachments": [{
				"fallback": fallback,
				"color": color,
				"title": typedata.name.title(), 
				"title_link": "https://github.com/Sidaroth/PokedexService",
				"text": responseString,
				"mrkdwn_in": ['text']
			}]
		}

		return response

	def help(self):
		""" Displays helpful information privately to the user on request """
		self.verboseprint("Oh snap! A user has request aid!")
		responseString = "*Help:*\n"

		fallBack = "Example usage: ----"
		helpString =  "Example usage:\n"
		helpString += "*/dex [pokemon]* \n"
		helpString += "*/dex type [type]* \n"
		helpString += "*/dex pokemon [pokemon]* \n"
		helpString += "*/dex type [type] silent* for a private query. This is hidden from the chat channel.\n"
		helpString += "For all queries [type] or [pokemon] is interchangable with any name or id, i.e grass and 12, or bulbsaur and 1.\n"
		helpString += "Usage of the 'silent' flag is also available for *all* commands.\n"
		
		response = {
			"text": responseString,
			"attachments": [{
				"fallback": fallBack,				## Required
				"color": "good",					## Actually green
				"title": "Pokedex Documentation",
				"title_link": "https://github.com/Sidaroth/PokedexService",
				"text":	helpString,
				"mrkdwn_in": ["text"] 
			}],
			"response_type": "ephemeral"
		}

		return jsonify(response)

	def errorReply(self):
		return jsonify({"response_type": "ephemeral", "text": "Your query does not match any currently known pokemon! Try /dex help for more information."})
