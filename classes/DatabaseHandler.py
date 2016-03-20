# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/PokedexService/
import psycopg2
import os
from classes.Typedata import Typedata

class DatabaseHandler:
	""" Handles all things database """

	def __init__(self, verbose=False):
		""" Object model / Constructor """
		self.verboseprint = print if verbose else lambda *a, **k: None
		self.DBUser = ""
		self.DBPw = ""
		self.connection = None
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
			self.connection = psycopg2.connect(dbname='pokedex', user=self.DBUser, host='localhost', password=self.DBPw)
			self.verboseprint("Succesfully connected to database!")
			return True
		except psycopg2.Error as exception:
			self.verboseprint("ERROR: Unable to connect to the database!")
			self.verboseprint(exception)
			return False

	def deleteOccurence(self, typedata):
		""" Deletes an occurence of typedata from the database, if it exists """
		cursor = self.connection.cursor()
		SQL = "DELETE FROM types WHERE name=%s AND id=%s"
		data = [typedata.name, typedata.id]

		cursor.execute(SQL, data)
		self.connection.commit()
		cursor.close()

	def storeType(self, typedata):
		""" Stores a type with the provided information in the database """
		cursor = self.connection.cursor()
		SQL = """INSERT INTO types (id, name, immunities, 
		resistances, weaknesses, halfdamageto, nodamageto, updatetime) 
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
		# Is there a better way?	                                 
		data = [typedata.id, typedata.name, typedata.immunities, typedata.resistances, typedata.weaknesses,
				typedata.halfDamageTo, typedata.noDamageTo, typedata.updateTime]

		cursor.execute(SQL, data)
		self.connection.commit()
		cursor.close()

	def getAllKnownTypes(self):
		""" Returns a list of 'typedata' elements for all known types in the database """
		knownTypes = []

		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM types")
		temp = cursor.fetchall()

		# For each row, create a corresponding Typedata object. 
		for dbTuple in temp:
			knownType = Typedata()
			knownType.id, knownType.name, knownType.immunities, knownType.resistances, knownType.weaknesses, knownType.halfdamageto, knownType.nodamageto, knownType.updatetime = dbTuple
			knownTypes.append(knownType)

		return knownTypes

	def getAllKnownPokemon(self):
		""" Returns a dictionary of all known pokemon in the database """
		knownPokemon = []

		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM pokemon")
		temp = cursor.fetchall()

		#for dbTuple in temp:
		#	knownPokemon = Pokedata()

		return knownPokemon

	def getAllKnownAbilities(self):
		""" Returns a dictionary of all known abilities in the database """
		knownAbilities = []

		return knownAbilities