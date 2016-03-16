# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from flask import jsonify

class PokedexRequestHandler:
	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None

	def handlePokedexRequest(self, text):
		""" handle pokedex requests """
		self.verboseprint("Handling a /pokedex or /dex request with text: " + text)
		return jsonify({"response_type": "in_channel", "text": "Handled a pokedex request"})