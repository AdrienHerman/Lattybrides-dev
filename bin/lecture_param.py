"""
Lecture des paramètres
HERMAN Adrien
21/11/2023
"""

def lecture_param(path_config="config.txt", debug=True):
	"""
	Lecture des paramètres

	-----------
	Variables :
		path_config -> Chemin vers le fichier de configuration
		wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		file_debug -> Fichier de déboggage (ouvert)
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
	-----------
	"""

	# Modules de Python
	import os

	# Récupération du dossier contenant le fichier
	path = path_config.split("/")
	del path[len(path) - 1]
	path = '/'.join(path)

	# Variable contenant les log
	log = ""

	if path != "":
		if not (path_config.split("/")[len(path_config.split("/")) - 1] in os.listdir(path)):
			if debug:
				log += "lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}\n".format(path_config)

			return []
	else:
		if not (path_config in os.listdir()):
			if debug:
				log += "lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}\n".format(path_config)

			return []

	# Variables
	# ATTENTION : À l'ajout de variable, ne pas oublier d'actualiser
	# le nombre de variables à retourner !
	#	Fonctions de génération
	gen_losange_basic = None
	gen_losange_grad = None
	gen_func = [None for i in range(2)]
	#	Géométrie générale
	generation_plateaux_extremitees = None
	ep_plateau_dessous = None
	ep_plateau_dessus = None
	ep = None
	dimlat_ep = None
	dimlat_x = None
	dimlat_y = None
	# 	Partie optimisation de la masse
	optimisation_masse = None
	objectif_masse = None
	tolerance = None
	nb_pas_max = None
	correction_ep_par_pas = None
	pourcentage_modification_correction = None
	seuil_augmentation_correction = None
	seuil_diminution_correction = None
	rho = None
	# 	Géométrie des losanges "basic"
	nb_motif_x_sg = None
	nb_motif_y_sg = None
	#	Géométrie des gradients
	nb_y_par_couche = None
	nb_x_par_couche = None
	dimlat_par_couche_manuel = None
	dimlat_par_couche = None
	ep_par_couche = None
	ep_plateaux = None
	#	Partie exploitation du modèle 3D
	extrude = None 
	export = None 
	export_name = None 
	export_path = None 
	sketch_visible = None
	# 	Partie Débogage
	semi_debug = None 
	debug = None 
	debug_current_folder = None

	# Stockage des données
	if debug and debug:
		log += "Ouverture du fichier de configuration\n"

	try:
		file = open(path_config, "r")
		lignes = file.readlines()
		file.close()
	except:
		if debug:
			log += "Impossible d'ouvrir le fichier de configuration\n"

	# Parsing des données
	if debug and debug:
		log += "Début du parsing des données\n"

	for i in range(len(lignes)):
		lignes[i] = lignes[i].split(":")

	# Traitement des données
	for i in range(len(lignes)):
		# Commentaire
		if lignes[i][0] == "#":	continue
		
		# Fonctions de génération des structures
		if lignes[i][0] == "gen_losange_basic":
			if lignes[i][1] == "False":
				gen_losange_basic = False
				gen_func[0] = False
			elif lignes[i][1] == "True":
				gen_losange_basic = True
				gen_func[0] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_losange_basic\n"
		elif lignes[i][0] == "gen_losange_grad":
			if lignes[i][1] == "False":
				gen_losange_grad = False
				gen_func[1] = False
			elif lignes[i][1] == "True":
				gen_losange_grad = True
				gen_func[1] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_losange_grad\n"

		# Géométrie
		if lignes[i][0] == "generation_plateaux_extremitees":
			if lignes[i][1] == "False":		generation_plateaux_extremitees = False
			elif lignes[i][1] == "True":	generation_plateaux_extremitees = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour generation_plateaux_extremitees\n"
		elif lignes[i][0] == "ep_plateau_dessous":
			try:
				ep_plateau_dessous = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans ep_plateau_dessous n'est pas correct !
									\n     ep_plateau_dessous={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "ep_plateau_dessus":
			try:
				ep_plateau_dessus = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans ep_plateau_dessus n'est pas correct !
									\n     ep_plateau_dessus={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "ep":
			try:
				ep = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans ep n'est pas correct !
									\n     ep={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "dimlat_ep":
			try:
				dimlat_ep = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans dimlat_ep n'est pas correct !
									\n     dimlat_ep={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "dimlat_x":
			try:
				dimlat_x = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans dimlat_x n'est pas correct !
									\n     dimlat_x={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "dimlat_y":
			try:
				dimlat_y = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans dimlat_y n'est pas correct !
									\n     dimlat_y={0}\n""".format(lignes[i][1])

		# Partie optimisation de la masse
		if lignes[i][0] == "optimisation_masse":
			if lignes[i][1] == "False":		optimisation_masse = False
			elif lignes[i][1] == "True":	optimisation_masse = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour optimisation_masse\n"
		elif lignes[i][0] == "objectif_masse":
			try:
				objectif_masse = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans objectif_masse n'est pas correct !
									\n     objectif_masse={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "tolerance":
			try:
				tolerance = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans tolerance n'est pas correct !
									\n     tolerance={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "nb_pas_max":
			try:
				nb_pas_max = int(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nb_pas_max n'est pas correct !
									\n     nb_pas_max={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "correction_ep_par_pas":
			try:
				correction_ep_par_pas = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans correction_ep_par_pas n'est pas correct !
									\n     correction_ep_par_pas={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "pourcentage_modification_correction":
			try:
				pourcentage_modification_correction = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans pourcentage_modification_correction n'est pas correct !
									\n     pourcentage_modification_correction={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "seuil_augmentation_correction":
			try:
				seuil_augmentation_correction = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans seuil_augmentation_correction n'est pas correct !
									\n     seuil_augmentation_correction={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "seuil_diminution_correction":
			try:
				seuil_diminution_correction = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans seuil_diminution_correction n'est pas correct !
									\n     seuil_diminution_correction={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "rho":
			try:
				rho = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans rho n'est pas correct !
									\n     rho={0}\n""".format(lignes[i][1])

		# Géométrie des losanges "basic"
		if lignes[i][0] == "nb_motif_x_sg":
			try:
				nb_motif_x_sg = int(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nb_motif_x_sg n'est pas correct !
									\n     nb_motif_x_sg={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "nb_motif_y_sg":
			try:
				nb_motif_y_sg = int(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nb_motif_y_sg n'est pas correct !
									\n     nb_motif_y_sg={0}\n""".format(lignes[i][1])

		# Géométrie des losanges "grad"
		if lignes[i][0] == "nb_y_par_couche":
			try:
				nb_y_par_couche = [int(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nb_y_par_couche n'est pas correct !
									\n     nb_y_par_couche={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "nb_x_par_couche":
			try:
				nb_x_par_couche = [int(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nb_x_par_couche n'est pas correct !
									\n     nb_x_par_couche={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "dimlat_par_couche_manuel":
			if lignes[i][1] == "False":		dimlat_par_couche_manuel = False
			elif lignes[i][1] == "True":	dimlat_par_couche_manuel = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour dimlat_par_couche_manuel\n"
		elif lignes[i][0] == "dimlat_par_couche":
			try:
				dimlat_par_couche = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans dimlat_par_couche n'est pas correct !
									\n     dimlat_par_couche={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "ep_par_couche":
			try:
				ep_par_couche = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans ep_par_couche n'est pas correct !
									\n     ep_par_couche={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "ep_plateaux":
			try:
				ep_plateaux = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans ep_plateaux n'est pas correct !
									\n     ep_plateaux={0}\n""".format(lignes[i][1])

		# Partie exploitation du modèle 3D
		if lignes[i][0] == "extrude":
			if lignes[i][1] == "False":		extrude = False
			elif lignes[i][1] == "True":	extrude = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour extrude\n"
		elif lignes[i][0] == "export":
			if lignes[i][1] == "False":		export = False
			elif lignes[i][1] == "True":	export = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour export\n"
		elif lignes[i][0] == "export_name":
			export_name = str(lignes[i][1])
		elif lignes[i][0] == "export_path":
			export_path = str(lignes[i][1])
		elif lignes[i][0] == "sketch_visible":
			if lignes[i][1] == "False":		sketch_visible = False
			elif lignes[i][1] == "True":	sketch_visible = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour sketch_visible\n"

		# Partie Débogage
		if lignes[i][0] == "semi_debug":
			if lignes[i][1] == "False":		semi_debug = False
			elif lignes[i][1] == "True":	semi_debug = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour semi_debug\n"
		elif lignes[i][0] == "debug":
			if lignes[i][1] == "False":		debug = False
			elif lignes[i][1] == "True":	debug = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour debug\n"
		elif lignes[i][0] == "debug_current_folder":
			debug_current_folder = str(lignes[i][1])

	# Traitement des données non définies
	return_ok = [	True,
				gen_losange_basic,
				gen_losange_grad,
				generation_plateaux_extremitees,
				[ep_plateau_dessous, ep_plateau_dessus],
				ep,
				dimlat_ep,
				dimlat_x,
				dimlat_y,
				optimisation_masse,
				objectif_masse,
				tolerance,
				nb_pas_max,
				correction_ep_par_pas,
				pourcentage_modification_correction,
				seuil_augmentation_correction,
				seuil_diminution_correction,
				rho,
				nb_motif_x_sg,
				nb_motif_y_sg,
				nb_y_par_couche,
				nb_x_par_couche,
				dimlat_par_couche_manuel,
				dimlat_par_couche,
				ep_par_couche,
				ep_plateaux,
				extrude,
				export,
				export_name,
				export_path,
				sketch_visible,
				semi_debug,
				debug,
				debug_current_folder]
	return_nok = [False for i in range(len(return_ok))]	# Liste à retourner si la lecture des parmaètres ne s'est pas terminée correctement

	# 	Traitement du nombre de fonctions de génération
	if gen_func.count(True) > 1:
		if debug:
			log += "lecture_param\nIl y a trop de fonctions de génération de strucutres sélectionnées !\n"
		return_nok.append(log)
		return return_nok
	elif gen_func.count(True) == 0:
		if debug:
			log += "lecture_param\nIl n'y a pas de fonction de génération de strucutres sélectionnées !\n"
		return_nok.append(log)
		return return_nok

	# 	Traitement des variables de géométrie générale
	if generation_plateaux_extremitees == None:
		if debug:
			log += "lecture_param\ngeneration_plateaux_extremitees n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif ep_plateau_dessous == None:
		if debug:
			log += "lecture_param\nep_plateau_dessous n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif ep_plateau_dessus == None:
		if debug:
			log += "lecture_param\nep_plateau_dessus n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif ep == None:
		if debug:
			log += "lecture_param\nep n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif dimlat_ep == None:
		if debug:
			log += "lecture_param\ndimlat_ep n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif dimlat_x == None:
		if debug:
			log += "lecture_param\ndimlat_x n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif dimlat_y == None:
		if debug:
			log += "lecture_param\ndimlat_y n'est pas définie !\n"
		return_nok.append(log)
		return return_nok

	# Partie optimisation de la masse
	if optimisation_masse == None:
		if debug:
			log += "lecture_param\noptimisation_masse n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif objectif_masse == None:
		if debug:
			log += "lecture_param\nobjectif_masse n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif tolerance == None:
		if debug:
			log += "lecture_param\ntolerance n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif correction_ep_par_pas == None:
		if debug:
			log += "lecture_param\ncorrection_ep_par_pas n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif pourcentage_modification_correction == None:
		if debug:
			log += "lecture_param\npourcentage_modification_correction n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif seuil_augmentation_correction == None:
		if debug:
			log += "lecture_param\nseuil_augmentation_correction n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif seuil_diminution_correction == None:
		if debug:
			log += "lecture_param\nseuil_diminution_correction n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif rho == None:
		if debug:
			log += "lecture_param\nrho n'est pas définie !\n"
		return_nok.append(log)
		return return_nok

	# 	Traitement des variables concernant la géométrie des losanges "basic"
	if gen_losange_basic == True:
		if nb_motif_x_sg == None:
			if debug:
				log += "lecture_param\nnb_motif_x_sg n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif nb_motif_y_sg == None:
			if debug:
				log += "lecture_param\nnb_motif_y_sg n'est pas définie !\n"
			return_nok.append(log)
			return return_nok

	# Géométrie des losanges "grad"
	if gen_losange_grad == True:
		if nb_y_par_couche == None:
			if debug:
				log += "lecture_param\nnb_y_par_couche n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif nb_x_par_couche == None:
			if debug:
				log += "lecture_param\nnb_x_par_couche n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif dimlat_par_couche_manuel == None:
			if debug:
				log += "lecture_param\ndimlat_par_couche_manuel n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif dimlat_par_couche == None:
			if debug:
				log += "lecture_param\ndimlat_par_couche n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif ep_par_couche == None:
			if debug:
				log += "lecture_param\nep_par_couche n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif ep_plateaux == None:
			if debug:
				log += "lecture_param\nep_plateaux n'est pas définie !\n"
			return_nok.append(log)
			return return_nok

		if len(nb_x_par_couche) != len(nb_y_par_couche):
			if debug:
				log += """lecture_param\nnb_x_par_couche doit ({0}) avoir le 
						même nombre d'items que nb_y_par_couche ({1}) !\n""".format(	len(nb_x_par_couche),
																					len(nb_y_par_couche))
			return_nok.append(log)
			return return_nok
		if len(dimlat_par_couche) != len(nb_y_par_couche):
			if debug:
				log += """lecture_param\ndimlat_par_couche doit ({0}) avoir le 
						même nombre d'items que nb_y_par_couche ({1}) !\n""".format(	len(dimlat_par_couche),
																					len(nb_y_par_couche))
			return_nok.append(log)
			return return_nok
		if len(ep_par_couche) != len(nb_y_par_couche):
			if debug:
				log += """lecture_param\nep_par_couche doit ({0}) avoir le 
						même nombre d'items que nb_y_par_couche ({1}) !\n""".format(	len(ep_par_couche),
																					len(nb_y_par_couche))
			return_nok.append(log)
			return return_nok
		if len(ep_plateaux) != len(nb_y_par_couche) - 1:
			if debug:
				log += """lecture_param\nep_plateaux doit ({0}) avoir un item de moins 
						que nb_y_par_couche ({1}) !\n""".format(	len(ep_plateaux),
																len(nb_y_par_couche))
			return_nok.append(log)
			return return_nok

	# Partie exploitation du modèle 3D
	if extrude == None:
		if debug:
			log += "lecture_param\nextrude n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif export == None:
		if debug:
			log += "lecture_param\nexport n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif export_name == None:
		if debug:
			log += "lecture_param\nexport_name n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif export_path == None:
		if debug:
			log += "lecture_param\nexport_path n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif sketch_visible == None:
		if debug:
			log += "lecture_param\nsketch_visible n'est pas définie !\n"
		return_nok.append(log)
		return return_nok

	# Partie Débogage
	if semi_debug == None:
		if debug:
			log += "lecture_param\nsemi_debug n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif debug == None:
		if debug:
			log += "lecture_param\ndebug n'est pas définie !\n"
		return_nok.append(log)
		return return_nok
	elif debug_current_folder == None:
		if debug:
			log += "lecture_param\ndebug_current_folder n'est pas définie !\n"
		return_nok.append(log)
		return return_nok

	return_ok.append(log)
	return 	return_ok