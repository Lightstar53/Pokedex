# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from flask import jsonify, request
from services.pokedex import PokedexRequestHandler
from services.isitup import IsitupRequestHandler
import os

class ServiceHandler:
	""" Handles and delegates service requests """

	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None
		self.verboseprint("ServiceHandler initialized in verbose mode... (Consider setting app.py: verbose to false)")

		self.pokedexRequestHandler = PokedexRequestHandler(verbose=verbose)
		self.isitupRequestHandler = IsitupRequestHandler(verbose=verbose)

		## Valid tokens are loaded from .secret file using 'loadValidTokens()' to avoid making tokens public through version control. 
		self.VALID_TOKENS = []
		self.VALID_COMMANDS = ['/isitup', '/pokedex', '/dex']
		self.loadValidTokens()

		## Error 'codes'
		self.TOKEN_MISMATCH = 'tokenMismatch'
		self.INVALID_COMMAND = 'invalidCommand'
		self.verboseprint("Awaiting requests...")

	def loadValidTokens(self):		## Consider environment variable
		""" Loads valid tokens from validTokens.secret
		    format: token1,token2,token3,token4 etc."""
		self.verboseprint("Loading valid tokens...")

		thisDir = os.path.dirname(os.path.realpath('__file__'))
		fileName = os.path.join(thisDir, 'validTokens.secret')
		self.verboseprint("File path: " + fileName)

		## Make sure we can open the file
		try:
			file = open(fileName)
		except IOError as e:
			self.verboseprint("Could not open file!")
			self.verboseprint(e)

		## If file opened succesfully, append read tokens into valid token list
		with file:
			fileInput = file.read()
			file.close()
			tokens = fileInput.split(",")
			self.VALID_TOKENS = tokens

	def errorReply(self, errorType, command=None):
		""" Given an errortype and sometimes a command, returns the correct error response in JSON form """
		self.verboseprint("Returning custom error reply")
		if errorType == self.TOKEN_MISMATCH:
			return jsonify({"text": "ERROR: The team identifying token does not match."})
		elif errorType == self.INVALID_COMMAND:
			if command not in self.VALID_COMMANDS[1:]:
				return jsonify({"text": "ERROR: The command '" + command + "' is invalid, try /dex help or /pokedex help for more info"})
			elif command not in self.VALID_COMMANDS[:1]:
				return jsonify({"text": "ERROR: The command '" + command + "' is invalid, try /isitup help for more info"})

	def servePost(self, request):
		""" Retrieves and validates form information posted by slack bots """
		self.verboseprint("Serving post...")
		token = request.form['token']
		if token not in self.VALID_TOKENS:
			self.verboseprint("Mismatched token: " + token)
			self.verboseprint("VALID_TOKENS are: " + self.VALID_TOKENS)
			return errorReply(TOKEN_MISMATCH)

		return self.delegate(request.form['command'], request.form['text'], request.form['response_url'])

	def delegate(self, command, text, response_url):
		""" Delegates responsibility to the correct handler depending on command """
		self.verboseprint("Delegating...")
		if command == '/isitup':
			return self.isitupRequestHandler.handleIsitupRequest(text)
		elif command == '/pokedex':
			return self.pokedexRequestHandler.handlePokedexRequest(text, response_url)
		elif command == '/dex':
			return self.pokedexRequestHandler.handlePokedexRequest(text, response_url)
		else:
			self.verboseprint("Invalid command: " + command)
			return errorReply(INVALID_COMMAND)

	def serveGet(self, request):
		return """<html>
					<head>
						<title>Pokedexu</title>
					</head>
				    <body>
				      <h1>Pokedex</h1>
				      <p>Nothing to see here, use the slack bot.</p>
				      <p>Visit <a href="https://github.com/Sidaroth/PokedexService">https://github.com/Sidaroth/PokedexService</a> for more information</a>
				    </body>
				 </html>"""