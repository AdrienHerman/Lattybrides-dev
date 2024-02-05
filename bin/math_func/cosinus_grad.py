"""
Génération de la structure Cosinus 2D avec gradients
Adrien HERMAN
05/02/2024
"""

def gen_cosinus_grad(	ep=0.4,
						doc=None,
						file_debug=None,
						nb_couches=3,
						ep_par_couche=[1,0.5],
						nb_cos_par_couche=[4,4],
						nb_plateaux_y_par_couche=[2,2],
						amp_par_couche=[1.0,1.0],
						period_fact_par_couche=[0.5,0.5],
						phi_par_couche=[.0,.0],
						nbpts_par_couche=[160,160],
						plot_math_func=None,
						cosinus_func=None,
						dimlat_x=40,
						dimlat_par_couche=[20,20],
						dimlat_ep=40,
						ep_plateaux=[1,1],
						semi_debug=False,
						debug=True,
						sketch_visible=False,
						extrude=True,
						nom_sketch_par_couche=["Sketch_Cos_1_", "Sketch_Cos_2_"],
						nom_sketch_plateaux_extremitees=["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
						nom_body_cos="Body_Cos",
						nom_pad_cos=["Pad_Cos_1_", "Pad_Cos_2_"],
						nom_pad_plateau_extremitees=["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
						gen_cos=None,
						generation_plateaux_extremitees=True,
						wdebug=None):
	"""
	Génération de la structure avec gradients.

	-----------
	Variables :
		- ep -> Épaisseur des parois de la structure lattice
		- doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		- file_debug -> Fichier de déboggage (ouvert)
		- nb_couches -> Nombre de couches différentes à générer
		- ep_par_couche -> Liste de tous les facteurs d'épaisseur à chaque couche (facteur * ep)
		- nb_cos_par_couche -> Nombre de cosinus (en x) par couches de gradient
		- nb_plateaux_y_par_couche -> Nombre de plateaux liant les cosinus par couches de gradients
		- amp_par_couche -> Amplitude du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus) par couche de gradient
		- period_fact_par_couche > Facteur de période du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- phi_par_couche -> Déphasage du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus) par couche de gradient
		- nbpts_par_couche -> Nombre de points d'échantillonnage de la courbe par couche de gradient
		- plot_math_func -> Fonction de traçage de fonction mathématiques
		- dimlat_x / dimlat_y -> Dimensions de la zone de construction
		- dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		- ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
					   [Épaisseur du plateau du dessous, Épaisseur du plateau du dessus]
		- semi_debug -> Tracer les lignes de construction
		- debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		- sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		- extrude -> Réaliser l'extrusion = True
		- nom_sketch_par_couche -> Nom de l'esquisse du motif cosinus par couches
		- nom_sketch_plateaux_extremitees -> Nom des esquisses de définition des plateaux
		- nom_body_cos -> Nom de la pièce
		- nom_pad_cos -> Nom du pad du motif cosinus
		- nom_pad_plateau -> Nom des pad des plateaux liant les parties hautes et basses de la structure
		- gen_cos -> Fonction de génération de la structure lattice cosinus
		- generation_plateaux_extremitees -> True = Les plateaux aux extrémités sont générés, False = Génération des plateaux ignorés
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher

	if doc == None: FreeCAD.newDocument()						# Création du document
	posy = 0 													# Position y de l'origine des esquisses à créer
	sketches = []												# Liste contenant toutes les esquisses des cosinus

	if file_debug != None and debug:
		wdebug("Création du body du cosinus : {0}\n".format(nom_body_cos), file_debug)

	body = doc.addObject('PartDesign::Body', nom_body_cos)	# Créer un body

	for no_couche in range(nb_couches):
		if file_debug != None and debug:
			wdebug("""Génération de la structure losange pour la couche {0}:\n     posy = {1}\n""".format(	no_couche,
																											posy), file_debug)

		# Génération de la structure sur le couche no_couche
		gen_cos(	ep=ep*ep_par_couche[no_couche],
					doc=doc,
					file_debug=file_debug,
					nb_cos=nb_cos_par_couche[no_couche],
					nb_plateaux_y=nb_plateaux_y_par_couche[no_couche],
					amp=amp_par_couche[no_couche],
					period_fact=period_fact_par_couche[no_couche],
					phi=phi_par_couche[no_couche],
					nbpts=nbpts_par_couche[no_couche],
					plot_math_func=plot_math_func,
					cosinus_func=cosinus_func,
					dimlat_x=dimlat_x,
					dimlat_y=dimlat_par_couche[no_couche],
					dimlat_ep=dimlat_ep,
					ep_plateaux=ep_plateaux,
					semi_debug=semi_debug,
					debug=debug,
					sketch_visible=sketch_visible,
					extrude=extrude,
					nom_sketch_cos=nom_sketch_par_couche[no_couche],
					nom_sketch_plateaux_extremitees=nom_sketch_plateaux_extremitees[no_couche],
					nom_body_cos=nom_body_cos,
					nom_pad_cos=nom_pad_cos[no_couche],
					nom_pad_plateau_extremitees=nom_pad_plateau_extremitees,
					generation_plateaux_extremitees=generation_plateaux_extremitees,
					wdebug=wdebug,
					create_body=False,
					posy=posy,
					remove_fusion=False)

		# Incrément de la position y dans le repère
		posy += dimlat_par_couche[no_couche]