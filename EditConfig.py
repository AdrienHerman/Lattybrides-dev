"""
Affichage du fichier de configuration.
HERMAN Adrien
06/02/2024
"""
"""
Exécution du script de génération de structure
via l'interface graphique.
HERMAN Adrien
06/02/2024
"""

# Modules de Python
from FreeCAD import Gui
import os, FreeCADGui

# Détection du dossier de travail
softpath = os.path.dirname(__file__)
iconPath = os.path.join(softpath, "icons")

class EditConfig_Class:
	"""
	Classe d'exécution du script de génération de la structure.
	"""

	def __init__(self):
		print("\n*** INITIALISATION DE LA CLASSE POUR L'AFFICHAGE DU FICHIER DE CONFIGURATION ***\n")

	def GetResources(self):
		return {
		"Pixmap": os.path.join(iconPath, "editicon.png"),
		"MenuText": "Afficher le fichier de configuration",
		"ToolTip": "Afficher le fichier de configuration pour la génération des structures.",
		}

	def Activated(self):
		FreeCADGui.open(softpath + "/config.py")

		return True

	def IsActive(self):
		return True

Gui.addCommand("EditConfig", EditConfig_Class())