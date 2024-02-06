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
	if len(path) > 1:
		del path[-1]
		path = '/'.join(path)

	# Variable contenant les log
	log = ""
	return_nok = [False for i in range(54)]	# Liste à retourner si la lecture des parmaètres ne s'est pas terminée correctement

	if path != "":
		if not (path_config.split("/")[-1] in os.listdir(path)):
			if debug:
				log += "lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}\n".format(path_config)

			return_nok.append(log)

			return return_nok
	else:
		if not (path_config in os.listdir()):
			if debug:
				log += "lecture_param\nLe fichier de paramètres n'existe pas !\n     path_config={0}\n".format(path_config)

			return_nok.append(log)

			return return_nok

	# Variables
	# ATTENTION : À l'ajout de variable, ne pas oublier d'actualiser
	# le nombre de variables à retourner !
	#	Fonctions de génération
	gen_losange_basic = None
	gen_losange_grad = None
	gen_hex_tri1_2D_aligne_basic = None
	gen_hex_tri1_2D_aligne_grad = None
	gen_hex_tri1_2D_naligne_basic = None
	gen_hex_tri1_2D_naligne_grad = None
	gen_tri_2D_basic = None
	gen_tri_2D_grad = None
	gen_cos_2D_basic = None
	gen_cos_2D_grad = None
	gen_func = [None for i in range(10)]
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
	# 	Géométries sans gradients
	nb_motif_x_sg = None
	nb_motif_y_sg = None
	#	Géométries avec gradients
	nb_y_par_couche = None
	nb_x_par_couche = None
	dimlat_par_couche_manuel = None
	dimlat_par_couche = None
	ep_par_couche = None
	ep_plateaux = None
	#	Géométrie Hexagones + Triangles 1 2D (Alignés ou Non / Avec ou sans gradients)
	alpha_hex_tri1_2D = None
	alpha_hex_tri1_2D_grad = None
	#	Géométrie Triangles 2D (Avec ou sans gradients)
	alpha_tri_2D = None
	alpha_tri_2D_grad = None
	#	Géométrie Cosinus 2D (Sans gradients)
	phi = None
	period_fact = None
	amp = None
	nbpts_cos = None
	#	Géométrie Cosinus 2D (Avec gradients)
	phi_grad = None
	period_fact_grad = None
	amp_grad = None
	nbpts_cos_grad = None
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
	if debug:
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
		elif lignes[i][0] == "gen_hex_tri1_2D_aligne_basic":
			if lignes[i][1] == "False":
				gen_hex_tri1_2D_aligne_basic = False
				gen_func[2] = False
			elif lignes[i][1] == "True":
				gen_hex_tri1_2D_aligne_basic = True
				gen_func[2] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_hex_tri1_2D_aligne_basic\n"
		elif lignes[i][0] == "gen_hex_tri1_2D_aligne_grad":
			if lignes[i][1] == "False":
				gen_hex_tri1_2D_aligne_grad = False
				gen_func[3] = False
			elif lignes[i][1] == "True":
				gen_hex_tri1_2D_aligne_grad = True
				gen_func[3] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_hex_tri1_2D_aligne_grad\n"
		elif lignes[i][0] == "gen_hex_tri1_2D_naligne_basic":
			if lignes[i][1] == "False":
				gen_hex_tri1_2D_naligne_basic = False
				gen_func[4] = False
			elif lignes[i][1] == "True":
				gen_hex_tri1_2D_naligne_basic = True
				gen_func[4] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_hex_tri1_2D_naligne_basic\n"
		elif lignes[i][0] == "gen_hex_tri1_2D_naligne_grad":
			if lignes[i][1] == "False":
				gen_hex_tri1_2D_naligne_grad = False
				gen_func[5] = False
			elif lignes[i][1] == "True":
				gen_hex_tri1_2D_naligne_grad = True
				gen_func[5] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_hex_tri1_2D_naligne_grad\n"
		elif lignes[i][0] == "gen_tri_2D_basic":
			if lignes[i][1] == "False":
				gen_tri_2D_basic = False
				gen_func[6] = False
			elif lignes[i][1] == "True":
				gen_tri_2D_basic = True
				gen_func[6] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_tri_2D_basic\n"
		elif lignes[i][0] == "gen_tri_2D_grad":
			if lignes[i][1] == "False":
				gen_tri_2D_grad = False
				gen_func[7] = False
			elif lignes[i][1] == "True":
				gen_tri_2D_grad = True
				gen_func[7] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_tri_2D_grad\n"
		elif lignes[i][0] == "gen_cos_2D_basic":
			if lignes[i][1] == "False":
				gen_cos_2D_basic = False
				gen_func[8] = False
			elif lignes[i][1] == "True":
				gen_cos_2D_basic = True
				gen_func[8] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_cos_2D\n"
		elif lignes[i][0] == "gen_cos_2D_grad":
			if lignes[i][1] == "False":
				gen_cos_2D_grad = False
				gen_func[9] = False
			elif lignes[i][1] == "True":
				gen_cos_2D_grad = True
				gen_func[9] = True
			else:
				if debug:
					log += "lecture_param\nCommande inconnue pour gen_cos_2D_grad\n"

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

		# Géométrie sans gradients
		if lignes[i][0] == "nb_motif_x_sg":
			try:
				nb_motif_x_sg = int(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nb_motif_x_sg n'est pas correct !
									\n     nb_motif_x_sg={0}\n""".format(lignes[i][1])

			if nb_motif_x_sg != None and nb_motif_x_sg <= 0:
				log += """lecture_param\nnb_motif_x_sg doit être un nombre entier positif strict !
							\n     nb_motif_x_sg={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "nb_motif_y_sg":
			try:
				nb_motif_y_sg = int(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nb_motif_y_sg n'est pas correct !
									\n     nb_motif_y_sg={0}\n""".format(lignes[i][1])

			if nb_motif_y_sg != None and nb_motif_y_sg <= 0:
				log += """lecture_param\nnb_motif_y_sg doit être un nombre entier positif strict !
							\n     nb_motif_y_sg={0}\n""".format(lignes[i][1])

		# Géométries avec gradients
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

		# Géométrie Hexagones + Triangles 1 2D (Alignés ou Non / Avec ou sans gradients)
		if lignes[i][0] == "alpha_hex_tri1_2D":
			try:
				alpha_hex_tri1_2D = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans alpha_hex_tri1_2D n'est pas correct !
									\n     alpha_hex_tri1_2D={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "alpha_hex_tri1_2D_grad":
			try:
				alpha_hex_tri1_2D_grad = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans alpha_hex_tri1_2D_grad n'est pas correct !
									\n     alpha_hex_tri1_2D_grad={0}\n""".format(lignes[i][1])

		# Géométrie Triangles 2D (Avec ou sans gradients)
		if lignes[i][0] == "alpha_tri_2D":
			try:
				alpha_tri_2D = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans alpha_tri_2D n'est pas correct !
									\n     alpha_tri_2D={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "alpha_tri_2D_grad":
			try:
				alpha_tri_2D_grad = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans alpha_tri_2D_grad n'est pas correct !
									\n     alpha_tri_2D_grad={0}\n""".format(lignes[i][1])

		# Géométrie Cosinus 2D (Sans gradients)
		if lignes[i][0] == "phi" and ',' in lignes[i][1]:
			try:
				phi = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans phi n'est pas correct !
									\n     phi={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "phi":
			try:
				phi = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans phi n'est pas correct !
									\n     phi={0}\n""".format(lignes[i][1])
		if lignes[i][0] == "period_fact" and ',' in lignes[i][1]:
			try:
				period_fact = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans period_fact n'est pas correct !
									\n     period_fact={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "period_fact":
			try:
				period_fact = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans period_fact n'est pas correct !
									\n     period_fact={0}\n""".format(lignes[i][1])
		if lignes[i][0] == "amp" and ',' in lignes[i][1]:
			try:
				amp = [float(lignes[i][1].split(',')[j]) for j in range(len(lignes[i][1].split(',')))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans amp n'est pas correct !
									\n     amp={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "amp":
			try:
				amp = float(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans amp n'est pas correct !
									\n     amp={0}\n""".format(lignes[i][1])
		if lignes[i][0] == "nbpts_cos":
			try:
				nbpts_cos = int(lignes[i][1])
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans nbpts_cos n'est pas correct !
									\n     nbpts_cos={0}\n""".format(lignes[i][1])

		# Géométrie Cosinus 2D (Avec gradients)
		try:
			lignes_s = lignes[i][1].split('|')
		except:
			if debug:
				log += """	lecture_param\nLe type de données entrée dans phi_grad n'est pas correct !
								\n     phi_grad={0}\n""".format(lignes[i][1])
		if lignes[i][0] == "phi_grad" and '|' in lignes[i][1] and ',' in lignes[i][1]:
			try:
				phi_grad = [[float(phi_s) for phi_s in lignes_s[j].split(',')] for j in range(len(lignes_s))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans phi_grad n'est pas correct !
									\n     phi_grad={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "phi_grad" and '|' in lignes[i][1]:
			phi_grad = [float(phi_s) for phi_s in lignes_s]

		try:
			lignes_s = lignes[i][1].split('|')
		except:
			if debug:
				log += """	lecture_param\nLe type de données entrée dans period_fact_grad n'est pas correct !
								\n     period_fact_grad={0}\n""".format(lignes[i][1])
		if lignes[i][0] == "period_fact_grad" and '|' in lignes[i][1] and ',' in lignes[i][1]:
			try:
				period_fact_grad = [[float(period_fact_s) for period_fact_s in lignes_s[j].split(',')] for j in range(len(lignes_s))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans period_fact_grad n'est pas correct !
									\n     period_fact_grad={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "period_fact_grad" and '|' in lignes[i][1]:
			period_fact_grad = [float(period_fact_s) for period_fact_s in lignes_s]

		try:
			lignes_s = lignes[i][1].split('|')
		except:
			if debug:
				log += """	lecture_param\nLe type de données entrée dans amp_grad n'est pas correct !
								\n     amp_grad={0}\n""".format(lignes[i][1])
		if lignes[i][0] == "amp_grad" and '|' in lignes[i][1] and ',' in lignes[i][1]:
			try:
				amp_grad = [[float(amp_s) for amp_s in lignes_s[j].split(',')] for j in range(len(lignes_s))]
			except:
				if debug:
					log += """	lecture_param\nLe type de données entrée dans amp_grad n'est pas correct !
									\n     amp_grad={0}\n""".format(lignes[i][1])
		elif lignes[i][0] == "amp_grad" and '|' in lignes[i][1]:
			amp_grad = [float(amp_s) for amp_s in lignes_s]

		try:
			lignes_s = lignes[i][1].split('|')
		except:
			if debug:
				log += """	lecture_param\nLe type de données entrée dans nbpts_cos_grad n'est pas correct !
								\n     nbpts_cos_grad={0}\n""".format(lignes[i][1])
		if lignes[i][0] == "nbpts_cos_grad" and '|' in lignes[i][1]:
			nbpts_cos_grad = [int(nbpts_cos_s) for nbpts_cos_s in lignes_s]

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
					gen_hex_tri1_2D_aligne_basic,
					gen_hex_tri1_2D_aligne_grad,
					gen_hex_tri1_2D_naligne_basic,
					gen_hex_tri1_2D_naligne_grad,
					gen_tri_2D_basic,
					gen_tri_2D_grad,
					gen_cos_2D_basic,
					gen_cos_2D_grad,
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
					alpha_hex_tri1_2D,
					alpha_hex_tri1_2D_grad,
					alpha_tri_2D,
					alpha_tri_2D_grad,
					phi,
					period_fact,
					amp,
					nbpts_cos,
					phi_grad,
					period_fact_grad,
					amp_grad,
					nbpts_cos_grad,
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

	# 	Traitement des variables concernant les géométrie sans gradients
	if gen_losange_basic or gen_hex_tri1_2D_aligne_basic:
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

	# Géométries avec gradients
	if gen_losange_grad or gen_hex_tri1_2D_aligne_grad:
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
		elif dimlat_par_couche_manuel and dimlat_par_couche == None:
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
		if dimlat_par_couche_manuel and len(dimlat_par_couche) != len(nb_y_par_couche):
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

	# Géométrie Hexagones + Triangles 1 2D (Alignés ou Non Sans gradients)
	if gen_hex_tri1_2D_aligne_basic:
		if alpha_hex_tri1_2D == None:
			if debug:
				log += "lecture_param\nalpha_hex_tri1_2D n'est pas définie !\n"
			return_nok.append(log)
			return return_nok

	# Géométrie Hexagones + Triangles 1 2D (Alignés ou Non Avec gradients)
	if gen_hex_tri1_2D_aligne_grad:
		if alpha_hex_tri1_2D_grad == None:
			if debug:
				log += "lecture_param\nalpha_hex_tri1_2D_grad n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif len(alpha_hex_tri1_2D_grad) != len(nb_y_par_couche):
			if debug:
				log += "lecture_param\nalpha_hex_tri1_2D_grad n'a pas le bon nombre d'éléments !\n"
			return_nok.append(log)
			return return_nok

	# Géométrie Triangles 2D (Sans gradients)
	if gen_tri_2D_basic:
		if alpha_tri_2D == None:
			if debug:
				log += "lecture_param\nalpha_tri_2D n'est pas définie !\n"
			return_nok.append(log)
			return return_nok

	# Géométrie Triangles 2D (Avec gradients)
	if gen_tri_2D_grad:
		if alpha_tri_2D_grad == None:
			if debug:
				log += "lecture_param\nalpha_tri_2D_grad n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif len(alpha_tri_2D_grad) != len(nb_y_par_couche):
			if debug:
				log += "lecture_param\nalpha_tri_2D_grad n'a pas le bon nombre d'éléments !\n"
			return_nok.append(log)
			return return_nok

	# Géométrie Cosinus 2D (Sans gradients)
	if gen_cos_2D_basic:
		if phi == None:
			if debug:
				log += "lecture_param\nphi n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif period_fact == None:
			if debug:
				log += "lecture_param\nperiod_fact n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif amp == None:
			if debug:
				log += "lecture_param\namp n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif nbpts_cos == None:
			if debug:
				log += "lecture_param\nnbpts_cos n'est pas définie !\n"
			return_nok.append(log)
			return return_nok

	# Géométrie Cosinus 2D (Avec gradients)
	if gen_cos_2D_grad:
		if phi_grad == None:
			if debug:
				log += "lecture_param\nphi_grad n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif len(phi_grad) != len(nb_y_par_couche):
			if debug:
				log += "lecture_param\nphi_grad n'a pas le bon nombre d'éléments !\n"
			return_nok.append(log)
			return return_nok
		
		if period_fact_grad == None:
			if debug:
				log += "lecture_param\nperiod_fact_grad n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif len(period_fact_grad) != len(nb_y_par_couche):
			if debug:
				log += "lecture_param\nperiod_fact_grad n'a pas le bon nombre d'éléments !\n"
			return_nok.append(log)
			return return_nok
		
		if amp_grad == None:
			if debug:
				log += "lecture_param\namp_grad n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif len(amp_grad) != len(nb_y_par_couche):
			if debug:
				log += "lecture_param\namp_grad n'a pas le bon nombre d'éléments !\n"
			return_nok.append(log)
			return return_nok
		
		if nbpts_cos_grad == None:
			if debug:
				log += "lecture_param\nnbpts_cos_grad n'est pas définie !\n"
			return_nok.append(log)
			return return_nok
		elif len(nbpts_cos_grad) != len(nb_y_par_couche):
			if debug:
				log += "lecture_param\nnbpts_cos_grad n'a pas le bon nombre d'éléments !\n"
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