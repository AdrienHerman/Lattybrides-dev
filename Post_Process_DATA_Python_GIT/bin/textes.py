"""
Affiche la version du logiciel.
29/01/2024
HERMAN Adrien
"""

def version(tirets=True, center=True):
	"""
	Retourne la version du logiciel.

	-----------
	Variables :
		- tirets : True = Affiche les tirets sinon ne les affiche pas.
		- center : True = Centre lui-même le texte sinon ne le centre pas.
	-----------

	---------
	Retours :
		- str : Version du logiciel.
	---------
	"""

	string = "TDC - Traitement des Données de Crash\n"
	if center:	string += "           "
	string += "29/01/2024\n"
	if center:	string += "          "
	string += "HERMAN Adrien\n"
	if center:	string += "       "
	string += "Version 2.0 beta 1"
	
	if tirets:
		string = "-------------------------------------\n" + string + "\n-------------------------------------"

	return string

def texte_demarrage():
	"""
	Retourne le texte à afficher au démarrage du logiciel.

	---------
	Retours :
		- str : Texte au démarrage.
	---------
	"""
	
	string = """***************************************
=============   |==========   |========
      |         |         |   |
      |         |         |   |
      |         |         |   |
      |         |         |   |
      |         |         |   |
      |         |==========   |========
***************************************\n\n""" + version()

	return string