"""
Fonctions de déboggage
HERMAN Adrien
18/10/2023
"""

def wdebug(string_debug, file_debug):
	# Gestion du debuggage du code
	print(string_debug, end="")
	file_debug.write(string_debug)

def create_file_debug(debug_current_folder=True):
	# Importation des modules externes
	import datetime, os

	# Création du fichier de déboggage
	now = datetime.datetime.now()
	dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
	if debug_current_folder == True:
		debug_folder = os.getcwd()
	else:
		debug_folder = debug_current_folder
	nom_file_debug = debug_folder + dt_string + ".log"
	file_debug = open(nom_file_debug, "a")

	wdebug("-----------------------\n", file_debug)
	wdebug("--- Début Programme ---\n", file_debug)
	wdebug("-----------------------\n", file_debug)

	return file_debug