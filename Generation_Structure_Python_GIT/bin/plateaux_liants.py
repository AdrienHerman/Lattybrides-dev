"""
Génération des plateaux de liens de la structure (en haut et en bas)
HERMAN Adrien
04/10/2023
"""

def gen_plateaux2(	nb_couches=3,
					ep_plateaux=[1,0.5,0.5,1],
					dimlat_x=40,
					dimlat_par_couche=[13.3,17.7,8.8],
					dimlat_ep=40,
					sketch_visible=False,
					nom_body_losange="Body_Losange",
					doc=None,
					nom_sketch_plateaux=["Sketch_Plateaux1","Sketch_Plateaux2","Sketch_Plateaux3","Sketch_Plateaux4"],
					nom_pad_plateaux=["Pad_Plateaux1","Pad_Plateaux2","Pad_Plateaux3","Pad_Plateaux4"],
					debug=True,
					file_debug=None):
	"""
	Génération des plateaux liants les strcutures sur le haut et le bas

	-----------
	Variables :
	-----------
		ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
		dimlat_x / dimlat_par_couche -> Dimensions de la zone de construction
		dimlat_ep -> Épaisseur de l'extrusion du modèle
		sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		nom_body_losange -> Nom de la pièce
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		nom_sketch_plateaux -> Nom de l'esquisse des plateaux
		nom_pad_plateau -> Num du pad des plateaux liant les parties hautes et basses de la structure
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
					debug_current_folder -> Générer le fichier de déboggage dans
				le dossier "debug" du répertoire courrant si True, sinon
				Générer le fichier de déboggae dans le dossier indiqué dans la variable
		file_debug -> Fichier de déboggage (ouvert)
	"""

	# Importation des modules python
	import FreeCAD as App
	import Part, Sketcher, sys

	# Importation des modules du logiciel
	sys.path.append("/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/")
	#sys.path.append("C:\Users\herma\Documents\Shadow Drive\INSA 5A\PLP\Generation Structures Python")
	from debug import wdebug

	dimlat_par_couche.insert(0, 0)

	if doc != None:
		# Construction des lignes des plateaux
		current_posy = 0
		for couchei in range(len(dimlat_par_couche)):
			# Vérification que la couche doit être créée
			if ep_plateaux[couchei] == 0:
				try:
					current_posy += dimlat_par_couche[couchei + 1]
				except:
					pass
					
				continue

			# Création de l'essquisse
			sketch_plateaux = doc.addObject("Sketcher::SketchObject", nom_sketch_plateaux[couchei])
			if file_debug != None and debug:
				wdebug("Création de l'esquisse des plateaux : {0}\n".format(nom_sketch_plateaux[couchei]), file_debug)

			# Création de la liste des points des plateaux
			liste_points = [	App.Vector(0, current_posy + ep_plateaux[couchei] / 2, 0),
								App.Vector(dimlat_x, current_posy + ep_plateaux[couchei] / 2, 0),
								App.Vector(dimlat_x, current_posy - ep_plateaux[couchei] / 2, 0),
								App.Vector(0, current_posy - ep_plateaux[couchei] / 2, 0)]

			for i in range(1, 5):
				sketch_plateaux.addGeometry(Part.LineSegment(liste_points[(i - 1) % 4], liste_points[i % 4]), False)
				if file_debug != None and debug:
					wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points[(i - 1) % 4].x,
																											liste_points[(i - 1) % 4].y,
																											liste_points[(i - 1) % 4].z,
																											liste_points[i % 4].x,
																											liste_points[i % 4].y,
																											liste_points[i % 4].z),
																											file_debug)

			doc.getObject(nom_body_losange).newObject('PartDesign::Pad', nom_pad_plateaux[couchei])	# Créer un Pad
			doc.getObject(nom_pad_plateaux[couchei]).Profile = sketch_plateaux						# Mettre l'esquisse dans le pad
			doc.getObject(nom_pad_plateaux[couchei]).Length = dimlat_ep								# Définir la longueur d'extrustion
			doc.getObject(nom_pad_plateaux[couchei]).ReferenceAxis = (sketch_plateaux, ['N_Axis'])	# Définir la direction d'extrusion
			doc.recompute()																			# Lancer les calculs
			sketch_plateaux.Visibility = sketch_visible												# Affichage de l'esquisse après l'extrusion

			try:
				current_posy += dimlat_par_couche[couchei + 1]
			except:
				pass

		del dimlat_par_couche[0]

		if file_debug != None and debug:
			wdebug("Extrusion des plateaux\n", file_debug)

def gen_plateaux(	ep_plateaux=1,
					dimlat_x=20,
					dimlat_y=20,
					dimlat_ep=20,
					sketch_visible=False,
					nom_body_losange="Body_Losange",
					doc=None,
					nom_sketch_plateaux="Sketch_Plateaux",
					nom_pad_plateaux="Pad_Plateaux",
					debug=True,
					file_debug=None):
	"""
	Génération des plateaux liants les strcutures sur le haut et le bas

	-----------
	Variables :
	-----------
		ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
		dimlat_x / dimlat_y -> Dimensions de la zone de construction
		dimlat_ep -> Épaisseur de l'extrusion du modèle
		sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		nom_body_losange -> Nom de la pièce
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		nom_sketch_plateaux -> Nom de l'esquisse des plateaux
		nom_pad_plateau -> Num du pad des plateaux liant les parties hautes et basses de la structure
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
					debug_current_folder -> Générer le fichier de déboggage dans
				le dossier "debug" du répertoire courrant si True, sinon
				Générer le fichier de déboggae dans le dossier indiqué dans la variable
		file_debug -> Fichier de déboggage (ouvert)
	"""

	# Importation des modules python
	import FreeCAD as App
	import Part, Sketcher, sys

	# Importation des modules du logiciel
	sys.path.append("/home/adrien/Documents/Shadow Drive/INSA 5A/PLP/Generation Structures Python/")
	#sys.path.append("C:\Users\herma\Documents\Shadow Drive\INSA 5A\PLP\Generation Structures Python")
	from debug import wdebug

	if doc != None:
		# Création de l'essquisse
		sketch_plateaux = doc.addObject("Sketcher::SketchObject", nom_sketch_plateaux)
		if file_debug != None and debug:
			wdebug("Création de l'esquisse des plateaux : {0}\n".format(nom_sketch_plateaux), file_debug)

		# Création de la liste des points des plateaux
		liste_points_dessous = [	App.Vector(0, 0, 0),
									App.Vector(dimlat_x, 0, 0),
									App.Vector(dimlat_x, -ep_plateaux, 0),
									App.Vector(0, -ep_plateaux, 0)]
		liste_points_dessus = [		App.Vector(0, dimlat_y, 0),
									App.Vector(dimlat_x, dimlat_y, 0),
									App.Vector(dimlat_x, dimlat_y + ep_plateaux, 0),
									App.Vector(0, dimlat_y + ep_plateaux, 0)]

		# Construction des lignes des plateaux
		#	Plateau du dessous
		if file_debug != None and debug:
			wdebug("\n\n---\nConstruction du plateau du dessus\n", file_debug)
		for i in range(1, 5):
			sketch_plateaux.addGeometry(Part.LineSegment(liste_points_dessous[(i - 1) % 4], liste_points_dessous[i % 4]), False)
			if file_debug != None and debug:
				wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessous[(i - 1) % 4].x,
																										liste_points_dessous[(i - 1) % 4].y,
																										liste_points_dessous[(i - 1) % 4].z,
																										liste_points_dessous[i % 4].x,
																										liste_points_dessous[i % 4].y,
																										liste_points_dessous[i % 4].z),
																										file_debug)

		# 	Plateau du dessus
		if file_debug != None and debug:
			wdebug("\n\n---\nConstruction du plateau du dessous\n", file_debug)
		for i in range(1, 5):
			sketch_plateaux.addGeometry(Part.LineSegment(liste_points_dessus[(i - 1) % 4], liste_points_dessus[i % 4]), False)
			if file_debug != None and debug:
				wdebug("Construction de la ligne entre ({0}, {1}, {2}) et ({3}, {4}, {5})\n".format(	liste_points_dessus[(i - 1) % 4].x,
																										liste_points_dessus[(i - 1) % 4].y,
																										liste_points_dessus[(i - 1) % 4].z,
																										liste_points_dessus[i % 4].x,
																										liste_points_dessus[i % 4].y,
																										liste_points_dessus[i % 4].z),
																										file_debug)

		doc.getObject(nom_body_losange).newObject('PartDesign::Pad', nom_pad_plateaux)						# Créer un Pad
		doc.getObject(nom_pad_plateaux).Profile = doc.getObject(nom_sketch_plateaux)						# Mettre l'esquisse dans le pad
		doc.getObject(nom_pad_plateaux).Length = dimlat_ep													# Définir la longueur d'extrustion
		doc.getObject(nom_pad_plateaux).ReferenceAxis = (doc.getObject(nom_sketch_plateaux), ['N_Axis'])	# Définir la direction d'extrusion
		doc.recompute()																						# Lancer les calculs
		doc.getObject(nom_sketch_plateaux).Visibility = sketch_visible										# Affichage de l'esquisse après l'extrusion
		if file_debug != None and debug:
			wdebug("Extrusion des plateaux\n", file_debug)