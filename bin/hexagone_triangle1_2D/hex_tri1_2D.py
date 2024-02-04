"""
Génération de la structure Hexagones + Triangles 1 2D
Sur base du code de Valentin BACOUT
Implémentation par Adrien HERMAN
06/12/2023
"""

def gen_hex_tri1_2D_aligne(	ep=0.4,
							doc=None,
							file_debug=None,
							nb_hex_x=4,
							nb_hex_y=4,
							alpha=1.0472,
							dimlat_x=40,
							dimlat_y=40,
							dimlat_ep=40,
							ep_plateaux=[1,1],
							semi_debug=False,
							debug=False,
							sketch_visible=False,
							extrude=True,
							nom_sketch_hex_tri="Sketch_Hex_Tri1_2D_Alignes",
							nom_sketch_plateaux_extremitees=["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							nom_body_hex_tri="Body_Hex_Tri1_2D_Alignes",
							nom_pad_hex_tri="Pad_Hex_Tri1_2D_Alignes",
							nom_pad_plateau_extremitees=["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							gen_plateaux=None,
							generation_plateaux_extremitees=True,
							wdebug=None,
							sketch=""):
	"""
	Génération de la structure de base.

	-----------
	Variables :
		- ep -> Épaisseur des parois de la structure lattice
		- doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		- file_debug -> Fichier de déboggage (ouvert)
		- nb_hex_x / nb_hex_y -> Nombre d'hexagones sur la distance x / y
		- alpha -> Angle des triangles sur les bords des hexagones
		- dimlat_x / dimlat_y -> Dimensions de la zone de construction
		- dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		- ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
					   [Épaisseur du plateau du dessous, Épaisseur du plateau du dessus]
		- semi_debug -> Tracer les lignes de construction
		- debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		- sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		- extrude -> Réaliser l'extrusion = True
		- nom_sketch_hex_tri -> Nom de l'esquisse du motif hexagone + triangle
		- nom_sketch_plateaux_extremitees -> Nom des esquisses de définition des plateaux
		- nom_body_hex_tri -> Nom de la pièce
		- nom_pad_hex_tri -> Nom du pad du motif hexagone + triangle
		- nom_pad_plateau -> Nom des pad des plateaux liant les parties hautes et basses de la structure
		- gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		- generation_plateaux_extremitees -> True = Les plateaux aux extrémités sont générés, False = Génération des plateaux ignorés
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		- sketch -> Objet contenant l'esquisse de la structure losange
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher, math

	if doc == None:	doc = FreeCAD.newDocument()

	if file_debug != None and debug: wdebug("""dimlat_x:{0}
												\ndimlat_y:{1}
												\ndimlat_ep:{2}
												\nnb_hex_x:{3}
												\nnb_hex_y:{4}
												\nnom_sketch_hex_tri:{5}
												\nalpha:{6}
												\n----\n""".format(	dimlat_x,
																	dimlat_y,
																	dimlat_ep,
																	nb_hex_x,
																	nb_hex_y,
																	nom_sketch_hex_tri,
																	alpha),
																	file_debug)

	"""
	-------------------------------
	--- Variables de l'objet 3D ---
	-------------------------------
	Note : Toutes les dimensions sont exprimées en mm et réfèrent au schéma
	"""
	# Dimensions caractéristiques du losange calculées (voir schéma)
	beta = math.pi/2-alpha
	lx = dimlat_x/nb_hex_x
	ly = dimlat_y/nb_hex_y
	cote = (ly/2)/math.sin(alpha)
	cote_ep = (ly/2-ep/2)/math.sin(alpha)
	
	if file_debug != None and debug: wdebug("""ep:{0}
												\nlx:{1}
												\nly:{2}
												\ncote:{3}
												\ncote_ep:{4}
												\nbeta:{5}
												\n----\n""".format(	ep,
																	lx,
																	ly,
																	cote,
																	cote_ep,
																	beta),
																	file_debug)

	# Condition à respecter pour pouvoir générer le motif
	if math.cos(alpha) * cote >= lx / 2:
		wdebug("gen_hex_tri1_2D_aligne : Il y a trop de motifs en x !\n     nb_hex_x={0}\n".format(nb_hex_x), file_debug)
		return

	# Création d'une nouvelle esquisse et de la pièce
	if sketch == "":
		if file_debug != None and debug:
			wdebug("Création de l'esquisse du losange : {0}\n".format(nom_sketch_hex_tri), file_debug)
			wdebug("Création du body du losange : {0}\n".format(nom_body_hex_tri), file_debug)

		sketch = doc.addObject("Sketcher::SketchObject", nom_sketch_hex_tri)
		body = doc.addObject('PartDesign::Body', nom_body_hex_tri)

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
	for j in range(nb_hex_y):
		for i in range(nb_hex_x):
			current_pos = (lx * i, ly * j, 0)

			"""
			Construction de la géométrie 1
				Coordonées des points :
					1 -> (0,ep/2,0)
					2 -> (math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)),ep/2,0)
					3 -> (math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)),ep/2,0)
					4 -> (lx/2,ep/2,0)
					5 -> (0,ly/2-ep/(2*math.sin(alpha))*math.tan(alpha),0)
					6 -> (ep/(2*math.sin(alpha)),ly/2,0)
					7 -> (math.cos(alpha)*cote,0,0)
					8 -> (0,ly/2,0)
			"""

			# Création du contour 1
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector(lx/2+current_pos[0],0+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(lx/2+current_pos[0],0+current_pos[1],0), App.Vector(lx/2+current_pos[0],ly/2+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(lx/2+current_pos[0],ly/2+current_pos[1],0), App.Vector(0+current_pos[0],ly/2+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly/2+current_pos[1],0), App.Vector(0+current_pos[0],0+current_pos[1],0)),True)

			# Creation de l'ame 8-7                                       
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly/2+current_pos[1],0), App.Vector(math.cos(alpha)*cote+current_pos[0],0+current_pos[1],0)),True)

			# ligne 1-2
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ep/2+current_pos[1],0), App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0)),False)

			# ligne 2-5
			sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(0+current_pos[0],ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

			# ligne 3-6
			sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(ep/(2*math.sin(alpha))+current_pos[0],ly/2+current_pos[1],0)),False)

			# ligne 3-4
			sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ep/2+current_pos[1],0)),False)
																  
			"""
			Construction de la géométrie 2
				Coordonées des points :
					1 -> (lx,ep/2,0)
					2 -> (lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))),ep/2,0)
					3 -> (lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))),ep/2,0)
					4 -> (lx/2,ep/2,0)
					5 -> (lx,ly/2-ep/(2*math.sin(alpha))*math.tan(alpha),0)
					6 -> (lx-(ep/(2*math.sin(alpha))),ly/2,0)
					7 -> (lx-(math.cos(alpha)*cote),0,0)
					8 -> (lx,ly/2,0)
			"""


			#Création du contour 2
			sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],0+current_pos[1],0)),True)

			# Creation de l'ame 8-7                                       
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx-(math.cos(alpha)*cote)+current_pos[0],0+current_pos[1],0)),True)

			# ligne 1-2
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ep/2)+current_pos[1],0), App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0)),False)

			# ligne 2-5
			sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector(lx+current_pos[0],(ly/2)-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

			# ligne 3-6
			sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector(lx-(ep/(2*math.sin(alpha)))+current_pos[0],(ly/2)+current_pos[1],0)),False)

			# ligne 3-4
			sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ep/2)+current_pos[1],0)),False)

			"""
			Construction de la géométrie 3
				Coordonées des points :
					1 -> (lx,ly-(ep/2),0)
					2 -> (lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))),ly-(ep/2),0)
					3 -> (lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))),ly-(ep/2),0)
					4 -> (lx/2,ly-(ep/2),0)
					5 -> (lx,ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)),0)
					6 -> (lx-(ep/(2*math.sin(alpha))),ly/2,0)
					7 -> (lx-(math.cos(alpha)*cote),ly,0)
					8 -> (lx,ly/2,0)
			"""

			#Création du contour 3
			sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)

			# Creation de l'ame 8-7                                       
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly/2+current_pos[1],0), App.Vector(lx-(math.cos(alpha)*cote)+current_pos[0],ly+current_pos[1],0)),True)

			# ligne 1-2
			sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

			# ligne 2-5
			sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly-((ly/2)-ep/(2*math.sin(alpha))*math.tan(alpha))+current_pos[1],0)),False)

			# ligne 3-6
			sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(lx-(ep/(2*math.sin(alpha)))+current_pos[0],(ly/2)+current_pos[1],0)),False)

			# ligne 3-4
			sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

			"""
			Construction de la géométrie 4
				Coordonées des points :
					1 ->(0,ly-(ep/2),0)
					2 ->(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)),ly-(ep/2),0)
					3 ->(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)),ly-(ep/2),0)
					4 ->(lx/2,ly-(ep/2),0)
					5 ->(0,ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)),0)
					6 ->(ep/(2*math.sin(alpha)),ly/2,0)
					7 ->(math.cos(alpha)*cote,ly,0)
					8 ->(0,ly/2,0)
			"""

			#Création du contour 4
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),True)
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0)),True)

			# Creation de l'ame 8-7                                       
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(math.cos(alpha)*cote+current_pos[0],ly+current_pos[1],0)),True)

			# ligne 1-2
			sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

			# ligne 2-5
			sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha))+current_pos[1],0)),False)

			# ligne 3-6
			sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(ep/(2*math.sin(alpha))+current_pos[0],(ly/2)+current_pos[1],0)),False)

			# ligne 3-4
			sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

			if i == 0 :
				# Fermeture des bords à gauche
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector(0+current_pos[0],(ep/2)+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly-ep/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),False)

				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly/2+ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

			if i == nb_hex_x-1:
				# Fermeture des bords à droite
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],(ep/2)+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly-ep/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),False)

				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly/2+ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

	# Fermeture des bords haut et bas
	sketch.addGeometry(Part.LineSegment( App.Vector(0,0,0), App.Vector(dimlat_x,0,0)),False)
	sketch.addGeometry(Part.LineSegment( App.Vector(0,dimlat_y,0), App.Vector(dimlat_x,dimlat_y,0)),False)

	# Extrusion de l'esquisse & Génération des plateaux
	if extrude:
		pad_hex_tri = body.newObject('PartDesign::Pad', nom_pad_hex_tri)	# Créer un Pad
		pad_hex_tri.Profile = sketch																# Mettre l'esquisse dans le pad
		pad_hex_tri.Length = dimlat_ep																# Définir la longueur d'extrustion
		pad_hex_tri.ReferenceAxis = (sketch, ['N_Axis'])											# Définir la direction d'extrusion
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
							nom_body=nom_body_hex_tri,
							doc=doc,
							nom_sketch_plateaux=nom_sketch_plateaux_extremitees,
							nom_pad_plateaux=nom_pad_plateau_extremitees,
							debug=debug,
							file_debug=file_debug,
							wdebug=wdebug)

def gen_hex_tri1_2D_naligne(	ep=0.4,
							doc=None,
							file_debug=None,
							nb_hex_x=4,
							nb_hex_y=4,
							alpha=1.0472,
							dimlat_x=40,
							dimlat_y=40,
							dimlat_ep=40,
							ep_plateaux=[1,1],
							semi_debug=False,
							debug=False,
							sketch_visible=False,
							extrude=True,
							nom_sketch_hex_tri="Sketch_Hex_Tri1_2D_Alignes",
							nom_sketch_plateaux_extremitees=["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							nom_body_hex_tri="Body_Hex_Tri1_2D_Alignes",
							nom_pad_hex_tri="Pad_Hex_Tri1_2D_Alignes",
							nom_pad_plateau_extremitees=["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							gen_plateaux=None,
							generation_plateaux_extremitees=True,
							wdebug=None,
							sketch=""):
	"""
	Génération de la structure de base.

	-----------
	Variables :
		- ep -> Épaisseur des parois de la structure lattice
		- doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		- file_debug -> Fichier de déboggage (ouvert)
		- nb_hex_x / nb_hex_y -> Nombre d'hexagones sur la distance x / y
		- alpha -> Angle des triangles sur les bords des hexagones
		- dimlat_x / dimlat_y -> Dimensions de la zone de construction
		- dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		- ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
					   [Épaisseur du plateau du dessous, Épaisseur du plateau du dessus]
		- semi_debug -> Tracer les lignes de construction
		- debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		- sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		- extrude -> Réaliser l'extrusion = True
		- nom_sketch_hex_tri -> Nom de l'esquisse du motif hexagone + triangle
		- nom_sketch_plateaux_extremitees -> Nom des esquisses de définition des plateaux
		- nom_body_hex_tri -> Nom de la pièce
		- nom_pad_hex_tri -> Nom du pad du motif hexagone + triangle
		- nom_pad_plateau -> Nom des pad des plateaux liant les parties hautes et basses de la structure
		- gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		- generation_plateaux_extremitees -> True = Les plateaux aux extrémités sont générés, False = Génération des plateaux ignorés
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		- sketch -> Objet contenant l'esquisse de la structure losange
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher, math

	if doc == None:	doc = FreeCAD.newDocument()

	if file_debug != None and debug: wdebug("""dimlat_x:{0}
												\ndimlat_y:{1}
												\ndimlat_ep:{2}
												\nnb_hex_x:{3}
												\nnb_hex_y:{4}
												\nnom_sketch_hex_tri:{5}
												\nalpha:{6}
												\n----\n""".format(	dimlat_x,
																	dimlat_y,
																	dimlat_ep,
																	nb_hex_x,
																	nb_hex_y,
																	nom_sketch_hex_tri,
																	alpha),
																	file_debug)

	# Dimensions caractéristiques du losange calculées (voir schéma)
	beta = math.pi/2-alpha
	lx = dimlat_x/nb_hex_x
	ly = dimlat_y/nb_hex_y
	cote = (ly/2)/math.sin(alpha)
	cote_ep = (ly/2-ep/2)/math.sin(alpha)
	
	if file_debug != None and debug: wdebug("""ep:{0}
												\nlx:{1}
												\nly:{2}
												\ncote:{3}
												\ncote_ep:{4}
												\nbeta:{5}
												\n----\n""".format(	ep,
																	lx,
																	ly,
																	cote,
																	cote_ep,
																	beta),
																	file_debug)

	if math.cos(alpha) * cote >= lx / 2:
		wdebug("gen_hex_tri1_2D_aligne : Il y a trop de motifs en x !\n     nb_hex_x={0}\n".format(nb_hex_x), file_debug)
		return

	# Création d'une nouvelle esquisse et de la pièce
	if sketch == "":
		if file_debug != None and debug:
			wdebug("Création de l'esquisse du losange : {0}\n".format(nom_sketch_hex_tri), file_debug)
			wdebug("Création du body du losange : {0}\n".format(nom_body_hex_tri), file_debug)

		sketch = doc.addObject("Sketcher::SketchObject", nom_sketch_hex_tri)
		body = doc.addObject('PartDesign::Body', nom_body_hex_tri)

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
	for j in range(nb_hex_y):
		for i in range(nb_hex_x):
			current_pos = (lx * i, ly * j, 0)

			if j % 2 == 0:
				# Construction de la géométrie 1

				# Coordonées des points
				# 1 (0,ep/2,0)
				# 2 (math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)),ep/2,0)
				# 3 (math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)),ep/2,0)
				# 4 (lx/2,ep/2,0)
				# 5 (0,ly/2-ep/(2*math.sin(alpha))*math.tan(alpha),0)
				# 6 (ep/(2*math.sin(alpha)),ly/2,0)
				# 7 (math.cos(alpha)*cote,0,0)
				# 8 (0,ly/2,0)


				#Création du contour 1
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector(lx/2+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx/2+current_pos[0],0+current_pos[1],0), App.Vector(lx/2+current_pos[0],ly/2+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx/2+current_pos[0],ly/2+current_pos[1],0), App.Vector(0+current_pos[0],ly/2+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly/2+current_pos[1],0), App.Vector(0+current_pos[0],0+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly/2+current_pos[1],0), App.Vector(math.cos(alpha)*cote+current_pos[0],0+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ep/2+current_pos[1],0), App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(0+current_pos[0],ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(ep/(2*math.sin(alpha))+current_pos[0],ly/2+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ep/2+current_pos[1],0)),False)
																	  

				# Construction de la géométrie 2

				# coordonées des points
				# 1 (lx,ep/2,0)
				# 2 (lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))),ep/2,0)
				# 3 (lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))),ep/2,0)
				# 4 (lx/2,ep/2,0)
				# 5 (lx,ly/2-ep/(2*math.sin(alpha))*math.tan(alpha),0)
				# 6 (lx-(ep/(2*math.sin(alpha))),ly/2,0)
				# 7 (lx-(math.cos(alpha)*cote),0,0)
				# 8 (lx,ly/2,0)


				#Création du contour 2
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],0+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx-(math.cos(alpha)*cote)+current_pos[0],0+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ep/2)+current_pos[1],0), App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector(lx+current_pos[0],(ly/2)-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector(lx-(ep/(2*math.sin(alpha)))+current_pos[0],(ly/2)+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ep/2)+current_pos[1],0)),False)


				# Construction de la géométrie 3

				# coordonées des points
				# 1 (lx,ly-(ep/2),0)
				# 2 (lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))),ly-(ep/2),0)
				# 3 (lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))),ly-(ep/2),0)
				# 4 (lx/2,ly-(ep/2),0)
				# 5 (lx,ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)),0)
				# 6 (lx-(ep/(2*math.sin(alpha))),ly/2,0)
				# 7 (lx-(math.cos(alpha)*cote),ly,0)
				# 8 (lx,ly/2,0)


				#Création du contour 3
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly/2+current_pos[1],0), App.Vector(lx-(math.cos(alpha)*cote)+current_pos[0],ly+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly-((ly/2)-ep/(2*math.sin(alpha))*math.tan(alpha))+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(lx-(ep/(2*math.sin(alpha)))+current_pos[0],(ly/2)+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)


				# Construction de la géométrie 4

				# coordonées des points
				# 1 (0,ly-(ep/2),0)
				# 2 (math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)),ly-(ep/2),0)
				# 3 (math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)),ly-(ep/2),0)
				# 4 (lx/2,ly-(ep/2),0)
				# 5 (0,ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)),0)
				# 6 (ep/(2*math.sin(alpha)),ly/2,0)
				# 7 (math.cos(alpha)*cote,ly,0)
				# 8 (0,ly/2,0)


				#Création du contour 4
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(math.cos(alpha)*cote+current_pos[0],ly+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha))+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(ep/(2*math.sin(alpha))+current_pos[0],(ly/2)+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

			else:

				# Construction de la géométrie 1

				# coordonées des points
				# 1 (0,ep/2,0)
				# 2 (math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)),ep/2,0)
				# 3 (math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)),ep/2,0)
				# 4 (lx/2,ep/2,0)
				# 5 (0,ly/2-ep/(2*math.sin(alpha))*math.tan(alpha),0)
				# 6 (ep/(2*math.sin(alpha)),ly/2,0)
				# 7 (math.cos(alpha)*cote,0,0)
				# 8 (0,ly/2,0)


				#Création du contour 1
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],ly/2+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly/2+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly/2+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly/2+current_pos[1],0), App.Vector((lx/2)+current_pos[0],0+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly/2+current_pos[1],0), App.Vector(math.cos(alpha)*cote+(lx/2)+current_pos[0],0+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ep/2+current_pos[1],0), App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ep/2+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ep/2+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ep/2+current_pos[1],0), App.Vector(ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ly/2+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ep/2+current_pos[1],0), App.Vector(lx+current_pos[0],ep/2+current_pos[1],0)),False)

				# Construction de la géométrie 2

				# coordonées des points
				# 1 (lx,ep/2,0)
				# 2 (lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))),ep/2,0)
				# 3 (lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))),ep/2,0)
				# 4 (lx/2,ep/2,0)
				# 5 (lx,ly/2-ep/(2*math.sin(alpha))*math.tan(alpha),0)
				# 6 (lx-(ep/(2*math.sin(alpha))),ly/2,0)
				# 7 (lx-(math.cos(alpha)*cote),0,0)
				# 8 (lx,ly/2,0)


				#Création du contour 2
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector((lx/2)+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],0+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(0+current_pos[0],0+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)-(math.cos(alpha)*cote)+current_pos[0],0+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ep/2)+current_pos[1],0), App.Vector((lx/2)-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector((lx/2)-(ep/(2*math.sin(alpha)))+current_pos[0],(ly/2)+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],(ep/2)+current_pos[1],0), App.Vector(0+current_pos[0],(ep/2)+current_pos[1],0)),False)

				# Construction de la géométrie 3

				# coordonées des points
				# 1 (lx,ly-(ep/2),0)
				# 2 (lx-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))),ly-(ep/2),0)
				# 3 (lx-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))),ly-(ep/2),0)
				# 4 (lx/2,ly-(ep/2),0)
				# 5 (lx,ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)),0)
				# 6 (lx-(ep/(2*math.sin(alpha))),ly/2,0)
				# 7 (lx-(math.cos(alpha)*cote),ly,0)
				# 8 (lx,ly/2,0)


				#Création du contour 3
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly/2+current_pos[1],0), App.Vector((lx/2)-(math.cos(alpha)*cote)+current_pos[0],ly+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)-(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly-((ly/2)-ep/(2*math.sin(alpha))*math.tan(alpha))+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)-(ep/(2*math.sin(alpha)))+current_pos[0],(ly/2)+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)-(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)))+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

				# Construction de la géométrie 4

				# coordonées des points
				# 1 (0,ly-(ep/2),0)
				# 2 (math.sin(beta)*cote_ep-ep/(2*math.sin(alpha)),ly-(ep/2),0)
				# 3 (math.sin(beta)*cote_ep+ep/(2*math.sin(alpha)),ly-(ep/2),0)
				# 4 (lx/2,ly-(ep/2),0)
				# 5 (0,ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)),0)
				# 6 (ep/(2*math.sin(alpha)),ly/2,0)
				# 7 (math.cos(alpha)*cote,ly,0)
				# 8 (0,ly/2,0)


				#Création du contour 4
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly+current_pos[1],0), App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),True)

				# Creation de l'ame 8-7                                       
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(math.cos(alpha)*cote+(lx/2)+current_pos[0],ly+current_pos[1],0)),True)

				# ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector((lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

				# ligne 2-5
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep-ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector((lx/2)+current_pos[0],ly-(ly/2-ep/(2*math.sin(alpha))*math.tan(alpha))+current_pos[1],0)),False)

				# ligne 3-6
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],(ly/2)+current_pos[1],0)),False)

				# ligne 3-4
				sketch.addGeometry(Part.LineSegment( App.Vector(math.sin(beta)*cote_ep+ep/(2*math.sin(alpha))+(lx/2)+current_pos[0],ly-(ep/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly-(ep/2)+current_pos[1],0)),False)

			if i == 0 :

				#fermeture des bords
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector(0+current_pos[0],(ep/2)+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly-ep/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),False)

				if j % 2 ==0:
					sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)
					sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(0+current_pos[0],ly/2+ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

			if i == nb_hex_x-1:

				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],(ep/2)+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly-ep/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),False)

				if j % 2 == 0:
					sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly/2-ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)
					sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],(ly/2)+current_pos[1],0), App.Vector(lx+current_pos[0],ly/2+ep/(2*math.sin(alpha))*math.tan(alpha)+current_pos[1],0)),False)

	# Fermeture des bords haut et bas
	sketch.addGeometry(Part.LineSegment( App.Vector(0,0,0), App.Vector(dimlat_x,0,0)),False)
	sketch.addGeometry(Part.LineSegment( App.Vector(0,dimlat_y,0), App.Vector(dimlat_x,dimlat_y,0)),False)

	# Extrusion de l'esquisse & Génération des plateaux
	if extrude:
		pad_hex_tri = body.newObject('PartDesign::Pad', nom_pad_hex_tri)	# Créer un Pad
		pad_hex_tri.Profile = sketch																# Mettre l'esquisse dans le pad
		pad_hex_tri.Length = dimlat_ep																# Définir la longueur d'extrustion
		pad_hex_tri.ReferenceAxis = (sketch, ['N_Axis'])											# Définir la direction d'extrusion
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
							nom_body=nom_body_hex_tri,
							doc=doc,
							nom_sketch_plateaux=nom_sketch_plateaux_extremitees,
							nom_pad_plateaux=nom_pad_plateau_extremitees,
							debug=debug,
							file_debug=file_debug,
							wdebug=wdebug)