"""
Génération de la structure Triangles 2D
Sur base du code de Valentin BACOUT
Implémentation par Adrien HERMAN
16/01/2024
"""

def gen_triangle_basic(	ep=0.4,
						doc=None,
						file_debug=None,
						nb_tri_x=4,
						nb_tri_y=4,
						alpha=1.0472,
						dimlat_x=40,
						dimlat_y=40,
						dimlat_ep=40,
						ep_plateaux=[1,1],
						semi_debug=False,
						debug=False,
						sketch_visible=False,
						extrude=True,
						nom_sketch_tri="Sketch_Tri",
						nom_sketch_plateaux_extremitees=["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
						nom_body_tri="Body_Tri",
						nom_pad_tri="Pad_Tri",
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
		- nb_tri_x / nb_tri_y -> Nombre de triangles sur la distance x / y
		- alpha -> Angle des triangles sur les bords des hexagones
		- dimlat_x / dimlat_y -> Dimensions de la zone de construction
		- dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		- ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
					   [Épaisseur du plateau du dessous, Épaisseur du plateau du dessus]
		- semi_debug -> Tracer les lignes de construction
		- debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		- sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		- extrude -> Réaliser l'extrusion = True
		- nom_sketch_tri -> Nom de l'esquisse du motif triangle
		- nom_sketch_plateaux_extremitees -> Nom des esquisses de définition des plateaux
		- nom_body_tri -> Nom de la pièce
		- nom_pad_tri -> Nom du pad du motif triangle
		- nom_pad_plateau -> Nom des pad des plateaux liant les parties hautes et basses de la structure
		- gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		- generation_plateaux_extremitees -> True = Les plateaux aux extrémités sont générés, False = Génération des plateaux ignorés
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		- sketch -> Objet contenant l'esquisse de la structure triangle
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher, math

	if doc == None:	doc = FreeCAD.newDocument()

	if file_debug != None and debug: wdebug("""dimlat_x:{0}
												\ndimlat_y:{1}
												\ndimlat_ep:{2}
												\nnb_tri_x:{3}
												\nnb_tri_y:{4}
												\nnom_sketch_tri:{5}
												\nalpha:{6}
												\n----\n""".format(	dimlat_x,
																	dimlat_y,
																	dimlat_ep,
																	nb_tri_x,
																	nb_tri_y,
																	nom_sketch_tri,
																	alpha),
																	file_debug)

	"""
	-------------------------------
	--- Variables de l'objet 3D ---
	-------------------------------
	Note : Toutes les dimensions sont exprimées en mm et réfèrent au schéma
	"""
	# Dimensions caractéristiques du triangle calculées (voir schéma)
	lx = dimlat_x/nb_tri_x/2
	ly = dimlat_x/nb_tri_y/2
	if file_debug != None and debug: wdebug("""lx:{0}
												\nly:{1}
												\n----\n""".format(	lx,
																	ly),
																	file_debug)

	"""
	Coordonnées des points :
		Point 1 : (0, ep/2,0)
		Point 2 : (((ly-(ep/2)/math.cos(alpha))-(ep/2))/math.tan(alpha),ep/2,0)
		Point 3 : (0, (ly-(ep/2)/math.cos(alpha), 0)
		Point 4 : (lx, (ly-ep)/2-ep/2*math.cos(alpha), 0)
		Point 5 : ((ly-ep)/2-ep/2*math.cos(alpha)/math.tan(alpha),(ly-ep)/2,0)
		Point 6 : (lx, (ly-ep)/2,0)
	"""

	# Création d'une nouvelle esquisse et de la pièce
	if sketch == "":
		if file_debug != None and debug:
			wdebug("Création de l'esquisse du triangle : {0}\n".format(nom_sketch_tri), file_debug)
			wdebug("Création du body du triangle : {0}\n".format(nom_body_tri), file_debug)

		sketch = doc.addObject("Sketcher::SketchObject", nom_sketch_tri)
		body = doc.addObject('PartDesign::Body', nom_body_tri)

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

	# Curseur de position (repère local à chaque triangle)
	current_pos = (0,0,0)

	# i = Numéro de triangle y (ligne)
	# j = Numéro de triangle x (colonne)
	for j in range(nb_tri_y * 4 - 1):
		for i in range(nb_tri_x):
			current_pos = (2*lx * i, ly/2 * j, 0)

			if j % 2 == 0:

				# Création du contour 1
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],0+current_pos[1],0)),True)

				#ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ep/2+current_pos[1],0), App.Vector((ly-ep)/math.tan(alpha)+current_pos[0],(ep/2)+current_pos[1],0)),False)
				#Ligne 2-3
				sketch.addGeometry(Part.LineSegment( App.Vector((ly-ep)/math.tan(alpha)+current_pos[0],ep/2+current_pos[1],0), App.Vector(0+current_pos[0],ly-ep/2+current_pos[1],0)),False)
				#ligne 4-5
				sketch.addGeometry(Part.LineSegment( App.Vector(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				#ligne 5-6
				sketch.addGeometry(Part.LineSegment( App.Vector(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0), App.Vector(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				#ligne 4-6
				sketch.addGeometry(Part.LineSegment( App.Vector(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)


				# Création du contour 2
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(2*lx+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(2*lx+current_pos[0],0+current_pos[1],0), App.Vector(2*lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(2*lx+current_pos[0],ly+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)

				#ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-0+current_pos[0],ep/2+current_pos[1],0), App.Vector((2*lx)-((ly-ep)/math.tan(alpha))+current_pos[0],(ep/2)+current_pos[1],0)),False)
				#Ligne 2-3
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-((ly-ep)/math.tan(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector((2*lx)+current_pos[0],ly-ep/2+current_pos[1],0)),False)
				#ligne 4-5
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha)))+current_pos[0],ep/2+current_pos[1],0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha))+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				#ligne 5-6
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha))+current_pos[0],(ly-ep)/2+current_pos[1],0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha))+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				#ligne 4-6
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha)))+current_pos[0],ep/2+current_pos[1],0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha))+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				if i==0:
					#fermeture des bords
					sketch.addGeometry(Part.LineSegment( App.Vector(current_pos[0],ep/2+current_pos[1],0), App.Vector(current_pos[0],current_pos[1],0)),False)
					sketch.addGeometry(Part.LineSegment( App.Vector(current_pos[0],ly-ep/2+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),False)
				if i==nb_tri_x-1:
					#fermeture des bords
					sketch.addGeometry(Part.LineSegment( App.Vector(2*lx+current_pos[0],ep/2+current_pos[1],0), App.Vector(2*lx+current_pos[0],current_pos[1],0)),False)
					sketch.addGeometry(Part.LineSegment( App.Vector(2*lx+current_pos[0],ly-ep/2+current_pos[1],0), App.Vector(2*lx++current_pos[0],ly+current_pos[1],0)),False)

			else:
				# Création du contour 1
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly+current_pos[1],0), App.Vector(0+current_pos[0],0+current_pos[1],0)),True)

				#ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ep/2+current_pos[1],0), App.Vector(lx+(ly-ep)/math.tan(alpha)+current_pos[0],(ep/2)+current_pos[1],0)),False)
				#Ligne 2-3
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(lx+current_pos[0],ly-ep/2+current_pos[1],0)),False)
				#ligne 4-5
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				#ligne 5-6
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0), App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				#ligne 4-6
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+current_pos[0],ep/2+current_pos[1],0), App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)


				# Création du contour 2
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(2*lx+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(2*lx+current_pos[0],0+current_pos[1],0), App.Vector(2*lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(2*lx+current_pos[0],ly+current_pos[1],0), App.Vector(lx+current_pos[0],ly+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)

				#ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-0+current_pos[0]-lx,ep/2+current_pos[1],0), App.Vector((2*lx)-((ly-ep)/math.tan(alpha))+current_pos[0]-lx,(ep/2)+current_pos[1],0)),False)
				#Ligne 2-3
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-((ly-ep)/math.tan(alpha))+current_pos[0]-lx,ep/2+current_pos[1],0), App.Vector((2*lx)+current_pos[0]-lx,ly-ep/2+current_pos[1],0)),False)
				#ligne 4-5
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha)))+current_pos[0]-lx,ep/2+current_pos[1],0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1],0)),False)
				#ligne 5-6
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1],0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1],0)),False)
				#ligne 4-6
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha)))+current_pos[0]-lx,ep/2+current_pos[1],0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1],0)),False)

			if j==0:
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(ly-ep)/2*math.tan(alpha/2)+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(lx-(ly-ep)/2*math.tan(alpha/2))+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],(ly-ep)/2+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx-(ly-ep)/2*math.tan(alpha/2)+current_pos[0],0+current_pos[1],0), App.Vector(0+current_pos[0],0+current_pos[1],0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(lx-(ly-ep)/2*math.tan(alpha/2))+current_pos[0],0+current_pos[1],0), App.Vector(2*lx+current_pos[0],0+current_pos[1],0)),False)

			if j==nb_tri_y*4-2:
				# Création du contour 1
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],0+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],0+current_pos[1],0), App.Vector(lx+current_pos[0],ly/2+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ly/2+current_pos[1],0), App.Vector(0+current_pos[0],ly/2+current_pos[1],0)),True)
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly/2+current_pos[1],0), App.Vector(0+current_pos[0],0+current_pos[1],0)),True)

				#ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+current_pos[0],ep/2+current_pos[1]+ly/2,0), App.Vector(lx+(ly-ep)/math.tan(alpha)+current_pos[0],(ep/2)+current_pos[1]+ly/2,0)),False)
				#Ligne 2-3
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+current_pos[0],ep/2+current_pos[1]+ly/2,0), App.Vector(lx+math.tan(alpha/2)*(ly-ep)/2+current_pos[0],ly+current_pos[1],0)),False)
				#ligne 4-5
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+current_pos[0],ep/2+current_pos[1]+ly/2,0), App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1]+ly/2,0)),False)
				#ligne 5-6
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1]+ly/2,0), App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1]+ly/2,0)),False)
				#ligne 4-6
				sketch.addGeometry(Part.LineSegment( App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+current_pos[0],ep/2+current_pos[1]+ly/2,0), App.Vector(lx+((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha)+current_pos[0],(ly-ep)/2+current_pos[1]+ly/2,0)),False)
				
				#ligne 1-2
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-0+current_pos[0]-lx,ep/2+current_pos[1]+ly/2,0), App.Vector((2*lx)-((ly-ep)/math.tan(alpha))+current_pos[0]-lx,(ep/2)+current_pos[1]+ly/2,0)),False)
				#Ligne 2-3
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-((ly-ep)/math.tan(alpha))+current_pos[0]-lx,ep/2+current_pos[1]+ly/2,0), App.Vector(lx-math.tan(alpha/2)*(ly-ep)/2+current_pos[0],ly/2+current_pos[1]+ly/2,0)),False)
				#ligne 4-5
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha)))+current_pos[0]-lx,ep/2+current_pos[1]+ly/2,0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1]+ly/2,0)),False)
				#ligne 5-6
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))+((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1]+ly/2,0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1]+ly/2,0)),False)
				#ligne 4-6
				sketch.addGeometry(Part.LineSegment( App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha)))+current_pos[0]-lx,ep/2+current_pos[1]+ly/2,0), App.Vector((2*lx)-(((ly-ep)/math.tan(alpha))+(ep/math.cos(alpha))-((ly/2)-ep)/math.tan(alpha))+current_pos[0]-lx,(ly-ep)/2+current_pos[1]+ly/2,0)),False)

				#fermeture des bords
				sketch.addGeometry(Part.LineSegment( App.Vector(0+current_pos[0],ly/2+current_pos[1]+ly/2,0), App.Vector(lx-math.tan(alpha/2)*(ly-ep)/2+current_pos[0],ly/2+current_pos[1]+ly/2,0)),False)
				sketch.addGeometry(Part.LineSegment( App.Vector(2*lx+current_pos[0],ly/2+current_pos[1]+ly/2,0), App.Vector(lx+math.tan(alpha/2)*(ly-ep)/2+current_pos[0],ly/2+current_pos[1]+ly/2,0)),False)

		# Extrusion de l'esquisse & Génération des plateaux
	if extrude:
		pad_tri = doc.getObject(nom_body_tri).newObject('PartDesign::Pad', nom_pad_tri)	# Créer un Pad
		pad_tri.Profile = sketch														# Mettre l'esquisse dans le pad
		pad_tri.Length = dimlat_ep														# Définir la longueur d'extrustion
		pad_tri.ReferenceAxis = (sketch, ['N_Axis'])									# Définir la direction d'extrusion
		doc.recompute()																	# Lancer les calculs
		sketch.Visibility = sketch_visible												# Affichage de l'esquisse après l'extrusion
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
							nom_body=nom_body_tri,
							doc=doc,
							nom_sketch_plateaux=nom_sketch_plateaux_extremitees,
							nom_pad_plateaux=nom_pad_plateau_extremitees,
							debug=debug,
							file_debug=file_debug,
							wdebug=wdebug)