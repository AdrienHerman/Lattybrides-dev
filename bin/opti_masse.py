"""
Optimisation de la masse de la structure en modifiant l'épaisseur de paroie
HERMAN Adrien
03/10/2023
"""

def affichage_calculs_masse(masse, objectif_masse, tolerance, pas, ep, porosite, file_debug, precision=2):
	"""
	Afficher un graphique avec les calculs de la masse

	-----------
	Variables :
		masse -> Tableau avec les itérations de calcul sur la masse
		objectif_masse -> Masse cible en g
		tolerance -> Tolérance de calcul sur la masse en g
		pas -> Pas de calcul
		ep -> Épaisseur de la paroi de la structure lattice
		porosite -> Porosite de la structure lattice
		file_debug -> Fichier de déboggage (ouvert)
		precision -> Arrondi sur les nombres à afficher
	-----------
	"""

	# Importation des modules externes
	import matplotlib.pyplot as plt
	from matplotlib.ticker import MaxNLocator

	fig, ax = plt.subplots()
	ax.set_title("Nb_Iter = {0} | Masse_Finale = {1} g | Ep_Finale = {2} mm | Porosite = {3} % | Tolerance = +- {4} g".format(pas, round(masse[pas - 1], precision), round(ep, precision), round(porosite, precision), tolerance / 2))
	ax.set_xlabel("Nombre d'Itérations")
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	ax.set_ylabel("Masse (g)")
	ax.plot([i for i in range(pas)], masse[:pas], "b-", label="Masse Calculée")
	ax.plot([i for i in range(pas)], [objectif_masse for i in range(pas)], "g--", label="Masse Cible")
	ax.plot([i for i in range(pas)], [objectif_masse - tolerance / 2 for i in range(pas)], "r-.", label="Tolérance Inférieure")
	ax.plot([i for i in range(pas)], [objectif_masse + tolerance / 2 for i in range(pas)], "r-.", label="Tolérance Supérieure")
	ax.legend()
	plt.grid()
	plt.show()

def suppr_structure(doc,
					nom_body,
					nom_sketch_losange,
					nom_sketch_plateaux):
	"""
	Suppression des sets de données
	
	-----------
	Variables :
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		nom_body-> Nom de la pièce
		nom_sketch_losange -> Nom de l'esquisse du losange
		nom_sketch_plateaux -> Nom de l'esquisse de définition des plateaux
	-----------
	"""

	doc.getObject(nom_body).removeObjectsFromDocument()
	doc.removeObject(nom_body)
	if type(nom_sketch_losange) == list:
		for sketch_losange in nom_sketch_losange:
			try:	doc.removeObject(sketch_losange)
			except:	pass
	else:
		doc.removeObject(nom_sketch_losange)

	if type(nom_sketch_plateaux) == list:
		for sketch_plateaux in nom_sketch_plateaux:
			try:	doc.removeObject(sketch_plateaux)
			except:	pass
	else:
		doc.removeObject(nom_sketch_plateaux)
	doc.recompute()

def opti_masse(	doc,
				nom_body,
				nom_pad_losange,
				nom_pad_plateaux,
				nom_sketch_losange,
				nom_sketch_plateaux,
				gen,
				file_debug,
				wdebug,
				debug=False,
				tolerance=1e-3,
				nb_pas_max=100,
				masse=[],
				ep=0.1,
				pas=0,
				correction_ep_par_pas=0.01,
				pourcentage_modification_correction=0.15,
				seuil_augmentation_correction=0.05,
				seuil_diminution_correction=0.5,
				objectif_masse=2.8,
				rho=1.24,
				volume_max=1,
				*args):
	
	"""
	Optimisation de la masse de la structure

	-----------
	Variables :		
		doc -> Document FreeCAD (Attention il s'agit de l'objet document, il doit-être ouvert)
		nom_body-> Nom de la pièce
		nom_pad_losange -> Nom du pad du losange
		nom_pad_plateau -> Num du pad des plateaux liant les parties hautes et basses de la structure
		nom_sketch_losange -> Nom de l'esquisse du losange
		nom_sketch_plateaux -> Nom de l'esquisse de définition des plateaux
		gen -> Fonction de génération de la structure lattice
		file_debug -> Fichier de déboggage (ouvert)
		wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
				debug_current_folder -> Générer le fichier de déboggage dans
			le dossier "debug" du répertoire courrant si True, sinon
			Générer le fichier de déboggae dans le dossier indiqué dans la variable
		tolerance -> Tolérance de calcul sur la masse en g
		nb_pas_max -> Nombre maximal de pas de calcul
		masse -> Tableau avec les itérations de calcul sur la masse
		ep -> Épaisseur de la paroi de la structure lattice
		pas -> Pas de calcul
		correction_ep_par_pas -> Pas de correction en épaisseur à chaque étape
		pourcentage_modification_correction -> Pourcentage de modification de la variable correction_ep_par_pas
		seuil_augmentation_correction / seuil_diminution_correction -> Seuils à dépasser pour augmenter / diminuer la variable correction_ep_par_pas
		objectif_masse -> Masse cible en g
		rho -> Masse volumique du matériau utilisé en g/cm^3
		volume_max -> Volume d'encombrement de la structure (utilisé pour le calcul de la porosité)
		*args -> Arguments de la fonction de génération
	-----------
	"""

	# Importation des modules externes
	import sys

	# Génération de la structure
	gen(ep, doc, file_debug, *args)
	
	# Récupération du volume de la pièce et calcul de la masse
	if type(nom_pad_losange) == list:
		volume_sans_plateaux = 0
		for pad_losange in nom_pad_losange:
			volume_sans_plateaux += doc.getObject(pad_losange).Shape.Volume * 1e-3	# cm^3
	else:
		volume_sans_plateaux = doc.getObject(nom_pad_losange).Shape.Volume * 1e-3	# cm^3
		
	volume_avec_plateaux = doc.getObject(nom_body).Shape.Volume * 1e-3				# cm^3
	masse[pas] = volume_avec_plateaux * rho											# g
	porosite = (1 - volume_sans_plateaux / volume_max) * 100						# %
	if file_debug != None and debug:
		wdebug("\n---\nPas d'optimisation : {0}\n".format(pas + 1), file_debug)
		wdebug("    Calcul de la masse : {0} g\n    Calcul de la porosite : {1} %\n".format(masse[pas], porosite), file_debug)

	# Variation automatique du pas de correction de l'épaisseur
	if pas > 0:
		if abs(masse[pas] - masse[pas - 1]) <= seuil_augmentation_correction:
			correction_ep_par_pas *= (1 + pourcentage_modification_correction)
			if file_debug != None and debug:
				wdebug("    Augmentation du pas de correction : {0} mm\n".format(correction_ep_par_pas), file_debug)

		if abs(masse[pas] - masse[pas - 1]) >= seuil_diminution_correction:
			correction_ep_par_pas *= (1 - pourcentage_modification_correction)
			if file_debug != None and debug:
				wdebug("    Diminution du pas de correction : {0} mm\n".format(correction_ep_par_pas), file_debug)

	# Test des pas de calculs
	if pas < nb_pas_max - 1:
		# Test masse
		if abs(masse[pas] - objectif_masse) <= tolerance / 2:	# Masse OK
			if file_debug != None and debug:
				wdebug("    Objectif de masse atteint ! : {0} g\n".format(masse[pas]), file_debug)

			return masse, pas + 1, ep, porosite

		elif masse[pas] < objectif_masse:					# Rajout d'épaisseur nécessaire
			# Suppression de l'ancienne structure
			suppr_structure(doc,
							nom_body,
							nom_sketch_losange,
							nom_sketch_plateaux)

			if file_debug != None and debug:
				wdebug("    Rajout d'épaisseur nécessaire pour satisfaire le critère de masse : +{0} mm\n".format(correction_ep_par_pas), file_debug)

			return opti_masse(
				doc,
				nom_body,
				nom_pad_losange,
				nom_pad_plateaux,
				nom_sketch_losange,
				nom_sketch_plateaux,
				gen,
				file_debug,
				wdebug,
				debug,
				tolerance,
				nb_pas_max,
				masse,
				ep + correction_ep_par_pas,
				pas + 1,
				correction_ep_par_pas,
				pourcentage_modification_correction,
				seuil_augmentation_correction,
				seuil_diminution_correction,
				objectif_masse,
				rho,
				volume_max,
				*args)

		elif masse[pas] > objectif_masse:					# Retraît d'épaisseur nécessaire
			# Suppression de l'ancienne structure
			suppr_structure(doc,
							nom_body,
							nom_sketch_losange,
							nom_sketch_plateaux)

			if file_debug != None and debug:
				wdebug("    Diminution d'épaisseur nécessaire pour satisfaire le critère de masse : -{0} mm\n".format(correction_ep_par_pas), file_debug)

			return opti_masse(
				doc,
				nom_body,
				nom_pad_losange,
				nom_pad_plateaux,
				nom_sketch_losange,
				nom_sketch_plateaux,
				gen,
				file_debug,
				wdebug,
				debug,
				tolerance,
				nb_pas_max,
				masse,
				ep - correction_ep_par_pas,
				pas + 1,
				correction_ep_par_pas,
				pourcentage_modification_correction,
				seuil_augmentation_correction,
				seuil_diminution_correction,
				objectif_masse,
				rho,
				volume_max,
				*args)

	else:
		if file_debug != None and debug:
			wdebug("""\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
					\n!!! NOMBRE MAXIMAL DE PAS ATTEINT !!!
					\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n""", file_debug)

		return masse, pas, ep, porosite