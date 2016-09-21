# Service listening on port 4000 for commands from post (slack "bots" or slash commands)
# The ServiceHandler delegates responsibility to the correct command handlers.

# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/
# Requires: requests, flask (python -m pip install requests) to install requests if necessary. 

from flask import Flask, request, jsonify
from PokedexService.classes.ServiceHandler import ServiceHandler

app = Flask(__name__)

import PokedexService.views
