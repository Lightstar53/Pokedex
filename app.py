# Service listening on port 4000 for commands from post (slack "bots" or slash commands)
# The ServiceHandler delegates responsibility to the correct command handlers.

# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/
# Requires: requests, flask (python -m pip install requests) to install requests if necessary. 

from flask import Flask, request, jsonify
from classes.ServiceHandler import ServiceHandler

DEBUG = False			## Potentially take these as CL arguments
VERBOSE = True			## 

app = Flask(__name__)


@app.route("/github", methods=['POST'])
def pull():
	""" Github """
	payload = request.form['payload']
	print(payload)



@app.route("/", methods=['POST', 'GET'])
def run():
	""" Posts/Gets to holt.0x.no/slack/PokedexService """
	## POST / Bots
	if request.method == 'POST':
		return serviceHandler.servePost(request)			

	## GET / webpage
	elif request.method == 'GET':
		return serviceHandler.serveGet(request)

if __name__ == "__main__":
	serviceHandler = ServiceHandler(verbose=VERBOSE)
	app.run(port=4000, debug=DEBUG)