"""
Génération d'une structure lattice à base de losanges
et à gradients d'épaisseur
HERMAN Adrien
10/10/2023
"""

def losange_grad(	ep=0.4,
					doc=None,
					file_debug=None,
					nb_couches=3,
					nb_losange_par_couche=[2,3,2],
					dimlat_par_couche=[40/7*2,40/7*3,40/7*2],
					ep_par_couche=[1,0.5,0.5,1],
					nom_sketch_par_couche=["Sketch_Losange1","Sketch_Losange2","Sketch_Losange3"],
					nom_pad_par_couche=["Pad_Losange1","Pad_Losange2","Pad_Losange3"],
					dimlat_x=40,
					dimlat_ep=40,
					nb_losange_x=[7,4,7],
					nom_sketch_plateaux=["Sketch_Plateaux1","Sketch_Plateaux2","Sketch_Plateaux3","Sketch_Plateaux4"],
					nom_pad_plateaux=["Pad_Plateaux1","Pad_Plateaux2","Pad_Plateaux3","Pad_Plateaux4"],
					nom_body_losange="Body_Losange",
					ep_plateaux=[1,0.5,0.5,1],
					gen_plateaux=None,
					gen_losange=None,
					sketch_visible=False,
					extrude=True,
					semi_debug=False,
					debug=False,
					wdebug=None):
	"""
	Construire un gradient d'épaisseur dans la hauteur du losange
	Couches de losanges d'épaisseur de parois différentes

	-----------
	Variables :
		ep -> Épaisseur de référence pour les parois des différentes couches de la structure lattice
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		file_debug -> Fichier de déboggage (ouvert)
		nb_couches : Nombre de couches différentes à générer
		nb_losange_par_couche : Liste des nombre de losange à générer pour chaque couche
		dimlat_par_couche : Liste des dimensions y de chaque couches
		ep_par_couche : Liste de tous les facteurs d'épaisseur à chaque couche (facteur * ep)
		nom_sketch_par_couche : Liste de tous les noms d'esquisses
		nom_pad_par_couche -> Nom de tous les pad des losanges pour chaque couche
		dimlat_x -> Dimension de la zone de construction
		dimlat_ep -> Épaisseur d'extrusion de la structure lattice
		nb_losange_x -> Nombre de losanges sur la distance x
		nom_sketch_plateaux -> Nom de l'esquisse de définition des plateaux
		nom_pad_plateau -> Num du pad des plateaux liant les parties hautes et basses de la structure
		nom_body_losange -> Nom de la pièce
		ep_plateaux -> Épaisseur des plateaux liant les extrémités de la structure (dans le sens de chargement)
		gen_plateaux -> Fonction de génération des plateaux liant les deux extrémités
		gen_losange -> Fonction de génération de la structure losange
		sketch_visible -> Afficher l'esquisse de départ après l'extrusion = True
		extrude -> Réaliser l'extrusion = True
		semi_debug -> Tracer les lignes de construction
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
	-----------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher

	if doc == None: FreeCAD.newDocument()						# Création du document
	posy = 0 													# Position y de l'origine des esquisses à créer
	sketches = []												# Liste contenant toutes les esquisses des losanges

	if file_debug != None and debug:
		wdebug("Création du body du losange : {0}\n".format(nom_body_losange), file_debug)

	body = doc.addObject('PartDesign::Body', nom_body_losange)	# Créer un body

	for no_couche in range(nb_couches):
		# Création de l'esquisse de la couche
		if file_debug != None and debug:
			wdebug("Création de l'esquisse du losange pour la couche {1}: {0}\n".format(nom_sketch_par_couche[no_couche], no_couche), file_debug)

		sketches.append(doc.addObject("Sketcher::SketchObject", nom_sketch_par_couche[no_couche]))
		sketches[no_couche].Placement = App.Placement(App.Vector(0, posy, 0), App.Rotation(0, 0, 0, 1))

		if file_debug != None and debug:
			wdebug("""Génération de la structure losange pour la couche {0}:\n     posy = {1}\n""".format(	no_couche,
																											posy), file_debug)

		# Génération de la structure sur le couche no_couche
		gen_losange(	ep=ep * ep_par_couche[no_couche],
						doc=doc,
						file_debug=file_debug,
						nb_losange_x=nb_losange_x[no_couche],
						nb_losange_y=nb_losange_par_couche[no_couche],
						dimlat_ep=dimlat_ep,
						dimlat_x=dimlat_x,
						dimlat_y=dimlat_par_couche[no_couche],
						ep_plateaux=[0, 0],
						semi_debug=semi_debug,
						debug=debug,
						sketch_visible=sketch_visible,
						extrude=False,
						nom_sketch_losange=nom_sketch_par_couche[no_couche],
						nom_sketch_plateaux_extremitees=nom_sketch_plateaux[no_couche],
						nom_body_losange=nom_body_losange,
						nom_pad_losange=nom_pad_par_couche[no_couche],
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
						nom_body=nom_body_losange,
						doc=doc,
						nom_sketch_plateaux=nom_sketch_plateaux,
						nom_pad_plateaux=nom_pad_plateaux,
						debug=debug,
						file_debug=file_debug,
						wdebug=wdebug)