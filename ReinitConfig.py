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
import os

# Détection du dossier de travail
softpath = os.path.dirname(__file__)
iconPath = os.path.join(softpath, "icons")

class ReinitConfig_Class:
	"""
	Classe d'exécution du script de génération de la structure.
	"""

	def __init__(self):
		print("\n*** INITIALISATION DE LA CLASSE POUR L'AFFICHAGE DU FICHIER DE CONFIGURATION ***\n")

	def GetResources(self):
		return {
		"Pixmap": os.path.join(iconPath, "reiniticon.png"),
		"MenuText": "Réinitialisation du fichier de configuration",
		"ToolTip": "Réinitialisation du fichier de configuration aux paramètres par défaut.",
		}

	def Activated(self):
		file_config = open(softpath + "/config.py", "w")
		file_config_default = open(softpath + "/config_default.py", "r")

		for line in file_config_default:
			file_config.write(line)

		file_config_default.close()
		file_config.close()

		return True

	def IsActive(self):
		return True

Gui.addCommand("ReinitConfig", ReinitConfig_Class())