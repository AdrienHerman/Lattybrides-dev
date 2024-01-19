"""
Tracer une fonction mathématique sur une esquisse avec une B-Spline.
HERMAN Adrien
16/01/2024
"""

def def_func(x, *args):
	"""
	Fonction mathématique par défaut (y=x).
	"""

	return x

def plot_math_func(	nbpts=10,
					xy_0=.0,
					xy_fin=10.0,
					current_pos=(.0,.0,.0),
					func=def_func,
					x=False,
					y=True,
					doc=None,
					sketch=None,
					debug=False,
					file_debug=None,
					wdebug=None,
					*args):
	"""
	Tracer une fonction mathématique dans une esquisse.
	
	-----------
	Variables :
		- nbpts -> Nombre de points pour la discrétisation de la courbe
		- xy_0 / xy_fin -> Début / fin de l'intervalle de calcul de la fonction mathématique
		- current_pos -> Curseur de position
		- func -> Fonction mathématique à tracer
		- x / y -> = True si la fonction mathématique doit être tracée sur l'axe
		- doc -> Document où tracer la fonction mathématique
		- sketch -> Esquisse où tracer la fonction mathématique
		- debug -> Afficher les actions dans le terminal et dans le fichier de déboggage
		- file_debug -> Fichier de déboggage (ouvert)
		- wdebug -> Fonction d'écriture des informations de débogage dans le terminal et dans le fichier log
		- *args -> Arguments de la fonction mathématique à compléter
	-----------

	---------
	Retours :
		- [echantillonnage, pts_fct] -> Points d'échantillonnage et images au travers de la fonction mathématique
		- doc -> Objet "document" où à été tracé la courbe
		- sketch -> Objet "esquisse" où a été tracé la courbe
	---------
	"""

	# Importation des modules externes
	import FreeCAD as App
	import FreeCADGui, ImportGui, Part, Sketcher, math
	import numpy as np

	# Création du document et de l'esquisse
	if doc == None:
		doc = FreeCAD.newDocument()
		if file_debug != None and debug:	wdebug("Création d'un nouveau document\n", file_debug)

	if sketch == None:
		sketch = doc.addObject("Sketcher::SketchObject", "Plot_Sketch")
		if file_debug != None and debug:	wdebug("Création d'une nouvelle esquisse\n\n", file_debug)

	# Calculer la fonction mathématique
	if file_debug != None and debug:	wdebug("Calcul du vecteur d'échantillonnage = [", file_debug)
	echantillonnage = np.ndarray.tolist(np.arange(xy_0, xy_fin + (xy_fin - xy_0) / nbpts, (xy_fin - xy_0) / nbpts))
	if file_debug != None and debug:
		for e in echantillonnage:
			wdebug("{0},".format(e), file_debug)
		wdebug("]\n\n", file_debug)

	if file_debug != None and debug:	wdebug("Calcul du vecteur de la fonction mathématique = [", file_debug)
	if y:	pts_fct = [func(e, *args) + current_pos[1] for e in echantillonnage]
	elif x:	pts_fct = [func(e, *args) + current_pos[0] for e in echantillonnage]
	if file_debug != None and debug:
		for pts in pts_fct:
			wdebug("{0},".format(pts), file_debug)
		wdebug("]\n\n", file_debug)

	if file_debug != None and debug:	wdebug("Création des objets points FreeCAD.\n", file_debug)
	if y:
		pts_freecad = [App.Vector(echantillonnage[i], pts_fct[i], 0) for i in range(len(pts_fct))]
		for pts in pts_freecad:	sketch.addGeometry(Part.Point(pts), False)

	elif x:
		pts_freecad = [App.Vector(pts_fct[i], echantillonnage[i], 0) for i in range(len(pts_fct))]
		for pts in pts_freecad:	sketch.addGeometry(Part.Point(pts), False)

	# Tracer la fonction mathématique
	if file_debug != None and debug:	wdebug("Traçage de la B-Spline.\n", file_debug)
	_finalbsp_poles = []
	_finalbsp_knots = []
	_finalbsp_mults = []
	_bsps = []
	_bsps.append(Part.BSplineCurve())
	_bsps[-1].interpolate(pts_freecad, PeriodicFlag=False)
	_bsps[-1].increaseDegree(3)
	_finalbsp_poles.extend(_bsps[-1].getPoles())
	_finalbsp_knots.extend(_bsps[-1].getKnots())
	_finalbsp_mults.extend(_bsps[-1].getMultiplicities())
	sketch.addGeometry(Part.BSplineCurve(_finalbsp_poles,_finalbsp_mults,_finalbsp_knots,False,3,None,False),False)

	return [echantillonnage, pts_fct], doc, sketch