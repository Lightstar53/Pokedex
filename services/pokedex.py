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

	def handlePokedexRequest(self, text, response_url):
		""" Determine what kind of pokedex request is made, and delegate responsibility accordingly. """
		self.verboseprint("Handling a /dex request with text: " + text)
		if not self.DB.connectToDatabase():
			return jsonify({"response_type": "ephemeral", "text": "Database connection error. Alert admin. "})

		text = text.lower()
		if text == "help":			# Oh snap! A user needs help
			return self.help()

		# Split the input string on whitespace " ".
		textElements = text.split(" ")
		keyword = textElements[0]

		if keyword == keywords.pokeType.value:
			self.verboseprint("Keyword 'type' found!")
			return self.handleTypeRequest(textElements[1:])

		# Backup plan: 
		# We don't know it, pokeapi doesn't know it. It's probably not written correctly, or it is not relevant. 
		return self.errorReply()
	
	def handleTypeRequest(self, query):
		""" Handles any 'type' request. First we have to check if it is currently known by our DB.
			If it is known, we have to determine if the data is too old and has to be re-acquired """
		knownTypes = self.DB.getAllKnownTypes()
		self.verboseprint("Complete query: " + query[0])

		match = False
		## Check old data/reaquire
		for knownType in knownTypes:
			if query[0] == knownType['name'] or query[0] == knownType['id']:
				self.verboseprint("Typematch found!")
				match = True


		queryString = self.baseUrl + 'type/' + query[0]
		self.verboseprint("Querystring: " + queryString)
		## If no data has been found we need to query the API for potential new type (or BS)
		response = self.makePokeAPIRequest(queryString)

		if response != False: # We found something useful
			self.verboseprint(response)
			return jsonify({'resposne_type': 'in_channel', 'text': "*TEST* - Type id: " + str(response['id']) + ", Type name: " + response['name'] +", double damage from: " + str(response['damage_relations']['double_damage_from'])})			# Test

		return self.errorReply()


	def makePokeAPIRequest(self, queryString ):
		""" Makes a request to pokeAPI with given argument """
		response = requests.get(queryString).json()
		if 'detail' in response.keys() and response['detail'] == self.notFound:
			self.verboseprint("Seems to be a 404. ")
			return False

		return response

	def help(self):
		""" Displays helpful information privately to the user on request """
		self.verboseprint("Oh snap! A user has request aid!")
		responseString = "*Help:*\n"

		fallBack = "Example usage: To be continued..."
		helpString = "Example usage (try either):\n */who's* \n */that* \n */pokemon!?* \n"
		helpString += "It's PIKACHU\n"
		helpString += "For more detailed information please see the documentation page by clicking the title."
		
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
		return jsonify({"response_type": "in_channel", "text": "Your query does not match any currently known pokemon, types or abilities! Try /dex help for more information."})
