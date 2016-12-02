# Author: Sidaroth
# Copyright: 2016 Christian Holt, ymabob@gmail.com
# Project: https://github.com/Sidaroth/Pokedex/
import psycopg2
import os
from PokedexService.classes.Typedata import Typedata
from PokedexService.classes.Pokedata import Pokedata
from PokedexService.classes.Movedata import Movedata
from PokedexService.classes.Abilitydata import Abilitydata

class DatabaseHandler:
	""" Handles all things database
		
		We want to cache data on our end to avoid taxing the servers (or wait for their reply).
	"""

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

		fileLocation = os.path.join('PokedexService/classes/', 'dbInfo.secret')
		file = None
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

	def deleteOccurence(self, data, occType):
		""" Deletes an occurence of typedata from the database, if it exists """
		cursor = self.connection.cursor()

		SQL = "DELETE FROM " + occType + " WHERE name=%s AND id=%s"

		data = [data.name, data.id]
		cursor.execute(SQL, data)
		self.connection.commit()
		cursor.close()

	def storeType(self, typedata):
		""" Stores a type with the provided information in the database """
		self.verboseprint("Storing type: '" + typedata.name + "' in DB")
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

	def storePokemon(self, pd):
		""" Stores a pokemon with the provided information in the database """
		self.verboseprint("Storing pokemon: '" + pd.name + "' in DB")
		cursor = self.connection.cursor()
		SQL = """INSERT INTO pokemon(id, name, sprite, types, weaknesses, immunities, resistances, hiddens, abilities, updatetime)
		VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

		data = [pd.id, pd.name, pd.sprite, pd.types, pd.weaknesses, pd.immunities,
		 		pd.resistances, pd.hiddenAbilities, pd.abilities, pd.updateTime]

		cursor.execute(SQL, data)
		self.connection.commit()
		cursor.close()

	def storeMove(self, md):
		""" Stores a move with the provided information in the database """
		self.verboseprint("Storing move '" + md.name + "' in DB")
		cursor = self.connection.cursor()
		SQL = """INSERT INTO moves(id, name, type, target, power, accuracy, basePP, critRate, flavorText, updateTime)
				 VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """
		data = [md.id, md.name, md.type, md.target, md.power, 
				md.accuracy, md.basePP, md.critRate, md.flavorText, md.updateTime]

		cursor.execute(SQL, data)
		self.connection.commit()
		cursor.close()

	def storeAbility(self, ad):
		""" Stores an ability with the provided information in the database """
		self.verboseprint("Storing ability '" + ad.name + "' in DB")
		cursor = self.connection.cursor()
		SQL = """INSERT INTO abilities(id, name, flavorText, updateTime)
				 VALUES (%s, %s, %s, %s); """
		data = [ad.id, ad.name, ad.flavorText, ad.updateTime]
		cursor.execute(SQL, data)
		self.connection.commit()
		cursor.close()

	def getAllKnownTypes(self):
		""" Returns a list of 'typedata' objects for all known types in the database """
		knownTypes = []

		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM types")
		temp = cursor.fetchall()

		# For each row, create a corresponding Typedata object with a long ass tuple unpack. 
		for dbTuple in temp:
			known = Typedata()
			known.id, known.name, known.immunities, known.resistances, known.weaknesses, known.halfDamageTo, known.noDamageTo, known.updateTime = dbTuple
			knownTypes.append(known)

		return knownTypes

	def getAllKnownPokemon(self):
		""" Returns a list of 'pokedata' objects for all known pokemon in the database """
		knownPokemon = []

		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM pokemon")
		temp = cursor.fetchall()

		# For each row, create a corresponding pokedata object with a long ass tuple unpack.
		for dbTuple in temp:
			known = Pokedata()
			known.id, known.name, known.sprite, known.types, known.weaknesses, known.immunities, known.resistances, known.hiddenAbilities, known.abilities, known.updatetime = dbTuple
			known.name = known.name.lower();
			knownPokemon.append(known)

		return knownPokemon

	def getAllKnownAbilities(self):
		""" Returns a list of 'Abilitydata' objects for all known abilities in the DB """
		knownAbilities = []

		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM abilities")
		temp = cursor.fetchall()

		for dbTuple in temp:		## unpack results
			known = Abilitydata()
			known.id, known.name, known.flavorText, known.updateTime = dbTuple
			known.name.lower()
			knownAbilities.append(known)

		return knownAbilities

	def getAllKnownMoves(self):
		""" Returns a list of 'Movedata' objects for all known moves in the database """
		knownMoves = []
		
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM moves")
		temp = cursor.fetchall()

		for dbTuple in temp:		## unpack results
			known = Movedata()
			known.id, known.name, known.type, known.target, known.power, known.accuracy, known.basePP, known.critRate, known.flavorText, known.updateTime = dbTuple
			known.name.lower()
			knownMoves.append(known)

		return knownMoves
