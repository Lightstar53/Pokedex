from PokedexService import app
from flask import request
from PokedexService.classes.ServiceHandler import ServiceHandler

@app.route("/", methods=['POST', 'GET'])
def run():
        serviceHandler = ServiceHandler();
        """ Posts/Gets to set-up '/' """
        ## POST / Bots
        if request.method == 'POST':
                return serviceHandler.servePost(request)

        ## GET / webpage
        elif request.method == 'GET':
                return serviceHandler.serveGet(request)

