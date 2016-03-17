# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from flask import jsonify
from classes.DatabaseHandler import DatabaseHandler

class PokedexRequestHandler:
	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None
		self.DB = DatabaseHandler(verbose)

		self.totalNumberOfPokemon = 721		## As of generation 6 XY/ORAS	
		self.totalNumberOfTypes = 18		## As of generation 6 XY/ORAS
		self.generationStartPokemon = [1, 152, 252, 387, 494, 650, 722]	# Gen1 - 7

	def handlePokedexRequest(self, text):
		""" handle pokedex requests """
		self.verboseprint("Handling a /pokedex or /dex request with text: " + text)
		return jsonify({"response_type": "in_channel", "text": "Handled a pokedex request asking for " + text})