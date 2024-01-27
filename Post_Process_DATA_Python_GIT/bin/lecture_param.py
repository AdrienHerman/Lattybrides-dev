"""
Lecture des paramètres.
HERMAN Adrien
21/11/2023
"""

# Modules de Python
import os

# Modules du Logiciel
from bin.errors import *

def lecture_param(path_config="config.conf", QWindow=None):
	"""
	Lecture des paramètres

	-----------
	Variables :
		- path_config : Chemin vers le fichier de configuration.
		- QWindow     : Objet fenêtre.
	-----------

	---------
	Retours :
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	---------
	"""

	# Variables
	type_fichier = None
	superposer_courbes = None
	nom_fichier = None
	nom_dossier = None
	calc_temps = None
	enregistrer_data = None
	nom_enregistrement = None
	dossier_enregistrement = None
	sppr_rollback = None
	recherche_deb_impact = None
	deb_impact_manuel = None
	tmps_deb_impact = None
	tarrage_dep = None
	tarrage_tmps = None
	detect_fin_essai = None
	dep_max = None
	calculer_energie = None
	fact_force = None
	fact_dep = None
	taux_augmentation = None
	nb_pas_avant_augmentation = None
	calc_vitesse_impact = None
	nbpts_vitesse_impact = None
	afficher_dep_tmps = None
	afficher_F_tmps = None
	afficher_F_dep = None
	afficher_sep = None

	return_list = [	type_fichier,
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
					afficher_sep]

	# Récupération du dossier contenant le fichier
	path = path_config.split("/")
	del path[len(path) - 1]
	path = '/'.join(path)

	if path != "":
		if not (path_config.split("/")[len(path_config.split("/")) - 1] in os.listdir(path)):
			print_or_addterminal_message(	QWindow=QWindow,
											type_msg="err",
											text="lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}".format(path_config))

			return [None for i in range(len(return_list))]
	else:
		if not (path_config in os.listdir()):
			print_or_addterminal_message(	QWindow=QWindow,
											type_msg="err",
											text="lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}".format(path_config))

			return [None for i in range(len(return_list))]

	# Stockage des données
	file = open(path_config, "r")
	lignes = file.readlines()
	file.close()

	# Parsing des données
	for i in range(len(lignes)):
		lignes[i] = lignes[i].split(":")

	# Traitement des données
	for i in range(len(lignes)):
		if lignes[i][0] == "#":	continue
		
		if lignes[i][0] == "type_fichier":
			if lignes[i][1].lower() == "txt":	type_fichier = "txt"
			elif lignes[i][1].lower() == "csv":	type_fichier = "csv"
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour type_fichier")
		elif lignes[i][0] == "superposer_courbes":
			if lignes[i][1] == "False":		superposer_courbes = False
			elif lignes[i][1] == "True":	superposer_courbes = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour superposer_courbes")
		elif lignes[i][0] == "nom_fichier":
			nom_fichier = lignes[i][1]
		elif lignes[i][0] == "nom_dossier":
			nom_dossier = lignes[i][1]
		elif lignes[i][0] == "calc_temps":
			if lignes[i][1] == "False":		calc_temps = False
			elif lignes[i][1] == "True":	calc_temps = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour calc_temps")
		elif lignes[i][0] == "enregistrer_data":
			if lignes[i][1] == "False":		enregistrer_data = False
			elif lignes[i][1] == "True":	enregistrer_data = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour enregistrer_data")
		elif lignes[i][0] == "nom_enregistrement":
			nom_enregistrement = lignes[i][1]
		elif lignes[i][0] == "dossier_enregistrement":
			dossier_enregistrement = lignes[i][1]
		elif lignes[i][0] == "sppr_rollback":
			if lignes[i][1] == "False":		sppr_rollback = False
			elif lignes[i][1] == "True":	sppr_rollback = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour sppr_rollback")
		elif lignes[i][0] == "recherche_deb_impact":
			if lignes[i][1] == "False":		recherche_deb_impact = False
			elif lignes[i][1] == "True":	recherche_deb_impact = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour recherche_deb_impact")
		elif lignes[i][0] == "deb_impact_manuel":
			if lignes[i][1] == "False":		deb_impact_manuel = False
			elif lignes[i][1] == "True":	deb_impact_manuel = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour deb_impact_manuel")
		elif lignes[i][0] == "tmps_deb_impact":
			try:
				tmps_deb_impact = float(lignes[i][1])
			except:
				print_or_addterminal_message(	QWindow=QWindow,
												type_msg="wrg",
												text="""	lecture_param\nLe type de données entrée dans tmps_deb_impact n'est pas correct !
							\n     tmps_deb_impact={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "tarrage_dep":
			if lignes[i][1] == "False":		tarrage_dep = False
			elif lignes[i][1] == "True":	tarrage_dep = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour tarrage_dep")
		elif lignes[i][0] == "tarrage_tmps":
			if lignes[i][1] == "False":		tarrage_tmps = False
			elif lignes[i][1] == "True":	tarrage_tmps = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour tarrage_tmps")
		elif lignes[i][0] == "detect_fin_essai":
			if lignes[i][1] == "False":		detect_fin_essai = False
			elif lignes[i][1] == "True":	detect_fin_essai = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour detect_fin_essai")
		elif lignes[i][0] == "dep_max":
			try:
				dep_max = float(lignes[i][1])
			except:
				print_or_addterminal_message(	QWindow=QWindow,
												type_msg="wrg",
												text="""	lecture_param\nLe type de données entrée dans dep_max n'est pas correct !
							\n     dep_max={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "calculer_energie":
			if lignes[i][1] == "False":		calculer_energie = False
			elif lignes[i][1] == "True":	calculer_energie = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour calculer_energie")
		elif lignes[i][0] == "fact_force":
			try:
				fact_force = float(lignes[i][1])
			except:
				print_or_addterminal_message(	QWindow=QWindow,
												type_msg="wrg",
												text="""	lecture_param\nLe type de données entrée dans fact_force n'est pas correct !
							\n     fact_force={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "fact_dep":
			try:
				fact_dep = float(lignes[i][1])
			except:
				print_or_addterminal_message(	QWindow=QWindow,
												type_msg="wrg",
												text="""	lecture_param\nLe type de données entrée dans fact_dep n'est pas correct !
							\n     fact_dep={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "taux_augmentation":
			try:
				taux_augmentation = float(lignes[i][1])
			except:
				print_or_addterminal_message(	QWindow=QWindow,
												type_msg="wrg",
												text="""	lecture_param\nLe type de données entrée dans taux_augmentation n'est pas correct !
							\n     taux_augmentation={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "nb_pas_avant_augmentation":
			try:
				nb_pas_avant_augmentation = int(lignes[i][1])
			except:
				print_or_addterminal_message(	QWindow=QWindow,
												type_msg="wrg",
												text="""	lecture_param\nLe type de données entrée dans nb_pas_avant_augmentation n'est pas correct !
							\n     nb_pas_avant_augmentation={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "calc_vitesse_impact":
			if lignes[i][1] == "False":		calc_vitesse_impact = False
			elif lignes[i][1] == "True":	calc_vitesse_impact = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour calc_vitesse_impact")
		elif lignes[i][0] == "nbpts_vitesse_impact":
			try:
				nbpts_vitesse_impact = int(lignes[i][1])
			except:
				print_or_addterminal_message(	QWindow=QWindow,
												type_msg="wrg",
												text="""	lecture_param\nLe type de données entrée dans nbpts_vitesse_impact n'est pas correct !
							\n     nbpts_vitesse_impact={0}""".format(lignes[i][1]))
		elif lignes[i][0] == "afficher_dep_tmps":
			if lignes[i][1] == "False":		afficher_dep_tmps = False
			elif lignes[i][1] == "True":	afficher_dep_tmps = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour afficher_dep_tmps")
		elif lignes[i][0] == "afficher_F_tmps":
			if lignes[i][1] == "False":		afficher_F_tmps = False
			elif lignes[i][1] == "True":	afficher_F_tmps = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour afficher_F_tmps")
		elif lignes[i][0] == "afficher_F_dep":
			if lignes[i][1] == "False":		afficher_F_dep = False
			elif lignes[i][1] == "True":	afficher_F_dep = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour afficher_F_dep")
		elif lignes[i][0] == "afficher_sep":
			if lignes[i][1] == "False":		afficher_sep = False
			elif lignes[i][1] == "True":	afficher_sep = True
			else:	print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="lecture_param\nCommande inconnue pour afficher_sep")

	if type_fichier == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ntype_fichier est non défini")
	elif superposer_courbes == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nsuperposer_courbes est non défini")
	elif nom_fichier == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nnom_fichier est non défini")
	elif nom_dossier == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nnom_dossier est non défini")
	elif calc_temps == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ncalc_temps est non défini")
	elif enregistrer_data == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nenregistrer_data est non défini")
	elif nom_enregistrement == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nnom_enregistrement est non défini")
	elif dossier_enregistrement == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ndossier_enregistrement est non défini")
	elif sppr_rollback == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nsppr_rollback est non défini")
	elif recherche_deb_impact == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nrecherche_deb_impact est non défini")
	elif deb_impact_manuel == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ndeb_impact_manuel est non défini")
	elif tmps_deb_impact == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ntmps_deb_impact est non défini")
	elif tarrage_dep == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ntarrage_dep est non défini")
	elif tarrage_tmps == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ntarrage_tmps est non défini")
	elif detect_fin_essai == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ndetect_fin_essai est non défini")
	elif dep_max == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ndep_max est non défini")
	elif calculer_energie == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ncalculer_energie est non défini")
	elif fact_force == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nfact_force est non défini")
	elif fact_dep == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nfact_dep est non défini")
	elif taux_augmentation == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ntaux_augmentation est non défini")
	elif calc_vitesse_impact == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\ncalc_vitesse_impact est non défini")
	elif nbpts_vitesse_impact == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nnbpts_vitesse_impact est non défini")
	elif nb_pas_avant_augmentation == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nnb_pas_avant_augmentation est non défini")
	elif afficher_dep_tmps == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nafficher_dep_tmps est non défini")
	elif afficher_F_tmps == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nafficher_F_tmps est non défini")
	elif afficher_F_dep == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nafficher_F_dep est non défini")
	elif afficher_sep == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="wrg",
										text="lecture_param\nafficher_sep est non défini")

	return_list = [	type_fichier,
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
				afficher_sep]

	return return_list