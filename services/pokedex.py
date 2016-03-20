# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from flask import jsonify
from enum import Enum, unique
from datetime import date
import requests

from classes.DatabaseHandler import DatabaseHandler
from classes.Typedata import Typedata

@unique
class keywords(Enum):
	pokeType = 'type'
	pokemon = 'pokemon'
	dexList = 'list'
	ability = 'ability'

class PokedexRequestHandler:
	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None
		self.DB = DatabaseHandler(verbose)
		self.baseUrl = 'http://pokeapi.co/api/v2/'

		self.DataValidity = 14				## Number of days data is valid before re-retrieving
		self.totalNumberOfPokemon = 721		## As of generation 6 XY/ORAS	
		self.totalNumberOfTypes = 18		## As of generation 6 XY/ORAS
		self.generationStartPokemon = [1, 152, 252, 387, 494, 650, 722]	# Gen1 - 7
		self.notFound = 'Not found.'
		self.responseType = 'in_channel'

		self.colorLookup = {
			'normal': '#A8A77A', 'fire': '#EE8130', 'water': '#6390F0', 'electric': '#F7D02C',
			'grass': '#7AC74C', 'ice': '#96D9D6', 'fighting': '#C22E28', 'poison': '#A33EA1',
			'ground': '#E2BF65', 'flying': '#A98FF3', 'psychic': '#F95587', 'bug': '#A6B91A',
			'rock': '#B6A136', 'ghost': '#735797', 'dragon': '#6F35FC', 'dark': '#705746',
			'steel': '#B7B7CE', 'fairy': '#D685AD'}

	def handlePokedexRequest(self, query, response_url):
		""" Determine what kind of pokedex request is made, and delegate responsibility accordingly. """
		self.verboseprint("Handling a /dex request with text: " + query)
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

		else:
			self.verboseprint("Keyword is unknown.")

		# Backup plan: 
		# We don't know it, pokeapi doesn't know it. It's probably not written correctly, or it is not relevant. 
		self.DB.connection.close()
		return self.errorReply()
	
	def handlePokemonRequest(self, query):
		""" Handles any 'pokemon' request. First we have to check if it is currently known by our DB.
			If it is known, we have to determine if the data is too old and has to be re-acquired """

		knownPokemon = self.DB.getAllKnownPokemon()


	def handleTypeRequest(self, query):
		""" Handles any 'type' request. First we have to check if it is currently known by our DB.
			If it is known, we have to determine if the data is too old and has to be re-acquired """
		knownTypes = self.DB.getAllKnownTypes()

		## Check for old data (and if we have to reacquire)
		for knownType in knownTypes:
			if query[0] == knownType.name or query[0] == str(knownType.id):
				self.verboseprint("Typematch found!")
				delta = knownType.updateTime - date.today()

				if delta.days < self.DataValidity:
					self.verboseprint("Data is considered valid!")
					return jsonify(self.formatTypeString(knownType))
				else:
					self.DB.deleteOccurence(knownType)
					self.verboseprint("Data is NOT considered valid!")
					break

		## If no data has been found we need to query the API for potential new type (or BS)
		## Also run if data is too old. 
		self.verboseprint("")
		queryString = self.baseUrl + 'type/' + query[0]
		self.verboseprint("Querystring: " + queryString)
		response = self.makePokeAPIRequest(queryString)

		if response != False: # We found something useful
			typedata = Typedata(response)
			self.DB.storeType(typedata)

			return jsonify(self.formatTypeString(typedata))

		return self.errorReply()

	def makePokeAPIRequest(self, queryString ):
		""" Makes a request to pokeAPI with given argument """
		response = requests.get(queryString).json()
		if 'detail' in response.keys() and response['detail'] == self.notFound:
			self.verboseprint("Seems to be a 404. ")
			return False

		return response

	def formatTypeString(self, typedata):
		""" Formats a type string for pretty return to slack """
		self.verboseprint("Formatting type string!")
		header = "*Type #" + str(typedata.id) + ":*\n"
		color = self.colorLookup[typedata.name]
		fallback = "Type information for " + typedata.name + "."

		## String formatting #pretty #print
		weaknessString    = "*Weaknesses*: "			+ self.stringBuilder(typedata.weaknesses)
		resistanceString  = "*Resistances*: "			+ self.stringBuilder(typedata.resistances)
		immunityString    = "*Immunities*: "			+ self.stringBuilder(typedata.immunities)
		resistedString    = "*Resisted by*: "			+ self.stringBuilder(typedata.halfDamageTo)
		ineffectiveString = "*Ineffective against*: "	+ self.stringBuilder(typedata.noDamageTo)

		responseString = weaknessString + resistanceString + immunityString + resistedString + ineffectiveString + "\n"

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

	def stringBuilder(self, mList):
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

	def help(self):
		""" Displays helpful information privately to the user on request """
		self.verboseprint("Oh snap! A user has request aid!")
		responseString = "*Help:*\n"

		fallBack = "Example usage: ----"
		helpString = "Example usage:\n */dex type [type]* \n"
		helpString += "*/dex type [type] silent* for a private query. This is hidden from the chat channel.\n"
		helpString += "For all queries [type] is interchangable with any type name or id, i.e grass or 12."
		
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
		return jsonify({"response_type": "ephemeral", "text": "Your query does not match any currently known pokemon, types or abilities! Try /dex help for more information."})
