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
					nb_cos=4,
					nb_plateaux_y=4,
					amp=1.0,
					period_fact=0.5,
					phi=.0,
					nbpts=160,
					plot_math_func=None,
					cosinus_func=None,
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
					generation_plateaux_extremitees=True,
					wdebug=None,
					create_body=True,
					posy=0,
					remove_fusion=True):
	"""
	Génération de la structure de base.

	-----------
	Variables :
		- ep -> Épaisseur des parois de la structure lattice
		- doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		- file_debug -> Fichier de déboggage (ouvert)
		- nb_cos -> Nombre de cosinus sur la distance
		- amp -> Amplitude du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- period_fact > Facteur de période du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- phi -> Déphasage du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- nbpts -> Nombre de points d'échantillonnage de la courbe
		- plot_math_func -> Fonction de traçage de fonction mathématiques
		- cosinus_func -> Fonction de calcul de points (cosinus)
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
		- generation_plateaux_extremitees -> True = Les plateaux aux extrémités sont générés, False = Génération des plateaux ignorés
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		- create_body -> True s'il faut créer le body
		- posy -> Position en y de l'esquisse
		- remove_fusion -> True s'il faut enlever le pad et le sketch de fusion du solide
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher

	# Vérification des données
	list_type = False
	if type(period_fact) == list and type(phi) == list and type(amp) == list :
		list_type = True
		if not (len(period_fact) == len(phi) == len(amp) == nb_cos):
			if file_debug != None and debug:
				wdebug("""\nERREUR : period_fact ({0}), amp ({6}),
							phi ({2}) ne sont pas de même dimension
							que nb_cos ({4}) !""".format(	len(period_fact),
																					len(phi),
																					nb_cos,
																					len(amp)),
																					file_debug)
			return

	elif type(period_fact) == list or type(phi) == list or type(amp) == list :
		if type(period_fact) != list or type(phi) != list or type(amp) != list :
			if file_debug != None and debug:
				wdebug("""\nERREUR : period_fact ({0}),
							phi ({1}), amp ({2})) 
							ne sont pas tous du type list !""".format(	type(period_fact),
																		type(phi),
																		type(amp)),
																		file_debug)
			return

	# Création du document
	if doc == None:	doc = FreeCAD.newDocument()

	if file_debug != None and debug: wdebug("""dimlat_x:{0}
												\ndimlat_y:{1}
												\ndimlat_ep:{2}
												\nnb_cos:{3}
												\nnb_cos:{4}
												\nnom_sketch_cos:{5}
												\nperiod_fact:{6}
												\nphi:{7}
												\amp:{8}
												\n----\n""".format(	dimlat_x,
																	dimlat_y,
																	dimlat_ep,
																	nb_cos,
																	nb_cos,
																	nom_sketch_cos,
																	period_fact,
																	phi,
																	amp),
																	file_debug)

	"""
	-------------------------------
	--- Variables de l'objet 3D ---
	-------------------------------
	Note : Toutes les dimensions sont exprimées en mm et réfèrent au schéma
	"""
	# Dimensions caractéristiques du triangle calculées (voir schéma)
	espacement = dimlat_x / nb_cos
	espacement_plateaux = dimlat_y / nb_plateaux_y
	if file_debug != None and debug: wdebug("""espacement:{0}
												\nespacement_plateaux:{1}
												\n----\n""".format(	espacement,
																	espacement_plateaux),
																	file_debug)

	# Création d'un nouveau corps
	if create_body:
		if file_debug != None and debug:
			wdebug("Création du body du cosinus : {0}\n".format(nom_body_cos), file_debug)

		body = doc.addObject('PartDesign::Body', nom_body_cos)

	else:
		body = doc.getObject(nom_body_cos)

	# Construction du rectangle de délimitation de la structure
	#	Points de délimitation du quadrilatère (dans le sens anti-horaire)
	point_delimitation = (	App.Vector(0, 0, 0),
							App.Vector(dimlat_x, 0, 0),
							App.Vector(dimlat_x, dimlat_y, 0),
							App.Vector(0, dimlat_y, 0))

	# Génération d'un contour pour fusionner le solide
	if extrude and generation_plateaux_extremitees:
		point_fusion = (	App.Vector(0, 0, 0),
							App.Vector(0.05, 0, 0),
							App.Vector(dimlat_x, dimlat_y, 0),
							App.Vector(dimlat_x - 0.05, dimlat_y, 0))

		sketch_fusion = doc.addObject("Sketcher::SketchObject", "FusionSketch")
		sketch_fusion.Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))
		for j in range(1, 5):	sketch_fusion.addGeometry(Part.LineSegment(point_fusion[(j - 1) % 4], point_fusion[j % 4]), False)

		pad_fusion = body.newObject('PartDesign::Pad', "FusionPad")	# Créer un Pad
		pad_fusion.Profile = sketch_fusion							# Mettre l'esquisse dans le pad
		pad_fusion.Length = dimlat_ep								# Définir la longueur d'extrustion
		pad_fusion.ReferenceAxis = (sketch_fusion, ['N_Axis'])		# Définir la direction d'extrusion

		# Génération des plateaux liants les extrémités
		if file_debug != None and debug:
			wdebug("Création des plateaux liants les extrémités de la structure.\n", file_debug)

		point_plateau_dessous = (	App.Vector(0, 0, 0),
									App.Vector(dimlat_x, 0, 0),
									App.Vector(dimlat_x, ep_plateaux[0], 0),
									App.Vector(0, ep_plateaux[0], 0))

		sketch_plateau_dessous = doc.addObject("Sketcher::SketchObject", nom_sketch_plateaux_extremitees[0])
		sketch_plateau_dessous.Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))
		for j in range(1, 5):	sketch_plateau_dessous.addGeometry(Part.LineSegment(point_plateau_dessous[(j - 1) % 4], point_plateau_dessous[j % 4]), False)
		sketch_plateau_dessous.Visibility = sketch_visible	

		pad_plateau_dessous = body.newObject('PartDesign::Pad', nom_pad_plateau_extremitees[0])	# Créer un Pad
		pad_plateau_dessous.Profile = sketch_plateau_dessous									# Mettre l'esquisse dans le pad
		pad_plateau_dessous.Length = dimlat_ep													# Définir la longueur d'extrustion
		pad_plateau_dessous.ReferenceAxis = (sketch_plateau_dessous, ['N_Axis'])				# Définir la direction d'extrusion
		doc.recompute()																			# Lancer les calculs

	else:
		# Génération des plateaux liants les extrémités
		if file_debug != None and debug:
			wdebug("ATTENTION : Des problèmes de calculs vont survenir (Multiple shape is not supported) !\n", file_debug)
		return

	current_pos = (.0, .0, .0)	# Curseur de position (repère local à chaque cosinus)
	sketch_cos_x = []			# Liste contenant toutes les esquisses des cosinus suivant l'axe x
	pad_cos_x = []				# Liste contenant tous les pads des cosinus suivant l'axe x
	sketch_cos_y = []			# Liste contenant toutes les esquisses des cosinus suivant l'axe y
	pad_cos_y = []				# Liste contenant tous les pads des cosinus suivant l'axe y

	# Création des cosinus suivant l'axe x
	for i in range(nb_cos):
		if file_debug != None and debug:
			wdebug("Création du cosinus suivant l'axe x numéro {0}.\n".format(i + 1), file_debug)

		# Création de l'esquisse
		sketch_cos_x.append(doc.addObject("Sketcher::SketchObject", nom_sketch_cos))
		sketch_cos_x[i].Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))
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
			phi_ = phi[i]
			period_fact_ = period_fact[i]
			amp_ = amp[i]
		else:
			phi_ =  phi
			period_fact_ = period_fact
			amp_ = amp

		# Traçage des deux cosinus
		current_pos = (i * espacement - ep / 2 + espacement / 2, .0, .0)
		[echant_1, pts_1], d, s = plot_math_func(	nbpts,
													0,
													dimlat_y,
													current_pos,
													cosinus_func,
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

		current_pos = (i * espacement + ep / 2 + espacement / 2, .0, .0)
		[echant_2, pts_2], d, s = plot_math_func(	nbpts,
													0,
													dimlat_y,
													current_pos,
													cosinus_func,
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
		wdebug("{0} cosinus suivant l'axe x ont étés tracés avec succès.\n".format(nb_cos), file_debug)

	# Génération des plateaux liants la structure dans la direction y
	sketch_plateau = []
	pad_plateau = []
	for i in range(nb_plateaux_y):
		# Calcul de la position et des points
		current_pos = espacement_plateaux * (i + 1)
		point_plateau = (	App.Vector(0, current_pos - ep_plateaux[0] / 2, 0),
							App.Vector(dimlat_x, current_pos - ep_plateaux[0] / 2, 0),
							App.Vector(dimlat_x, current_pos + ep_plateaux[0] / 2, 0),
							App.Vector(0, current_pos + ep_plateaux[0] / 2, 0))

		# Création de l'esquisse et traçage des lignes
		sketch_plateau.append(doc.addObject("Sketcher::SketchObject", "Sketch_Plateau_Y{0}".format(i)))
		sketch_plateau[i].Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))
		for j in range(1, 5):	sketch_plateau[i].addGeometry(Part.LineSegment(point_plateau[(j - 1) % 4], point_plateau[j % 4]), False)
		sketch_plateau[i].Visibility = sketch_visible

		# Création du pad et extrusion
		if extrude:
			pad_plateau.append(body.newObject('PartDesign::Pad', "Pad_Plateau_Y{0}".format(i)))	# Créer un Pad
			pad_plateau[i].Profile = sketch_plateau[i]											# Mettre l'esquisse dans le pad
			pad_plateau[i].Length = dimlat_ep													# Définir la longueur d'extrustion
			pad_plateau[i].ReferenceAxis = (sketch_plateau[i], ['N_Axis'])						# Définir la direction d'extrusion
			doc.recompute()

	if file_debug != None and debug:
		wdebug("{0} plateaux liants suivant les cosinus ont été tracés avec succès.\n".format(nb_plateaux_y), file_debug)

	# Génération du plateau du dessous
	if extrude and generation_plateaux_extremitees:
		point_plateau_dessous = (	App.Vector(0, dimlat_y - ep_plateaux[1], 0),
									App.Vector(dimlat_x, dimlat_y - ep_plateaux[1], 0),
									App.Vector(dimlat_x, dimlat_y, 0),
									App.Vector(0, dimlat_y, 0))

		sketch_plateau_dessus = doc.addObject("Sketcher::SketchObject", nom_sketch_plateaux_extremitees[1])
		sketch_plateau_dessus.Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))
		for j in range(1, 5):	sketch_plateau_dessus.addGeometry(Part.LineSegment(point_plateau_dessous[(j - 1) % 4], point_plateau_dessous[j % 4]), False)
		sketch_plateau_dessus.Visibility = sketch_visible	

		pad_plateau_dessus = body.newObject('PartDesign::Pad', nom_pad_plateau_extremitees[1])	# Créer un Pad
		pad_plateau_dessus.Profile = sketch_plateau_dessus										# Mettre l'esquisse dans le pad
		pad_plateau_dessus.Length = dimlat_ep													# Définir la longueur d'extrustion
		pad_plateau_dessus.ReferenceAxis = (sketch_plateau_dessus, ['N_Axis'])					# Définir la direction d'extrusion

		# Suppression du solide de fusion de la structure
		if remove_fusion:
			doc.removeObject("FusionPad")
			doc.removeObject("FusionSketch")

		doc.recompute()