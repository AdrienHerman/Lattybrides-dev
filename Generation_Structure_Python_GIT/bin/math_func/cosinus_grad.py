"""
Génération de la structure Cosinus 2D avec gradients
Adrien HERMAN
19/01/2024
"""

def gen_cosinus_grad(	ep=0.4,
						doc=None,
						file_debug=None,
						nb_cos=[4,4],
						nb_plateaux_y=[4,4],
						amp=[1.0,1.0],
						period_fact=[0.5,0.5],
						phi=[.0,.0],
						nbpts=[160,160],
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
						nom_sketch_cos=["Sketch_Cos_1_", "Sketch_Cos_2_"],
						nom_sketch_plateaux_extremitees=["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
						nom_body_cos=["Body_Cos_1_", "Body_Cos_2_"],
						nom_pad_cos=["Pad_Cos_1_", "Pad_Cos_2_"],
						nom_pad_plateau_extremitees=["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
						gen_plateaux=None,
						generation_plateaux_extremitees=True,
						wdebug=None):
	"""
	Génération de la structure avec gradients.

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