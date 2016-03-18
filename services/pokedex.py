# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from flask import jsonify
from classes.DatabaseHandler import DatabaseHandler
from enum import Enum, unique
import requests

@unique
class queryType(Enum):
	""" Enumerator for query types. @unique guarantees unique values. """
	unknown = 0
	pokeType = 1
	pokemon = 2
	ability = 3


class PokedexRequestHandler:
	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None
		self.DB = DatabaseHandler(verbose)

		self.DataValidity = 14				## Number of days data is valid before re-retrieving
		self.totalNumberOfPokemon = 721		## As of generation 6 XY/ORAS	
		self.totalNumberOfTypes = 18		## As of generation 6 XY/ORAS
		self.generationStartPokemon = [1, 152, 252, 387, 494, 650, 722]	# Gen1 - 7
		self.notFound = 'Not found.'

	def handlePokedexRequest(self, text, response_url):
		""" handle pokedex requests """
		self.verboseprint("Handling a /dex request with text: " + text)
		if not self.DB.connectToDatabase():
			return jsonify({"response_type": "ephemeral", "text": "Database connection error. Alert admin. "})

		if text.lower() == "help":			# Oh snap! A user needs help
			return self.help()

		text = text.lower()
		query = self.determineQueryType(text)
		
		if query == queryType.pokeType:								## Known type 
			return self.handleKnownType(text)
		elif query == queryType.pokemon:							## Known pokemon
			return self.handleKnownPokemon(text)
		elif query == queryType.ability:							## Known ability
			return self.handleKnownAbility(text)
		elif query == queryType.unknown:							# You're a pokemon master, you discovered a new ability/type/pokemon, legendary!
			return self.handleUnknown(text, response_url)

	def determineQueryType(self, text):
		""" Determine if the input text is known """
		self.verboseprint("Checking query type...")	

		for pokeType in self.DB.getAllKnownTypes():
			if pokeType['name'] == text or str(pokeType['id']) == text:
				return queryType.pokeType
		
		for pokemon in self.DB.getAllKnownPokemon():
			if pokemon['name'] == text or str(pokemon['id']) == text:
				self.verboseprint(pokemon)
				return queryType.pokemon

		for ability in self.DB.getAllKnownAbilities():
			if ability['name'] == text or str(ability['id']) == text:
				return queryType.ability

		return queryType.unknown

	def retrieveInformation(self, text, query=queryType.unknown):
		""" Determines what type of request to make """
		baseUrl = "http://pokeapi.co/api/v2/"

		# TODO
		# Needs the original requests response_url to send a delayed answer. 
		# PokeAPI is slow, 3000ms is not enough to avoid timeout when running several requests.

		if query == queryType.unknown:
			self.verboseprint("Handling an unknown query")
			## Is it recognized as a pokemon?
			queryString = baseUrl + 'pokemon/' + str(text)
			response = self.makePokeAPIRequest(queryString)
			if response != False:
				return response

			## Is it recognized as a type?
			queryString = baseUrl + 'type/' + str(text)
			response = self.makePokeAPIRequest(queryString)
			if response != False:
				return response
			## Is it recognized as an ability?
			queryString = baseUrl + 'ability/' + str(text)
			response = self.makePokeAPIRequest(queryString)
			if response != False:
				return response

			return False

		## Future?
		#elif query == queryType.pokeType:
		#	queryString = baseUrl + 'type/' + str(text)
		#elif query == queryType.pokemon:
		#	queryString = baseUrl + 'pokemon/' + str(text)
		#elif query == queryType.ability:
		#	queryString = baseUrl + 'ability/' + str(text)


	def makePokeAPIRequest(self, queryString ):
		""" Makes a request to pokeAPI with given argument """
		response = requests.get(queryString).json()
		if 'detail' in response.keys() and response['detail'] == self.notFound:
			self.verboseprint("Seems to be a 404. ")
			return False

		return response


	def handleKnownType(self, text):
		""" This type is already in our database, determine if old information is valid (how recent is it?) or retrieve new. """

	def handleKnownPokemon(self, text):
		""" This pokemon is already in our database, determine if old information is valid (how recent is it?) or retrieve new. """
		self.verboseprint("We found a known pokemon!")
		return jsonify({"response_type": "in_channel", "text": "Your query *" + text + "* matches a known pokemon! (TEST)"})
	
	def handleKnownAbility(self, text):
		""" This ability is already in our database, determine if old information is valid (how recent is it?) or retrieve new. """


	def handleUnknown(self, text, response_url):
		""" Determine if this is a newly discovered pokemon, type, or ability, or if it is just a user error. """
		response = self.retrieveInformation(text)
		if response != False:
			self.verboseprint("We actually found something...")
			return jsonify({"response_type": "in_channel", "text": "Your query *" + text + "* Amazingly matched something online. "})

		# We don't know it, pokeapi doesn't know it. It's probably not written correctly, or is not relevant. 
		return jsonify({"response_type": "in_channel", "text": "Your query *" + text + "* does not match any currently known pokemon, types or abilities! Try /dex help for more information."})

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
