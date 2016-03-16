# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from flask import jsonify

class IsitupRequestHandler:
	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None

	def handleIsitupRequest(self, text):
		""" handle isitup requests """
		self.verboseprint("Handling an /isitup request with text: " + text)
		return jsonify({"response_type": "in_channel", "text": "Handled an isitup request"})