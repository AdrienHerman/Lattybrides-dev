"""
Génération de la structure Triangles 2D avec gradients
Adrien HERMAN
16/01/2024
"""

def gen_triangle_grad(	ep=0.4,
						doc=None,
						file_debug=None,
						nb_couches=3,
						nb_tri_x=[7,4,7],
						nb_tri_par_couche=[2,3,2],
						alpha=[1.0472,1.0,0.95],
						dimlat_x=40,
						dimlat_par_couche=[40/7*2,40/7*3,40/7*2],
						dimlat_ep=40,
						ep_par_couche=[1,0.5,0.5,1],
						ep_plateaux=[1,0.5,0.5,1],
						semi_debug=False,
						debug=False,
						sketch_visible=False,
						extrude=True,
						nom_sketch_par_couche=["Sketch_Tri1","Sketch_Tri2","Sketch_Tri3"],
						nom_sketch_plateaux=["Sketch_Plateaux1","Sketch_Plateaux2","Sketch_Plateaux3","Sketch_Plateaux4"],
						nom_body_tri="Body_Tri_2D_Alignes",
						nom_pad_par_couche=["Pad_Tri1","Pad_Tri2","Pad_Tri3"],
						nom_pad_plateaux=["Pad_Plateaux1","Pad_Plateaux2","Pad_Plateaux3","Pad_Plateaux4"],
						gen_plateaux=None,
						gen_tri=None,
						wdebug=None):
	"""
	Génération de la structure avec gradients.

	-----------
	Variables :
		- ep -> Épaisseur des parois de la structure lattice
		- doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		- file_debug -> Fichier de déboggage (ouvert)
		- nb_tri_x / nb_tri_y -> Nombre d'hexagones sur la distance x / y
		- alpha -> Angle des triangles
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
		- gen_tri -> Fonction de génération des triangles
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher

	if doc == None: FreeCAD.newDocument()						# Création du document
	posy = 0 													# Position y de l'origine des esquisses à créer
	sketches = []												# Liste contenant toutes les esquisses des hexagones + triangles

	if file_debug != None and debug:
		wdebug("Création du body du triangle : {0}\n".format(nom_body_tri), file_debug)

	body = doc.addObject('PartDesign::Body', nom_body_tri)	# Créer un body

	for no_couche in range(nb_couches):
		# Création de l'esquisse de la couche
		if file_debug != None and debug:
			wdebug("Création de l'esquisse du triangle pour la couche {1}: {0}\n".format(nom_sketch_par_couche[no_couche], no_couche), file_debug)

		sketches.append(doc.addObject("Sketcher::SketchObject", nom_sketch_par_couche[no_couche]))
		sketches[no_couche].Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))

		if file_debug != None and debug:
			wdebug("""Génération de la structure triangle pour la couche {0}:\n     posy = {1}\n""".format(	no_couche,
																											posy), file_debug)

		# Génération de la structure sur le couche no_couche
		gen_tri(	ep=ep * ep_par_couche[no_couche],
					doc=doc,
					file_debug=file_debug,
					nb_tri_x=nb_tri_x[no_couche],
					nb_tri_y=nb_tri_par_couche[no_couche],
					alpha=alpha[no_couche],
					dimlat_ep=dimlat_ep,
					dimlat_x=dimlat_x,
					dimlat_y=dimlat_par_couche[no_couche],
					ep_plateaux=[0, 0],
					semi_debug=semi_debug,
					debug=debug,
					sketch_visible=sketch_visible,
					extrude=False,
					nom_sketch_tri=nom_sketch_par_couche[no_couche],
					nom_sketch_plateaux_extremitees=nom_sketch_plateaux[no_couche],
					nom_body_tri=nom_body_tri,
					nom_pad_tri=nom_pad_par_couche[no_couche],
					nom_pad_plateau_extremitees=nom_pad_plateaux[no_couche],
					gen_plateaux=None,
					generation_plateaux_extremitees=False,
					wdebug=wdebug,
					sketch=sketches[no_couche])

		# Incrément de la position y dans le repère
		posy += dimlat_par_couche[no_couche]

	# Extrusion des l'esquisses & Génération des plateaux
	if extrude:
		# Extrusion de chaque couches
		for no_couche in range(nb_couches):
			body.newObject('PartDesign::Pad', nom_pad_par_couche[no_couche])									# Créer un Pad
			doc.getObject(nom_pad_par_couche[no_couche]).Profile = sketches[no_couche]							# Mettre l'esquisse dans le pad
			doc.getObject(nom_pad_par_couche[no_couche]).Length = dimlat_ep										# Définir la longueur d'extrustion
			doc.getObject(nom_pad_par_couche[no_couche]).ReferenceAxis = (sketches[no_couche], ['N_Axis'])		# Définir la direction d'extrusion
			doc.recompute()																						# Lancer les calculs
			sketches[no_couche].Visibility = sketch_visible														# Affichage de l'esquisse après l'extrusion
			
			if file_debug != None and debug:
				wdebug("Extrusion de la structure : Couche no {0}\n".format(no_couche), file_debug)

		# Génération des plateaux liants les couches de la structure
		if file_debug != None and debug:
			wdebug("Création des plateaux liants les couches de la structure.\n", file_debug)

		gen_plateaux(	nb_couches=nb_couches,
						ep_plateaux=ep_plateaux,
						dimlat_x=dimlat_x,
						dimlat_par_couche=dimlat_par_couche,
						dimlat_ep=dimlat_ep,
						sketch_visible=sketch_visible,
						nom_body=nom_body_tri,
						doc=doc,
						nom_sketch_plateaux=nom_sketch_plateaux,
						nom_pad_plateaux=nom_pad_plateaux,
						debug=debug,
						file_debug=file_debug,
						wdebug=wdebug)