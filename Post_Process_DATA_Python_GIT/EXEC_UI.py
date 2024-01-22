"""
Corps principal de l'application avec interface graphique
HERMAN Adrien
22/01/2024

pyuic6 UI/H3D_Parts_MainWindow.ui -o MainWindowUI.py
"""

# Modules de Python
import sys
from PyQt6.QtWidgets import (
	QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)
from PyQt6.uic import loadUi
from PyQt6.QtGui import QKeySequence, QPixmap
from PyQt6.QtCore import QDate

# Modules internes
from UI.MainWindowUI import Ui_MainWindow
from bin.lecture_param import *

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		"""
		Initialisation de l'objet fenêtre
		"""

		super().__init__(parent)
		self.setupUi(self)              # Lancement de la fenêtre
		self.connectSignalsSlots()		# Connexion des signaux

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

		# Actions du menu principal
		self.actionQuitter.triggered.connect(self.close)
		self.actionQuitter.setShortcut(QKeySequence("Ctrl+Q"))

	def changeEnabled(self, list_objects, state):
		"""
		Action d'activer / désactiver une liste d'objets
		"""
		
		for o in list_objects:	o.setEnabled(state)

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
							self.pushButton_nom_fichier]

			self.changeEnabled(list_objects, True)

			list_objects = [self.label_nom_dossier,
							self.lineEdit_nom_dossier,
							self.pushButton_nom_dossier]

			self.changeEnabled(list_objects, False)

	def comboBox_currentTextChanged_type_fichier(self):
		"""
		Action d'activer / désactiver les éléments pour type_fichier
		"""

		# Récupération de l'état de la combobox
		current_text = self.comboBox_type_fichier.currentText()

		if current_text == "CSV":	state = True
		else:						state = False

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

	def load_config(self, path_config="config_default.txt"):
		"""
		Charger la configuration d'un fichier de configuration dans la fenêtre

		-----------
		Variables :
			- path_config : Chemin vers le fichier de configuration
		-----------
		"""
		
		[	type_fichier,
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
			afficher_sep] = lecture_param(path_config)

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

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec())