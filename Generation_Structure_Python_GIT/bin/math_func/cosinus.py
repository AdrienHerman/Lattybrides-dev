"""
Génération de la structure cosinus.
Base du code de Valentin BACOUT.
Implémentation par Adrien HERMAN.
16/01/2024
"""

def cosinus_fct(x, phi, period_fact, amp):
	"""
	Calcul du cos(x + phi) (x et phi en radians).
	"""
	import math
	return amp * math.cos(x * period_fact + phi)

def gen_cosinus(	ep=0.4,
					doc=None,
					file_debug=None,
					nb_cos_x=4,
					nb_cos_y=4,
					amp_x=1.0,
					period_fact_x=0.5,
					phi_x=.0,
					amp_y=1.0,
					period_fact_y=0.5,
					phi_y=.0,
					nbpts=160,
					plot_math_func=None,
					dimlat_x=40,
					dimlat_y=40,
					dimlat_ep=40,
					ep_plateaux=[1,1],
					semi_debug=False,
					debug=True,
					sketch_visible=False,
					extrude=True,
					nom_sketch_cos="Sketch_Cos",
					nom_sketch_plateaux_extremitees=["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
					nom_body_cos="Body_Cos",
					nom_pad_cos="Pad_Cos",
					nom_pad_plateau_extremitees=["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
					gen_plateaux=None,
					generation_plateaux_extremitees=True,
					wdebug=None):
	"""
	Génération de la structure de base.

	-----------
	Variables :
		- ep -> Épaisseur des parois de la structure lattice
		- doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		- file_debug -> Fichier de déboggage (ouvert)
		- nb_cos_x / nb_cos_y -> Nombre de cosinus sur la distance x / y
		- amp_x/y -> Amplitude du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- period_fact_x/y > Facteur de période du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- phi_x/y -> Déphasage du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- nbpts -> Nombre de points d'échantillonnage de la courbe
		- plot_math_func -> Fonction de traçage de fonction mathématiques
		- dimlat_x / dimlat_y -> Dimensions de la zone de construction
		- dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		- ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
					   [Épaisseur du plateau du dessous, Épaisseur du plateau du dessus]
		- semi_debug -> Tracer les lignes de construction
		- debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		- sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		- extrude -> Réaliser l'extrusion = True
		- nom_sketch_cos -> Nom de l'esquisse du motif cosinus
		- nom_sketch_plateaux_extremitees -> Nom des esquisses de définition des plateaux
		- nom_body_cos -> Nom de la pièce
		- nom_pad_cos -> Nom du pad du motif cosinus
		- nom_pad_plateau -> Nom des pad des plateaux liant les parties hautes et basses de la structure
		- gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		- generation_plateaux_extremitees -> True = Les plateaux aux extrémités sont générés, False = Génération des plateaux ignorés
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher

	# Vérification des données
	list_type = False
	if type(period_fact_x) == list and type(period_fact_y) == list and type(phi_x) == list and type(phi_y) == list and type(amp_x) == list and type(amp_y) == list:
		list_type = True
		if not (len(period_fact_x) == len(phi_x) == len(amp_x) == nb_cos_x) or not (len(period_fact_y) == len(phi_y) == len(amp_y) == nb_cos_y):
			if file_debug != None and debug:
				wdebug("""\nERREUR : period_fact_x ({0}), period_fact_y ({1}), amp_x ({6}), amp_y ({7}),
							phi_x ({2}), phi_y ({3}) ne sont pas de même dimension
							que nb_cos_x ({4}) et que nb_cos_y ({5}) !""".format(	len(period_fact_x),
																					len(period_fact_y),
																					len(phi_x),
																					len(phi_y),
																					nb_cos_x,
																					nb_cos_y,
																					len(amp_x),
																					len(amp_y)),
																					file_debug)
			return

	elif type(period_fact_x) == list or type(period_fact_y) == list or type(phi_x) == list or type(phi_y) == list or type(amp_x) == list or type(amp_y) == list:
		if type(period_fact_x) != list or type(period_fact_y) != list or type(phi_x) != list or type(phi_y) != list or type(amp_x) != list or type(amp_y) != list:
			if file_debug != None and debug:
				wdebug("""\nERREUR : period_fact_x ({0}), period_fact_y ({1}),
							phi_x ({2}), phi_y({3}), amp_x ({4}), amp_y ({5}) 
							ne sont pas tous du type list !""".format(	type(period_fact_x),
																		type(period_fact_y),
																		type(phi_x),
																		type(phi_y),
																		type(amp_x),
																		type(amp_y)),
																		file_debug)
			return

	# Création du document
	if doc == None:	doc = FreeCAD.newDocument()

	if file_debug != None and debug: wdebug("""dimlat_x:{0}
												\ndimlat_y:{1}
												\ndimlat_ep:{2}
												\nnb_cos_x:{3}
												\nnb_cos_y:{4}
												\nnom_sketch_cos:{5}
												\nperiod_fact_x:{6}
												\nphi_x:{7}
												\nperiod_fact_y:{8}
												\nphi_y:{8}
												\n----\n""".format(	dimlat_x,
																	dimlat_y,
																	dimlat_ep,
																	nb_cos_x,
																	nb_cos_y,
																	nom_sketch_cos,
																	period_fact_x,
																	phi_x,
																	period_fact_y,
																	phi_y),
																	file_debug)

	"""
	-------------------------------
	--- Variables de l'objet 3D ---
	-------------------------------
	Note : Toutes les dimensions sont exprimées en mm et réfèrent au schéma
	"""
	# Dimensions caractéristiques du triangle calculées (voir schéma)
	espacement_x = dimlat_x / nb_cos_x
	espacement_y = dimlat_y / nb_cos_y
	if file_debug != None and debug: wdebug("""espacement_x:{0}
												\nespacement_y:{1}
												\n----\n""".format(	espacement_x,
																	espacement_y),
																	file_debug)

	# Création d'un nouveau corps
	if file_debug != None and debug:
		wdebug("Création du body du cosinus : {0}\n".format(nom_body_cos), file_debug)

	body = doc.addObject('PartDesign::Body', nom_body_cos)

	# Construction du rectangle de délimitation de la structure
	#	Points de délimitation du quadrilatère (dans le sens anti-horaire)
	point_delimitation = (	App.Vector(0, 0, 0),
							App.Vector(dimlat_x, 0, 0),
							App.Vector(dimlat_x, dimlat_y, 0),
							App.Vector(0, dimlat_y, 0))

	# Génération du plateau du bas
	if extrude and generation_plateaux_extremitees:
		# Génération des plateaux liants les extrémités
		if file_debug != None and debug:
			wdebug("Création du plateau liants l'extrémité basse de la structure'.\n", file_debug)

		gen_plateaux(	nb_couches=1,
						ep_plateaux=ep_plateaux,
						dimlat_x=dimlat_x,
						dimlat_par_couche=[0],
						dimlat_ep=dimlat_ep,
						sketch_visible=sketch_visible,
						nom_body=nom_body_cos,
						doc=doc,
						nom_sketch_plateaux=nom_sketch_plateaux_extremitees,
						nom_pad_plateaux=nom_pad_plateau_extremitees,
						debug=debug,
						file_debug=file_debug,
						wdebug=wdebug)
	elif not extrude and generation_plateaux_extremitees:
		# Génération des plateaux liants les extrémités
		if file_debug != None and debug:
			wdebug("ATTENTION : Des problèmes de calculs vont survenir (Multiple shape is not supported) !\n", file_debug)

	current_pos = (.0, .0, .0)	# Curseur de position (repère local à chaque cosinus)
	sketch_cos_x = []			# Liste contenant toutes les esquisses des cosinus suivant l'axe x
	pad_cos_x = []				# Liste contenant tous les pads des cosinus suivant l'axe x
	sketch_cos_y = []			# Liste contenant toutes les esquisses des cosinus suivant l'axe y
	pad_cos_y = []				# Liste contenant tous les pads des cosinus suivant l'axe y

	# Création des cosinus suivant l'axe x
	for i in range(nb_cos_x):
		if file_debug != None and debug:
			wdebug("Création du cosinus suivant l'axe x numéro {0}.\n".format(i + 1), file_debug)

		# Création de l'esquisse
		sketch_cos_x.append(doc.addObject("Sketcher::SketchObject", nom_sketch_cos))
		if file_debug != None and debug:
			wdebug("Création de l'esquisse du cosinus.\n", file_debug)

		#	Construction du quadrilatère si le mode semi_debug est activé
		if semi_debug:
			for j in range(1, 5):
				sketch_cos_x[i].addGeometry(Part.LineSegment(point_delimitation[(j - 1) % 4], point_delimitation[j % 4]), True)
				if file_debug != None and debug:
					wdebug("\n\n     Construction du rectangle de délimitation de la structure\n", file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	point_delimitation[(j - 1) % 4].x,
																											point_delimitation[(j - 1) % 4].y,
																											point_delimitation[(j - 1) % 4].z,
																											point_delimitation[j % 4].x,
																											point_delimitation[j % 4].y,
																											point_delimitation[j % 4].z),
																											file_debug)
				wdebug("\n", file_debug)

		if list_type:
			phi_ = phi_x[i]
			period_fact_ = period_fact_x[i]
			amp_ = amp_x[i]
		else:
			phi_ =  phi_x
			period_fact_ = period_fact_x
			amp_ = amp_x

		# Traçage des deux cosinus
		current_pos = (i * espacement_x - ep / 2 + espacement_x / 2, .0, .0)
		[echant_1, pts_1], d, s = plot_math_func(	nbpts,
													0,
													dimlat_y,
													current_pos,
													cosinus_fct,
													True,
													False,
													doc,
													sketch_cos_x[i],
													debug,
													file_debug,
													wdebug,
													phi_,
													period_fact_,
													amp_)

		current_pos = (i * espacement_x + ep / 2 + espacement_x / 2, .0, .0)
		[echant_2, pts_2], d, s = plot_math_func(	nbpts,
													0,
													dimlat_y,
													current_pos,
													cosinus_fct,
													True,
													False,
													doc,
													sketch_cos_x[i],
													debug,
													file_debug,
													wdebug,
													phi_,
													period_fact_,
													amp_)
		if file_debug != None and debug:
			wdebug("Traçage des deux parties du cosinus.\n", file_debug)

		# Fermeture du contour
		sketch_cos_x[i].addGeometry(Part.LineSegment(	App.Vector(pts_1[0], echant_1[0], 0),
														App.Vector(pts_2[0], echant_2[0], 0)),
														False)
		sketch_cos_x[i].addGeometry(Part.LineSegment(	App.Vector(pts_1[-1], echant_1[-1], 0),
														App.Vector(pts_2[-1], echant_2[-1], 0)),
														False)
		if file_debug != None and debug:
			wdebug("Fermeture du contour.\n", file_debug)

		# Extrusion du contour
		if extrude:
			pad_cos_x.append(body.newObject('PartDesign::Pad', nom_pad_cos))	# Créer un Pad
			pad_cos_x[i].Profile = sketch_cos_x[i]								# Mettre l'esquisse dans le pad
			pad_cos_x[i].Length = dimlat_ep										# Définir la longueur d'extrustion
			pad_cos_x[i].ReferenceAxis = (sketch_cos_x[i], ['N_Axis'])			# Définir la direction d'extrusion
			doc.recompute()														# Lancer les calculs
			sketch_cos_x[i].Visibility = sketch_visible							# Affichage de l'esquisse après l'extrusion
			if file_debug != None and debug:
				wdebug("Extrusion de la structure\n", file_debug)

	if file_debug != None and debug:
		wdebug("{0} cosinus suivant l'axe x ont étés tracés avec succès.\n".format(nb_cos_x), file_debug)

	# Création des cosinus suivant l'axe y
	for i in range(nb_cos_y):
		if file_debug != None and debug:
			wdebug("Création du cosinus suivant l'axe y numéro {0}.\n".format(i + 1), file_debug)

		# Création de l'esquisse
		sketch_cos_y.append(doc.addObject("Sketcher::SketchObject", nom_sketch_cos))
		if file_debug != None and debug:
			wdebug("Création de l'esquisse du cosinus.\n", file_debug)

		#	Construction du quadrilatère si le mode semi_debug est activé
		if semi_debug:
			for j in range(1, 5):
				sketch_cos_y[i].addGeometry(Part.LineSegment(point_delimitation[(j - 1) % 4], point_delimitation[j % 4]), True)
				if file_debug != None and debug:
					wdebug("\n\n     Construction du rectangle de délimitation de la structure\n", file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	point_delimitation[(j - 1) % 4].x,
																											point_delimitation[(j - 1) % 4].y,
																											point_delimitation[(j - 1) % 4].z,
																											point_delimitation[j % 4].x,
																											point_delimitation[j % 4].y,
																											point_delimitation[j % 4].z),
																											file_debug)
				wdebug("\n", file_debug)

		if list_type:
			phi_ = phi_y[i]
			period_fact_ = period_fact_y[i]
			amp_ = amp_y[i]
		else:
			phi_ =  phi_y
			period_fact_ = period_fact_y
			amp_ = amp_y

		# Traçage des deux cosinus
		current_pos = (.0, i * espacement_y - ep / 2 + espacement_y / 2, .0)
		[echant_1, pts_1], d, s = plot_math_func(	nbpts,
													0,
													dimlat_x,
													current_pos,
													cosinus_fct,
													False,
													True,
													doc,
													sketch_cos_y[i],
													debug,
													file_debug,
													wdebug,
													phi_,
													period_fact_,
													amp_)

		current_pos = (.0, i * espacement_y + ep / 2 + espacement_y / 2, .0)
		[echant_2, pts_2], d, s = plot_math_func(	nbpts,
													0,
													dimlat_x,
													current_pos,
													cosinus_fct,
													False,
													True,
													doc,
													sketch_cos_y[i],
													debug,
													file_debug,
													wdebug,
													phi_,
													period_fact_,
													amp_)
		if file_debug != None and debug:
			wdebug("Traçage des deux parties du cosinus.\n", file_debug)

		# Fermeture du contour
		sketch_cos_y[i].addGeometry(Part.LineSegment(	App.Vector(echant_1[0], pts_1[0], 0),
														App.Vector(echant_2[0], pts_2[0], 0)),
														False)
		sketch_cos_y[i].addGeometry(Part.LineSegment(	App.Vector(echant_1[-1], pts_1[-1], 0),
														App.Vector(echant_2[-1], pts_2[-1], 0)),
														False)
		if file_debug != None and debug:
			wdebug("Fermeture du contour.\n", file_debug)

		# Extrusion du contour
		if extrude:
			pad_cos_y.append(body.newObject('PartDesign::Pad', nom_pad_cos))	# Créer un Pad
			pad_cos_y[i].Profile = sketch_cos_y[i]								# Mettre l'esquisse dans le pad
			pad_cos_y[i].Length = dimlat_ep										# Définir la longueur d'extrustion
			pad_cos_y[i].ReferenceAxis = (sketch_cos_y[i], ['N_Axis'])			# Définir la direction d'extrusion
			doc.recompute()														# Lancer les calculs
			sketch_cos_y[i].Visibility = sketch_visible							# Affichage de l'esquisse après l'extrusion
			if file_debug != None and debug:
				wdebug("Extrusion de la structure\n", file_debug)

	if file_debug != None and debug:
		wdebug("{0} cosinus suivant l'axe y ont étés tracés avec succès.\n".format(nb_cos_y), file_debug)

	# Génération du plateau du haut
	if extrude and generation_plateaux_extremitees:
		# Génération des plateaux liants les extrémités
		if file_debug != None and debug:
			wdebug("Création des plateaux liants les extrémités de la structure.\n", file_debug)

		gen_plateaux(	nb_couches=1,
						ep_plateaux=ep_plateaux,
						dimlat_x=dimlat_x,
						dimlat_par_couche=[dimlat_y],
						dimlat_ep=dimlat_ep,
						sketch_visible=sketch_visible,
						nom_body=nom_body_cos,
						doc=doc,
						nom_sketch_plateaux=nom_sketch_plateaux_extremitees,
						nom_pad_plateaux=nom_pad_plateau_extremitees,
						debug=debug,
						file_debug=file_debug,
						wdebug=wdebug)