"""
Génération d'une structure lattice à base de losanges
HERMAN Adrien
02/10/2023
"""

def gen_losange(	ep=0.4,
					doc=None,
					file_debug=None,
					nb_losange_x=10,
					nb_losange_y=15,
					dimlat_ep=5,
					dimlat_x=20,
					dimlat_y=20,
					ep_plateaux=[1,1],
					semi_debug=False,
					debug=False,
					sketch_visible=False,
					extrude=True,
					nom_sketch_losange="Sketch_Losange",
					nom_sketch_plateaux_extremitees=["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
					nom_body_losange="Body_Losange",
					nom_pad_losange="Pad_Losange",
					nom_pad_plateau_extremitees=["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
					gen_plateaux=None,
					generation_plateaux_extremitees=True,
					wdebug=None,
					sketch=""):
	"""
	Génération de la structure de base (juste les losanges)

	-----------
	Variables :
		ep -> Épaisseur des parois de la structure lattice
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		file_debug -> Fichier de déboggage (ouvert)
		nb_losange_x / nb_losange_y -> Nombre de losanges sur la distance x / y
		dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		dimlat_x / dimlat_y -> Dimensions de la zone de construction
		ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
					   [Épaisseur du plateau du dessous, Épaisseur du plateau du dessus]
		semi_debug -> Tracer les lignes de construction
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		extrude -> Réaliser l'extrusion = True
		nom_sketch_losange -> Nom de l'esquisse du losange
		nom_sketch_plateaux_extremitees -> Nom des esquisses de définition des plateaux
		nom_body_losange -> Nom de la pièce
		nom_pad_losange -> Nom du pad du losange
		nom_pad_plateau -> Nom des pad des plateaux liant les parties hautes et basses de la structure
		gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		generation_plateaux_extremitees -> True = Les plateaux aux extrémités sont générés, False = Génération des plateaux ignorés
		wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		sketch -> Objet contenant l'esquisse de la structure losange
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher, math, sys

	if doc == None:	doc = FreeCAD.newDocument()

	"""
	-------------------------------
	--- Variables de l'objet 3D ---
	-------------------------------
	Note : Toutes les dimensions sont exprimées en mm
	"""
	# Listes de points utilisés
	liste_points_dessous = [[None for i in range(nb_losange_x)] for j in range(nb_losange_y * 2)]
	liste_points_dessus = [[None for i in range(nb_losange_x)] for j in range(nb_losange_y * 2)]
	liste_points_construction = [[None for i in range(nb_losange_x)] for j in range(nb_losange_y * 2)]
	if file_debug != None and debug: wdebug("""dimlat_x:{0}
												\ndimlat_y:{1}
												\ndimlat_ep:{2}
												\nnb_losange_x:{3}
												\nnb_losange_y:{4}
												\nnom_sketch_losange:{5}
												\n----\n""".format(	dimlat_x,
																	dimlat_y,
																	dimlat_ep,
																	nb_losange_x,
																	nb_losange_y,
																	nom_sketch_losange),
																	file_debug)

	# Dimensions caractéristiques du losange calculées (voir schéma)
	lx = dimlat_x / nb_losange_x
	ly = dimlat_y / nb_losange_y
	cote = 0.5 * math.sqrt(lx ** 2 + ly ** 2)
	alpha = math.acos(0.5 * lx / cote)
	epx = ep / (2 * math.sin(alpha))
	epy = ep / (2 * math.cos(alpha))
	if file_debug != None and debug: wdebug("""ep:{0}
												\nlx:{1}
												\nly:{2}
												\ncote:{3}
												\nalpha:{4}
												\nepx:{5}
												\nepy:{6}
												\n----\n""".format(	ep,
																	lx,
																	ly,
																	cote,
																	alpha,
																	epx,
																	epy),
																	file_debug)
	
	"""
	-----------------------
	--- Modélisation 2D ---
	-----------------------
	"""
	# Création d'une nouvelle esquisse et de la pièce
	if sketch == "":
		sketch = doc.addObject("Sketcher::SketchObject", nom_sketch_losange)
		doc.addObject('PartDesign::Body', nom_body_losange)

	if file_debug != None and debug:
		wdebug("Création de l'esquisse du losange : {0}\n".format(nom_sketch_losange), file_debug)
		wdebug("Création du body du losange : {0}\n".format(nom_body_losange), file_debug)

	# Construction du rectangle de délimitation de la structure
	#	Points de délimitation du quadrilatère (dans le sens anti-horaire)
	point_delimitation = (	App.Vector(0, 0, 0),
							App.Vector(dimlat_x, 0, 0),
							App.Vector(dimlat_x, dimlat_y, 0),
							App.Vector(0, dimlat_y, 0))
	#	Construction du quadrilatère si le mode semi_debug est activé
	if semi_debug:
		for i in range(1, 5):
			sketch.addGeometry(Part.LineSegment(point_delimitation[(i - 1) % 4], point_delimitation[i % 4]), True)
			if file_debug != None and debug:
				wdebug("\n\n     Construction du rectangle de délimitation de la structure\n", file_debug)
				wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	point_delimitation[(i - 1) % 4].x,
																										point_delimitation[(i - 1) % 4].y,
																										point_delimitation[(i - 1) % 4].z,
																										point_delimitation[i % 4].x,
																										point_delimitation[i % 4].y,
																										point_delimitation[i % 4].z),
																										file_debug)
				wdebug("\n", file_debug)

	# Curseur de position (repère local à chaque losange)
	current_pos = (0,0,0)

	# i = Numéro de losange y (ligne)
	# j = Numéro de losange x (colonne)
	for j in range(nb_losange_y * 2):
		for i in range(nb_losange_x):
			current_pos = (lx * i, (ly / 2) * j, 0)

			if j % 2 == 0:
				# Structure orientée à droite (partie haute du losange)
				# Dessous
				liste_points_dessous[j][i] = (	App.Vector(current_pos[0] + epx, current_pos[1], current_pos[2]),
												App.Vector(current_pos[0] + lx / 2, current_pos[1] + ly / 2 - epy, current_pos[2]),
												App.Vector(current_pos[0] + lx - epx, current_pos[1], current_pos[2]))
				sketch.addGeometry(Part.LineSegment(liste_points_dessous[j][i][0], liste_points_dessous[j][i][1]), False)
				sketch.addGeometry(Part.LineSegment(liste_points_dessous[j][i][1], liste_points_dessous[j][i][2]), False)
				# Dessus
				liste_points_dessus[j][i] = (	App.Vector(current_pos[0], current_pos[1] + epy, current_pos[2]),
												App.Vector(current_pos[0] + lx / 2 - epx, current_pos[1] + ly / 2, current_pos[2]),
												App.Vector(current_pos[0] + lx / 2 + epx, current_pos[1] + ly / 2, current_pos[2]),
												App.Vector(current_pos[0] + lx, current_pos[1] + epy, current_pos[2]))
				sketch.addGeometry(Part.LineSegment(liste_points_dessus[j][i][0], liste_points_dessus[j][i][1]), False)
				sketch.addGeometry(Part.LineSegment(liste_points_dessus[j][i][2], liste_points_dessus[j][i][3]), False)

				if semi_debug:
					# Ligne de construction
					liste_points_construction[j][i] = (	App.Vector(current_pos[0], current_pos[1], current_pos[2]),
														App.Vector(current_pos[0] + lx / 2, current_pos[1] +  ly / 2, current_pos[2]),
														App.Vector(current_pos[0] + lx,current_pos[1],current_pos[2]))
					sketch.addGeometry(Part.LineSegment(liste_points_construction[j][i][0], liste_points_construction[j][i][1]), True)
					sketch.addGeometry(Part.LineSegment(liste_points_construction[j][i][1], liste_points_construction[j][i][2]), True)

				if file_debug != None and debug:
					wdebug("\n--- Construction de la ligne x={0} et de la colonne y={1} ---\n".format(j + 1, i + 1), file_debug)
					wdebug("     Ligne dessous\n", file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessous[j][i][0].x,
																											liste_points_dessous[j][i][0].y,
																											liste_points_dessous[j][i][0].z,
																											liste_points_dessous[j][i][1].x,
																											liste_points_dessous[j][i][1].y,
																											liste_points_dessous[j][i][1].z),
																											file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessous[j][i][1].x,
																											liste_points_dessous[j][i][1].y,
																											liste_points_dessous[j][i][1].z,
																											liste_points_dessous[j][i][2].x,
																											liste_points_dessous[j][i][2].y,
																											liste_points_dessous[j][i][2].z),
																											file_debug)
					wdebug("     Ligne dessus\n", file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessus[j][i][0].x,
																											liste_points_dessus[j][i][0].y,
																											liste_points_dessus[j][i][0].z,
																											liste_points_dessus[j][i][1].x,
																											liste_points_dessus[j][i][1].y,
																											liste_points_dessus[j][i][1].z),
																											file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessus[j][i][2].x,
																											liste_points_dessus[j][i][2].y,
																											liste_points_dessus[j][i][2].z,
																											liste_points_dessus[j][i][3].x,
																											liste_points_dessus[j][i][3].y,
																											liste_points_dessus[j][i][3].z),
																											file_debug)
					if semi_debug:
						wdebug("     Ligne de construction\n", file_debug)
						wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_construction[j][i][0].x,
																												liste_points_construction[j][i][0].y,
																												liste_points_construction[j][i][0].z,
																												liste_points_construction[j][i][1].x,
																												liste_points_construction[j][i][1].y,
																												liste_points_construction[j][i][1].z),
																												file_debug)
						wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_construction[j][i][1].x,
																												liste_points_construction[j][i][1].y,
																												liste_points_construction[j][i][1].z,
																												liste_points_construction[j][i][2].x,
																												liste_points_construction[j][i][2].y,
																												liste_points_construction[j][i][2].z),
																												file_debug)
			else:
				# Structure orientée à gauche (partie basse du losange)
				# Dessous
				liste_points_dessous[j][i] = (	App.Vector(current_pos[0] + lx / 2 - epx, current_pos[1], current_pos[2]),
												App.Vector(current_pos[0], current_pos[1] + ly / 2 - epy, current_pos[2]),
												App.Vector(current_pos[0] + lx / 2 + epx, current_pos[1], current_pos[2]),
												App.Vector(current_pos[0] + lx, current_pos[1] + ly / 2 - epy, current_pos[2]))
				sketch.addGeometry(Part.LineSegment(liste_points_dessous[j][i][0], liste_points_dessous[j][i][1]), False)
				sketch.addGeometry(Part.LineSegment(liste_points_dessous[j][i][2], liste_points_dessous[j][i][3]), False)
				# Dessus
				liste_points_dessus[j][i] = (	App.Vector(current_pos[0] + epx, current_pos[1] + ly / 2, current_pos[2]),
												App.Vector(current_pos[0] + lx / 2, current_pos[1] + epy, current_pos[2]),
												App.Vector(current_pos[0] + lx - epx, current_pos[1] + ly / 2, current_pos[2]))
				sketch.addGeometry(Part.LineSegment(liste_points_dessus[j][i][0], liste_points_dessus[j][i][1]), False)
				sketch.addGeometry(Part.LineSegment(liste_points_dessus[j][i][1], liste_points_dessus[j][i][2]), False)

				if semi_debug:
					# Ligne de construction
					liste_points_construction[j][i] = (	App.Vector(current_pos[0], current_pos[1] + ly / 2, current_pos[2]),
														App.Vector(current_pos[0] + lx / 2, current_pos[1], current_pos[2]),
														App.Vector(current_pos[0] + lx, current_pos[1] + ly / 2, current_pos[2]))
					sketch.addGeometry(Part.LineSegment(liste_points_construction[j][i][0], liste_points_construction[j][i][1]), True)
					sketch.addGeometry(Part.LineSegment(liste_points_construction[j][i][1], liste_points_construction[j][i][2]), True)

				if file_debug != None and debug:
					wdebug("\n--- Construction de la ligne x={0} et de la colonne y={1} ---\n".format(j + 1, i + 1), file_debug)
					wdebug("     Ligne dessous\n", file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessous[j][i][0].x,
																											liste_points_dessous[j][i][0].y,
																											liste_points_dessous[j][i][0].z,
																											liste_points_dessous[j][i][1].x,
																											liste_points_dessous[j][i][1].y,
																											liste_points_dessous[j][i][1].z),
																											file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessous[j][i][2].x,
																											liste_points_dessous[j][i][2].y,
																											liste_points_dessous[j][i][2].z,
																											liste_points_dessous[j][i][3].x,
																											liste_points_dessous[j][i][3].y,
																											liste_points_dessous[j][i][3].z),
																											file_debug)
					wdebug("     Ligne dessus\n", file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessus[j][i][0].x,
																											liste_points_dessus[j][i][0].y,
																											liste_points_dessus[j][i][0].z,
																											liste_points_dessus[j][i][1].x,
																											liste_points_dessus[j][i][1].y,
																											liste_points_dessus[j][i][1].z),
																											file_debug)
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessus[j][i][1].x,
																											liste_points_dessus[j][i][1].y,
																											liste_points_dessus[j][i][1].z,
																											liste_points_dessus[j][i][2].x,
																											liste_points_dessus[j][i][2].y,
																											liste_points_dessus[j][i][2].z),
																											file_debug)
					if semi_debug:
						wdebug("     Ligne de construction\n", file_debug)
						wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_construction[j][i][0].x,
																												liste_points_construction[j][i][0].y,
																												liste_points_construction[j][i][0].z,
																												liste_points_construction[j][i][1].x,
																												liste_points_construction[j][i][1].y,
																												liste_points_construction[j][i][1].z),
																												file_debug)
						wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_construction[j][i][1].x,
																												liste_points_construction[j][i][1].y,
																												liste_points_construction[j][i][1].z,
																												liste_points_construction[j][i][2].x,
																												liste_points_construction[j][i][2].y,
																												liste_points_construction[j][i][2].z),
																												file_debug)

			if j == 0:	# Première ligne
				if i == 0:	# Première colonne
					sketch.addGeometry(Part.LineSegment(point_delimitation[0], liste_points_dessous[j][i][0]), False)
				elif i == nb_losange_x - 1:	# Dernière colonne
					sketch.addGeometry(Part.LineSegment(point_delimitation[1], liste_points_dessous[j][i][2]), False)
				if i > 0:	# Colonnes intermédiaires
					sketch.addGeometry(Part.LineSegment(liste_points_dessous[j][i - 1][2], liste_points_dessous[j][i][0]), False)
			
			elif j == nb_losange_y * 2 - 1:	# Dernière ligne
				if i == 0:	# Première colonne
					sketch.addGeometry(Part.LineSegment(point_delimitation[3], liste_points_dessus[j][i][0]), False)
				elif i == nb_losange_x - 1:	# Dernière colonne
					sketch.addGeometry(Part.LineSegment(point_delimitation[2], liste_points_dessus[j][i][2]), False)
				if i > 0:	# Colonnes intermédiaires
					sketch.addGeometry(Part.LineSegment(liste_points_dessus[j][i - 1][2], liste_points_dessus[j][i][0]), False)
			
			if i == 0 and j == 0:	# Première colonne & Première ligne
				sketch.addGeometry(Part.LineSegment(point_delimitation[0], liste_points_dessus[j][i][0]), False)
			elif i == nb_losange_x - 1 and j == 0:	# Dernière colonne & Première ligne
				sketch.addGeometry(Part.LineSegment(point_delimitation[1], liste_points_dessus[j][i][3]), False)
			elif i == 0 and j == nb_losange_y * 2 - 1:	# Première colonne & Dernière ligne
				sketch.addGeometry(Part.LineSegment(point_delimitation[3], liste_points_dessous[j][i][1]), False)
			elif i == nb_losange_x - 1 and j == nb_losange_y * 2 - 1:	# Première colonne & Dernière ligne
				sketch.addGeometry(Part.LineSegment(point_delimitation[2], liste_points_dessous[j][i][3]), False)
			
			if j % 2 == 0 and j != 0 and j != nb_losange_y * 2 - 1:	# Lignes intermédiaires
				if i == 0:	# Première colonne
					sketch.addGeometry(Part.LineSegment(liste_points_dessous[j - 1][i][1], liste_points_dessus[j][i][0]), False)
				elif i == nb_losange_x - 1:	# Dernière colonne
					sketch.addGeometry(Part.LineSegment(liste_points_dessous[j - 1][i][3], liste_points_dessus[j][i][3]), False)

	# Extrusion de l'esquisse & Génération des plateaux
	if extrude:
		pad_losange = doc.getObject(nom_body_losange).newObject('PartDesign::Pad', nom_pad_losange)	# Créer un Pad
		pad_losange.Profile = sketch																# Mettre l'esquisse dans le pad
		pad_losange.Length = dimlat_ep																# Définir la longueur d'extrustion
		pad_losange.ReferenceAxis = (sketch, ['N_Axis'])											# Définir la direction d'extrusion
		doc.recompute()																				# Lancer les calculs
		sketch.Visibility = sketch_visible															# Affichage de l'esquisse après l'extrusion
		if file_debug != None and debug:
			wdebug("Extrusion de la structure\n", file_debug)

		if generation_plateaux_extremitees:
			# Génération des plateaux liants les extrémités
			if file_debug != None and debug:
				wdebug("Création des plateaux liants les extrémités de la structure.\n", file_debug)

			gen_plateaux(	nb_couches=1,
							ep_plateaux=ep_plateaux,
							dimlat_x=dimlat_x,
							dimlat_par_couche=[dimlat_y],
							dimlat_ep=dimlat_ep,
							sketch_visible=sketch_visible,
							nom_body_losange=nom_body_losange,
							doc=doc,
							nom_sketch_plateaux=nom_sketch_plateaux_extremitees,
							nom_pad_plateaux=nom_pad_plateau_extremitees,
							debug=debug,
							file_debug=file_debug,
							wdebug=wdebug)