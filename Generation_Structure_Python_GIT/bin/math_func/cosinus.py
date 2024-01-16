"""
Génération de la structure cosinus.
Base du code de Valentin BACOUT.
Implémentation par Adrien HERMAN.
16/01/2024
"""

def cosinus_fct(x, phi):
	"""
	Calcul du cos(x + phi) (x et phi en radians).
	"""
	import math
	return math.cos(x + phi)

def gen_cosinus(	ep=0.4,
					doc=None,
					file_debug=None,
					nb_cos_x=4,
					nb_cos_y=4,
					phi=.0,
					nbpts=160,
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
		- phi -> Déphasage du cosinus (Si c'est une liste le déphasage sera effectué pour chaque cosinus)
		- nbpts -> Nombre de points d'échantillonnage de la courbe
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
	import FreeCADGui, ImportGui, Part, Sketcher, math
	sys.path.append("/home/adrienherman/Documents/Shadow Drive/INSA 5A/PLP/Python/dev/Generation_Structure_Python_GIT/bin/math_func/")
	from plot_math_function import plot_math_func

	if doc == None:	doc = FreeCAD.newDocument()

	if file_debug != None and debug: wdebug("""dimlat_x:{0}
												\ndimlat_y:{1}
												\ndimlat_ep:{2}
												\nnb_tri_x:{3}
												\nnb_tri_y:{4}
												\nnom_sketch_tri:{5}
												\n----\n""".format(	dimlat_x,
																	dimlat_y,
																	dimlat_ep,
																	nb_tri_x,
																	nb_tri_y,
																	nom_sketch_tri),
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

	current_pos = (.0, .0, .0)	# Curseur de position (repère local à chaque cosinus)
	sketch_cos = []				# Liste contenant toutes les esquisses des cosinus
	pad_cos = []				# Liste contenant tous les pads des cosinus

	# Création des cosinus suivant l'axe x
	for i in range(nb_cos_x):
		current_pos = (i * espacement_x - ep / 2, .0, .0)

		[echant, pts], d, s = plot_math_func(	nbpts,
												0,
												dimlat_y,
												current_pos,
												cosinus_fct,
												True,
												False,
												doc,
												doc.addObject("Sketcher::SketchObject", nom_sketch_cos),
												debug,
												file_debug,
												wdebug,
												phi)

		current_pos = (i * espacement_x + ep / 2, .0, .0)

		[echant, pts], d, s = plot_math_func(	nbpts,
												0,
												dimlat_y,
												current_pos,
												cosinus_fct,
												True,
												False,
												doc,
												s,
												debug,
												file_debug,
												wdebug,
												phi)

		sketch_cos.append(s)

gen_cosinus()