# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/

from flask import jsonify
import requests

class IsitupRequestHandler:
	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None

	def help(self):
		""" Displays helpful information privately to the user on request """
		responseString = "*Help:*\n"

		fallBack = "Example usage: /isitup google.com, /isitup amazon.com, /isitup vg.no"
		helpString = "Example usage (try either):\n */isitup google.com* \n */isitup amazon.com* \n */isitup vg.no* \n"
		helpString += "Please make sure to include both *domain* (google) and *suffix* (.com)\n"
		helpString += "For more detailed information please see the documentation page by clicking the title."
		
		response = {
			"text": responseString,
			"attachments": [{
				"fallback": fallBack,				## Required
				"color": "good",					## Actually green
				"title": "Pokedex Service Documentation",
				"title_link": "https://github.com/Sidaroth/PokedexService",
				"text":	helpString,
				"mrkdwn_in": ["text"] 
			}],
			"response_type": "ephemeral"
		}

		return jsonify(response)

	## TODO: Try to add .com automagically if user forgets
	def handleIsitupRequest(self, url):
		""" handle isitup requests """
		self.verboseprint("Handling an /isitup request with input: " + url)

		if(url == 'help'):
			self.verboseprint("Help called.")
			return self.help()

		userAgent = "IsitupForSlackSlashCommand/1.0 (https://github.com/Sidaroth/PokedexService/)"
		headers = {
			'User-Agent': userAgent,
			'From': 'ymabob@gmail.com'
		}

		try:
			self.verboseprint("Initiating request...")
			queryUrl = "https://isitup.org/" + url + ".json"
			response = requests.get(queryUrl, headers=headers).json()
			responseString = ""

			self.verboseprint("Processing response...")
			self.verboseprint(response)
			if response['status_code'] == 1:
				responseString += "Yay, *" + url + "* appears to be *up!*"
				self.verboseprint("Successful response: " + responseString)
			elif response['status_code'] == 2:
				responseString += "Nope, *" + url + "* appears to be down!*"
				self.verboseprint("Negative response: " + responseString)
			elif response['status_code'] == 3:
				responseString += "Whoops, isitup.org does not think *" + url + "* is a valid website.\n"
				responseString += "Make sure you supply both the domain *AND* suffix (i.e github.com)"
				self.verboseprint("Invalid URL response: " + responseString)

			return jsonify({"response_type": "in_channel", "text": responseString})

		except requests.exceptions.RequestException as exception:
			self.verboseprint(exception)
			return jsonify({"text": "ERROR: RequestException (Enable verbose or debug for more information)"})
		