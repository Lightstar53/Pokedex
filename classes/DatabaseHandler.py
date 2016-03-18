# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/
import psycopg2
import os

class DatabaseHandler:
	""" Handles all things database """

	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None
		self.DBUser = ""
		self.DBPw = ""
		self.loadDatabaseConnectionInfo()

		self.typeTableHeaders = ['id', 'name', 'immunities', 'resistances', 'weaknesses', 'halfdamageto', 'nodamageto', 'updatetime']


	def loadDatabaseConnectionInfo(self):
		""" Reads database connection information from hidden file """	## Consider environment variable
		self.verboseprint("Loading DB Connection info...")

		fileLocation= os.path.join('classes/', 'dbInfo.secret')

		try:
			file = open(fileLocation)
		except IOError as e:
			self.verboseprint("Could not open file!")
			self.verboseprint(e)

		with file:
			fileInput = file.read().split(",")
			file.close()
			self.DBUser = fileInput[0]
			self.DBPw = fileInput[1]

	def connectToDatabase(self):
		""" Establish a connection to the postgresql database """
		try:
			connection = psycopg2.connect(dbname='pokedex', user=self.DBUser, host='localhost', password=self.DBPw)
			self.verboseprint("Succesfully connected to database!")
			return True
		except psycopg2.Error as exception:
			self.verboseprint("ERROR: Unable to connect to the database!")
			self.verboseprint(exception)
			return False


	## These will return a list dictionaries of known types [{'name': normal, 'id': 1}, ...]
	def getAllKnownTypes(self):
		""" Returns the name and id of all known types in the database """
		return []

	def getAllKnownPokemon(self):
		""" Returns the name and id of all known pokemon in the database """
		return []

	def getAllKnownAbilities(self):
		""" Returns the name and id of all known abilities in the database """
		return []