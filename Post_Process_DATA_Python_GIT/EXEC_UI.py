"""
Corps principal de l'application avec interface graphique.
HERMAN Adrien
22/01/2024

pyuic6 UI/MainWindow.ui -o UI/MainWindowUI.py
"""

# Modules de Python
import sys, datetime
from PyQt6.QtWidgets import (
	QApplication, QDialog, QMainWindow, QFileDialog, QPushButton, QMessageBox
)
from PyQt6.QtGui import QKeySequence

# Modules du Logiciel
from UI.MainWindowUI import Ui_MainWindow
from bin.lecture_param import *
from bin.lecture_ecriture_donnees import *

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		"""
		Initialisation de l'objet fenêtre
		"""

		super().__init__(parent)
		self.setupUi(self)              # Lancement de la fenêtre
		self.connectSignalsSlots()      # Connexion des signaux

	def connectSignalsSlots(self):
		"""
		Connexion de tous les signaux et slots de la fenêtre
		"""

		# Action d'activer / désactiver les éléments pour superposer_courbes
		self.checkBox_superposer_courbes.stateChanged.connect(self.checkBox_stateChanged_superposer_courbes)

		# Action d'activer / désactiver les éléments pour type_fichier
		self.comboBox_type_fichier.currentTextChanged.connect(self.comboBox_currentTextChanged_type_fichier)

		# Action d'activer / désactiver les éléments pour enregistrer_data
		self.checkBox_enregistrer_data.stateChanged.connect(self.checkBox_stateChanged_enregistrer_data)

		# Action d'activer / désactiver les éléments pour recherche_deb_impact
		self.checkBox_recherche_deb_impact.stateChanged.connect(self.checkBox_stateChanged_recherche_deb_impact)

		# Action d'activer / désactiver les éléments pour deb_impact_manuel
		self.checkBox_deb_impact_manuel.stateChanged.connect(self.checkBox_stateChanged_deb_impact_manuel)

		# Action d'activer / désactiver les éléments pour checkBox_detect_fin_essai
		self.checkBox_detect_fin_essai.stateChanged.connect(self.checkBox_stateChanged_detect_fin_essai)

		# Action d'activer / désactiver les éléments pour checkBox_detect_fin_essai
		self.checkBox_calculer_energie.stateChanged.connect(self.checkBox_stateChanged_calculer_energie)
		
		# Action d'activer / désactiver les éléments pour checkBox_detect_fin_essai
		self.checkBox_calc_vitesse_impact.stateChanged.connect(self.checkBox_stateChanged_calc_vitesse_impact)

		# Charger la configuration par défaut dans la fenêtre
		self.pushButton_Defaults.clicked.connect(lambda: self.load_config())

		# Bouton "Quitter le Logiciel"
		self.pushButton_Quit.clicked.connect(self.close)

		# Bouton "Effacer les Messages du Terminal"
		self.pushButton_effacer_terminal.clicked.connect(lambda: self.textEdit_terminal.clear())

		# Bouton "Générer "config.txt""
		self.pushButton_MakeConfig.clicked.connect(self.pushButton_clicked_MakeConfig)

		# Bouton "Parcourir" pour nom_fichier
		self.pushButton_nom_fichier.clicked.connect(self.pushButton_clicked_nom_fichier)

		# Bouton "Parcourir" pour nom_dossier
		self.pushButton_nom_dossier.clicked.connect(self.pushButton_clicked_nom_dossier)

		# Bouton "Parcourir" pour enregistrer_data
		self.pushButton_parcourir_enregistrement.clicked.connect(self.pushButton_clicked_parcourir_enregistrement)

		# Actions du menu Fichiers
		#   Quitter le logiciel
		self.actionQuitter.triggered.connect(self.close)
		self.actionQuitter.setShortcut(QKeySequence("Ctrl+Q"))
		#   Ouvrir un fichier de configuration
		self.actionOuvrir_un_fichier_de_configuration.triggered.connect(self.actionOuvrir_trigger_un_fichier_de_configuration)
		self.actionOuvrir_un_fichier_de_configuration.setShortcut(QKeySequence("Ctrl+O"))

	def changeEnabled(self, list_objects, state):
		"""
		Action d'activer / désactiver une liste d'objets
		"""
		
		for o in list_objects:  o.setEnabled(state)

	def checkBox_stateChanged_superposer_courbes(self):
		"""
		Action d'activer / désactiver les éléments pour superposer_courbes
		"""

		# Récupération de l'état de la checkbox
		state = self.checkBox_superposer_courbes.isChecked()

		# Paramétrage de l'activation / désactivation
		if state:
			list_objects = [self.label_nom_fichier,
							self.lineEdit_nom_fichier,
							self.pushButton_nom_fichier]

			self.changeEnabled(list_objects, False)

			list_objects = [self.label_nom_dossier,
							self.lineEdit_nom_dossier,
							self.pushButton_nom_dossier]

			self.changeEnabled(list_objects, True)

		else:
			list_objects = [self.label_nom_fichier,
							self.lineEdit_nom_fichier,
							self.pushButton_nom_fichier,
							self.label_nom_dossier,
							self.lineEdit_nom_dossier]

			self.changeEnabled(list_objects, True)

			list_objects = [self.pushButton_nom_dossier]

			self.changeEnabled(list_objects, False)

	def comboBox_currentTextChanged_type_fichier(self):
		"""
		Action d'activer / désactiver les éléments pour type_fichier
		"""

		# Récupération de l'état de la combobox
		current_text = self.comboBox_type_fichier.currentText()

		if current_text == "CSV":   state = True
		else:                       state = False

		# Paramétrage de l'activation / désactivation
		list_objects = [self.groupBox_enregistrement_donnees,
						self.groupBox_traitement_donnees]

		self.changeEnabled(list_objects, state)

	def checkBox_stateChanged_enregistrer_data(self):
		"""
		Action d'activer / désactiver les éléments pour enregistrer_data
		"""

		# Récupération de l'état de la checkbox
		state = self.checkBox_enregistrer_data.isChecked()

		# Paramétrage de l'activation / désactivation
		list_objects = [self.label_nom_enregistrement,
						self.label_dossier_enregistrement,
						self.lineEdit_nom_enregistrement,
						self.lineEdit_dossier_enregistrement,
						self.pushButton_parcourir_enregistrement]

		self.changeEnabled(list_objects, state)

	def checkBox_stateChanged_recherche_deb_impact(self):
		"""
		Action d'activer / désactiver les éléments pour recherche_deb_impact
		"""

		# Liste des objets à activer / désactiver
		list_objects = [self.label_taux_augmentation,
						self.doubleSpinBox_taux_augmentation,
						self.label_nb_pas_avant_augmentation,
						self.spinBox_nb_pas_avant_augmentation]

		# Activer / Désactiver les objets
		self.changeEnabled(list_objects, self.checkBox_recherche_deb_impact.isChecked())

	def checkBox_stateChanged_deb_impact_manuel(self):
		"""
		Action d'activer / désactiver les éléments pour recherche_deb_impact
		"""

		# Liste des objets à activer / désactiver
		list_objects = [self.doubleSpinBox_tmps_deb_impact]

		# Activer / Désactiver les objets
		self.changeEnabled(list_objects, self.checkBox_deb_impact_manuel.isChecked())

	def checkBox_stateChanged_detect_fin_essai(self):
		"""
		Action d'activer / désactiver les éléments pour detect_fin_essai
		"""

		# Liste des objets à activer / désactiver
		list_objects = [self.label_dep_max,
						self.doubleSpinBox_dep_max]

		# Activer / Désactiver les objets
		self.changeEnabled(list_objects, self.checkBox_detect_fin_essai.isChecked())

	def checkBox_stateChanged_calculer_energie(self):
		"""
		Action d'activer / désactiver les éléments pour calculer_energie
		"""

		# Liste des objets à activer / désactiver
		list_objects = [self.label_fact_force,
						self.doubleSpinBox_fact_force,
						self.label_fact_dep,
						self.doubleSpinBox_fact_dep]

		# Activer / Désactiver les objets
		self.changeEnabled(list_objects, self.checkBox_calculer_energie.isChecked())

	def checkBox_stateChanged_calc_vitesse_impact(self):
		"""
		Action d'activer / désactiver les éléments pour calc_vitesse_impact
		"""

		# Liste des objets à activer / désactiver
		list_objects = [self.label_nbpts_vitesse_impact,
						self.spinBox_nbpts_vitesse_impact]

		# Activer / Désactiver les objets
		self.changeEnabled(list_objects, self.checkBox_calc_vitesse_impact.isChecked())

	def textEdit_terminal_addText(self, text):
		"""
		Ajouter du texte dans le terminal (en noir).

		-----------
		Variables :
			- text : Texte à afficher dans le terminal.
		-----------
		"""

		date = datetime.datetime.now()
		
		try:
			self.textEdit_terminal.append("<span style=\" color:black;\" >[" + str(date.day) + "/" + str(date.month) + "/" + str(date.year) + " " + str(date.hour) + ":" + str(date.minute) + "] </span><span style=\" color:black;\" >" + text + "</span>")

		except:
			self.textEdit_terminal_addError("ERREUR : Format du texte reçu par le terminal incorrect !")

	def textEdit_terminal_addWarning(self, text):
		"""
		Ajouter des warnings dans le terminal (en orange).

		-----------
		Variables :
			- text : Texte à afficher dans le terminal.
		-----------
		"""

		date = datetime.datetime.now()
		
		try:
			self.textEdit_terminal.append("<span style=\" color:black;\" >[" + str(date.day) + "/" + str(date.month) + "/" + str(date.year) + " " + str(date.hour) + ":" + str(date.minute) + "] </span><span style=\" color:orange;\" >" + text + "</span>")

		except:
			self.textEdit_terminal_addError("ERREUR : Format du texte reçu par le terminal incorrect !")

	def textEdit_terminal_addError(self, text):
		"""
		Ajouter des erreurs dans le terminal (en rouge).

		-----------
		Variables :
			- text : Texte à afficher dans le terminal.
		-----------
		"""

		date = datetime.datetime.now()
		
		try:
			self.textEdit_terminal.append("<span style=\" color:black;\" >[" + str(date.day) + "/" + str(date.month) + "/" + str(date.year) + " " + str(date.hour) + ":" + str(date.minute) + "] </span><span style=\" color:red;\" ><b>" + text + "</b></span>")

		except:
			self.textEdit_terminal_addError("ERREUR : Format du texte reçu par le terminal incorrect !")

	def pushButton_clicked_MakeConfig(self):
		"""
		Enregistrer la configuration.
		"""

		# Récupérer le dossier
		folder = self.open_folder_dialog()

		if folder:
			# superposer_courbes, nom_fichier, nom_dossier
			superposer_courbes = self.checkBox_superposer_courbes.isChecked()
			nom_fichier = self.lineEdit_nom_fichier.text()
			nom_dossier = self.lineEdit_nom_dossier.text()

			# type_fichier
			type_fichier = self.comboBox_type_fichier.currentText()

			# calc_temps
			calc_temps = self.checkBox_calc_temps.isChecked()

			# enregistrer_data, nom_enregistrement, dossier_enregistrement
			enregistrer_data = self.checkBox_enregistrer_data.isChecked()
			nom_enregistrement = self.lineEdit_nom_enregistrement.text()
			dossier_enregistrement = self.lineEdit_dossier_enregistrement.text()

			# suppr_rollback
			suppr_rollback = self.checkBox_suppr_rollback.isChecked()

			# recherche_deb_impact, taux_augmentation, nb_pas_avant_augmentation
			recherche_deb_impact = self.checkBox_recherche_deb_impact.isChecked()
			taux_augmentation = self.doubleSpinBox_taux_augmentation.value()
			nb_pas_avant_augmentation = self.spinBox_nb_pas_avant_augmentation.value()

			# deb_impact_manuel, tmps_deb_impact
			deb_impact_manuel = self.checkBox_deb_impact_manuel.isChecked()
			tmps_deb_impact = self.doubleSpinBox_tmps_deb_impact.value()

			# tarrage_dep, tarrage_tmps
			tarrage_dep = self.checkBox_tarrage_dep.isChecked()
			tarrage_tmps = self.checkBox_tarrage_tmps.isChecked()

			# detect_fin_essai, dep_max
			detect_fin_essai = self.checkBox_detect_fin_essai.isChecked()
			dep_max = self.doubleSpinBox_dep_max.value()

			# calculer_energie, fact_force, fact_dep
			calculer_energie = self.checkBox_calculer_energie.isChecked()
			fact_force = self.doubleSpinBox_fact_force.value()
			fact_dep = self.doubleSpinBox_fact_dep.value()

			# calc_vitesse_impact, nbpts_vitesse_impact
			calc_vitesse_impact = self.checkBox_calc_vitesse_impact.isChecked()
			nbpts_vitesse_impact = self.spinBox_nbpts_vitesse_impact.value()

			# afficher_dep_tmps, afficher_F_tmps, afficher_F_dep, afficher_sep
			afficher_dep_tmps = self.checkBox_afficher_dep_tmps.isChecked()
			afficher_F_tmps = self.checkBox_afficher_F_tmps.isChecked()
			afficher_F_dep = self.checkBox_afficher_F_dep.isChecked()
			afficher_sep = self.checkBox_afficher_sep.isChecked()

			enregistrer_configuration(	folder=folder,
										QWindow=self,
										conf={	"superposer_courbes":superposer_courbes,
												"nom_fichier":nom_fichier,
												"nom_dossier":nom_dossier,
												"type_fichier":type_fichier,
												"calc_temps":calc_temps,
												"enregistrer_data":enregistrer_data,
												"nom_enregistrement":nom_enregistrement,
												"dossier_enregistrement":dossier_enregistrement,
												"suppr_rollback":suppr_rollback,
												"recherche_deb_impact":recherche_deb_impact,
												"taux_augmentation":taux_augmentation,
												"nb_pas_avant_augmentation":nb_pas_avant_augmentation,
												"deb_impact_manuel":deb_impact_manuel,
												"tmps_deb_impact":tmps_deb_impact,
												"tarrage_dep":tarrage_dep,
												"tarrage_tmps":tarrage_tmps,
												"detect_fin_essai":detect_fin_essai,
												"dep_max":dep_max,
												"calculer_energie":calculer_energie,
												"fact_force":fact_force,
												"fact_dep":fact_dep,
												"calc_vitesse_impact":calc_vitesse_impact,
												"nbpts_vitesse_impact":nbpts_vitesse_impact,
												"afficher_dep_tmps":afficher_dep_tmps,
												"afficher_F_tmps":afficher_F_tmps,
												"afficher_F_dep":afficher_F_dep,
												"afficher_sep":afficher_sep})

	def pushButton_clicked_nom_fichier(self):
		"""
		Parcourir le chemin d'un fichier de courbe.
		"""

		# Récupérer le fichier
		file = self.open_file_dialog(fileType="Fichiers Bruts CSV (*.CSV *.csv);;Fichiers Traités TXT (*.TXT *.txt)")

		try:
			# Récupération du nom du fichier et du chemin
			fileName = file.split("/")[-1]
			filePath = '/'.join(file.split("/")[:(len(file.split("/")) - 1)])

			# Ajout du chemin dans la fenêtre
			self.lineEdit_nom_fichier.setText(fileName)
			self.lineEdit_nom_dossier.setText(filePath)

		except:
			self.textEdit_terminal_addError("ERREUR : Impossible de lire le fichier !")

	def pushButton_clicked_nom_dossier(self):
		"""
		Parcourir le chemin d'un dossier de courbe.
		"""

		# Récupérer le dossier
		folder = self.open_folder_dialog()

		# Ajout du chemin dans la fenêtre
		if folder:	self.lineEdit_nom_dossier.setText(folder)

	def pushButton_clicked_parcourir_enregistrement(self):
		"""
		Parcourir le chemin de sauvegarde d'une courbe.
		"""

		# Récupérer le fichier
		file = self.save_file_dialog()

		try:
			# Récupération du nom du fichier et du chemin
			fileName = file.split("/")[-1]
			filePath = '/'.join(file.split("/")[:(len(file.split("/")) - 1)])

			# Ajout du chemin dans la fenêtre
			self.lineEdit_nom_enregistrement.setText(fileName)
			self.lineEdit_dossier_enregistrement.setText(filePath)

		except:
			self.textEdit_terminal_addError("ERREUR : Impossible de lire le fichier !")

	def actionOuvrir_trigger_un_fichier_de_configuration(self):
		"""
		Ouvrir et charger un fichier de configuration à partir du menu.
		"""

		file = self.open_file_dialog()
		
		if not file:
			self.textEdit_terminal_addError("ERREUR : Impossible de charger le fichier de configuration !")

		else:
			self.load_config(file)

	def load_config(self, path_config="config_default.conf"):
		"""
		Charger la configuration d'un fichier de configuration dans la fenêtre

		-----------
		Variables :
			- path_config : Chemin vers le fichier de configuration
		-----------
		"""
		
		return_list = lecture_param(path_config=path_config, QWindow=self)

		if None in return_list:
			self.textEdit_terminal_addError("ERREUR : Impossible de lire le fichier de configuration par défaut !")

		else:
			[   type_fichier,
				superposer_courbes,
				nom_fichier,
				nom_dossier,
				calc_temps,
				enregistrer_data,
				nom_enregistrement,
				dossier_enregistrement,
				sppr_rollback,
				recherche_deb_impact,
				deb_impact_manuel,
				tmps_deb_impact,
				tarrage_dep,
				tarrage_tmps,
				detect_fin_essai,
				dep_max,
				calculer_energie,
				fact_force,
				fact_dep,
				taux_augmentation,
				nb_pas_avant_augmentation,
				calc_vitesse_impact,
				nbpts_vitesse_impact,
				afficher_dep_tmps,
				afficher_F_tmps,
				afficher_F_dep,
				afficher_sep] = return_list

			# superposer_courbes, nom_fichier, nom_dossier
			self.checkBox_superposer_courbes.setChecked(superposer_courbes)
			self.lineEdit_nom_fichier.setText(nom_fichier)
			self.lineEdit_nom_dossier.setText(nom_dossier)

			# type_fichier
			self.comboBox_type_fichier.setCurrentText(type_fichier.upper())

			# calc_temps
			self.checkBox_calc_temps.setChecked(calc_temps)

			# enregistrer_data, nom_enregistrement, dossier_enregistrement
			self.checkBox_enregistrer_data.setChecked(enregistrer_data)
			self.lineEdit_nom_enregistrement.setText(nom_enregistrement)
			self.lineEdit_dossier_enregistrement.setText(dossier_enregistrement)

			# suppr_rollback
			self.checkBox_suppr_rollback.setChecked(sppr_rollback)

			# recherche_deb_impact, taux_augmentation, nb_pas_avant_augmentation
			self.checkBox_recherche_deb_impact.setChecked(recherche_deb_impact)
			self.doubleSpinBox_taux_augmentation.setValue(taux_augmentation)
			self.spinBox_nb_pas_avant_augmentation.setValue(nb_pas_avant_augmentation)

			# deb_impact_manuel, tmps_deb_impact
			self.checkBox_deb_impact_manuel.setChecked(deb_impact_manuel)
			self.doubleSpinBox_tmps_deb_impact.setValue(tmps_deb_impact)

			# tarrage_dep, tarrage_tmps
			self.checkBox_tarrage_dep.setChecked(tarrage_dep)
			self.checkBox_tarrage_tmps.setChecked(tarrage_tmps)

			# detect_fin_essai, dep_max
			self.checkBox_detect_fin_essai.setChecked(detect_fin_essai)
			self.doubleSpinBox_dep_max.setValue(dep_max)

			# calculer_energie, fact_force, fact_dep
			self.checkBox_calculer_energie.setChecked(calculer_energie)
			self.doubleSpinBox_fact_force.setValue(fact_force)
			self.doubleSpinBox_fact_dep.setValue(fact_dep)

			# calc_vitesse_impact, nbpts_vitesse_impact
			self.checkBox_calc_vitesse_impact.setChecked(calc_vitesse_impact)
			self.spinBox_nbpts_vitesse_impact.setValue(nbpts_vitesse_impact)

			# afficher_dep_tmps, afficher_F_tmps, afficher_F_dep
			self.checkBox_afficher_dep_tmps.setChecked(afficher_dep_tmps)
			self.checkBox_afficher_F_tmps.setChecked(afficher_F_tmps)
			self.checkBox_afficher_F_dep.setChecked(afficher_F_dep)
			self.checkBox_afficher_sep.setChecked(afficher_sep)

	def save_file_dialog(self, folderName="", fileType="Fichiers Traités TXT (*.TXT *.txt)"):
		"""
		Ouvrir une fenêtre de sauvegarde de fichiers.

		-----------
		Variables :
			- folderName : Chemin où ouvrir la fenêtre de sélection de fichiers.
			- fileType : Types de fichiers acceptés par la sélection.
		-----------
		"""

		fileName, _ = QFileDialog.getSaveFileName(self, "Sauvegarder les Courbes", folderName, fileType)

		if fileName:
			return fileName

		else:
			self.textEdit_terminal_addWarning("WARNING : Le sélecteur de fichier ne s'est pas exécuté correctement !")

	def open_file_dialog(self, folderName="", fileType="Configuration File (*.conf)"):
		"""
		Ouvrir une fenêtre de sélection de fichiers.

		-----------
		Variables :
			- folderName : Chemin où ouvrir la fenêtre de sélection de fichiers.
			- fileType : Types de fichiers acceptés par la sélection.
		-----------
		"""

		dialog = QFileDialog()
		dialog.setNameFilter(fileType)
		dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
		dialog.setDirectory(folderName)

		if dialog.exec():
			if len(dialog.selectedFiles()) != 0:
				return dialog.selectedFiles()[0]

			else:
				self.textEdit_terminal_addError("ERREUR : Aucun fichier sélectionné !")
		else:
			self.textEdit_terminal_addWarning("WARNING : Le sélecteur de fichier ne s'est pas exécuté correctement !")
			return False

	def open_folder_dialog(self, folderName=""):
		"""
		Ouvrir une fenêtre de sélection de dossier.

		-----------
		Variables :
			- folderName : Chemin où ouvrir la fenêtre de sélection de fichiers.
		-----------
		"""

		dialog = QFileDialog()
		dialog.setFileMode(QFileDialog.FileMode.Directory)
		dialog.setDirectory(folderName)

		if dialog.exec():
			if len(dialog.selectedFiles()) != 0:
				return dialog.selectedFiles()[0]

			else:
				self.textEdit_terminal_addError("ERREUR : Aucun dossier sélectionné !")
		else:
			self.textEdit_terminal_addWarning("WARNING : Le sélecteur de dossier ne s'est pas exécuté correctement !")
			return False

	def messagebox_yes_no(self, title="", text=""):
		"""
		Afficher une MessageBox avec un choix Oui / Non.

		----------
		Variables:
			- title : Titre de la fenêtre.
			- text  : Texte de la fenêtre.
		----------

		---------
		Retours : 
			- Réponse de la messagebox : QMessageBox.StandardButton.Yes/No
		---------
		"""

		dialog = QMessageBox(QWindow)
		dialog.setWindowTitle(title)
		dialog.setText(text)
		dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

		return dialog.exec()

if __name__ == "__main__":
	# Modules du logiciel
	from EXEC import *

	# Affichage de l'interface graphique
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())