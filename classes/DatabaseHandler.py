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

	def loadDatabaseConnectionInfo(self):
		""" Reads database connection information from hidden file """	## Consider environment variable
		self.verboseprint("Loading DB Connection info...")

		fileLocation= os.path.join('classes/', 'dbInfo.secret')
		self.verboseprint("File: " + fileLocation)

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
			## Remove
			self.verboseprint("Read DB Info: " + self.DBUser + " - " + self.DBPw)

	def connectToDatabase(self):
		""" Establish a connection to the postgresql database """
		try:
			connection = psycopg2.connect(dbname='pokedex', user=self.DBUser, host='localhost', password=self.DBPw)
			self.verboseprint("Succesfully connected to database!")
		except psycopg2.Error as exception:
			self.verboseprint("ERROR: Unable to connect to the database!")
			self.verboseprint(exception)