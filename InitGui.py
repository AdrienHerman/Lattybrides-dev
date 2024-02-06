"""
Fichier d'intégration du script à l'interface graphique de FreeCAD
HERMAN Adrien
06/02/2024
"""

# Modules de Python
from FreeCAD import Gui
import os

# Détection du dossier de travail
import soft_path
softpath = os.path.dirname(soft_path.__file__)
softicon = os.path.join(os.path.join(softpath, "icons"), "softicon.png")

class Lattybrides(Workbench):
	"""
	Objet d'intégration du script à l'interface graphique de FreeCAD.
	"""

	global softpath
	global softicon

	MenuText = "Lattybrides"
	ToolTip = "Génération de structures lattices hybrides à gradients de réseau."
	Icon = softicon

	def Initialize(self):
		# Modules du Logiciel
		import EXEC, ReinitConfig, EditConfig

		self.list = [	"EXEC",
						"EditConfig",
						"ReinitConfig"]
		self.appendToolbar("Exécuter la Génération de Structure", self.list)
		self.appendMenu("Lattybrides", self.list)

	def Activated(self):
		return

	def Deactivated(self):
		return

	def ContextMenu(self, recipient):
		self.appendContextMenu("Lattybrides", self.list) # add commands to the context menu

	def GetClassName(self):
		return "Gui::PythonWorkbench"
	   
Gui.addWorkbench(Lattybrides())