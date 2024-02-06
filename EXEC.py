"""
Exécution du script de génération de structure
via l'interface graphique.
HERMAN Adrien
06/02/2024
"""

# Modules de Python
from FreeCAD import Gui
import FreeCAD as App
from PySide import QtGui
import os, time, sys

# Détection du dossier de travail
softpath = os.path.dirname(__file__)
iconPath = os.path.join(softpath, "icons")
binPath = os.path.join(softpath, "bin")

# Modules du Logiciel
sys.path.append(softpath + "/bin/")
sys.path.append(softpath + "/bin/losange/")
sys.path.append(softpath + "/bin/hexagone_triangle1_2D/")
sys.path.append(softpath + "/bin/triangle/")
sys.path.append(softpath + "/bin/math_func/")
from lecture_param import *
from plateaux_liants import *
from export_body import *
from opti_masse import *
from debug import *
from losange.losange import *
from losange.losange_grad import *
from hexagone_triangle1_2D.hex_tri1_2D import *
from hexagone_triangle1_2D.hex_tri1_2D_grad import *
from triangle.triangle_struct import *
from triangle.triangle_grad import *
from math_func.cosinus import *
from math_func.cosinus_grad import *
from math_func.plot_math_function import *

class EXEC_Class:
	"""
	Classe d'exécution du script de génération de la structure.
	"""

	def __init__(self):
		print("\n*** INITIALISATION DE LA CLASSE POUR L'EXECUTION DE LA GENERATION DE STRUCTURE ***\n")

	def GetResources(self):
		return {
		"Pixmap": os.path.join(iconPath, "softicon.png"),
		"MenuText": "Générer la structure lattice",
		"ToolTip": "Générer la structure lattice correspondant au fichier de configuration.",
		}

	def Activated(self):
		# Lecture des parmaètres du programme
		[	lecture_param_ok,
			gen_losange_basic,
			gen_losange_grad,
			gen_hex_tri1_2D_aligne_basic,
			gen_hex_tri1_2D_aligne_grad,
			gen_hex_tri1_2D_naligne_basic,
			gen_hex_tri1_2D_naligne_grad,
			gen_tri_2D_basic,
			gen_tri_2D_grad,
			gen_cos_2D_basic,
			gen_cos_2D_grad,
			generation_plateaux_extremitees,
			ep_plateaux_extremitees,
			ep,
			dimlat_ep,
			dimlat_x,
			dimlat_y,
			optimisation_masse,
			objectif_masse,
			tolerance,
			nb_pas_max,
			correction_ep_par_pas,
			pourcentage_modification_correction,
			seuil_augmentation_correction,
			seuil_diminution_correction,
			rho,
			nb_motif_x_sg,
			nb_motif_y_sg,
			nb_y_par_couche,
			nb_x_par_couche,
			dimlat_par_couche_manuel,
			dimlat_par_couche,
			ep_par_couche,
			ep_plateaux,
			alpha_hex_tri1_2D,
			alpha_hex_tri1_2D_grad,
			alpha_tri_2D,
			alpha_tri_2D_grad,
			phi,
			period_fact,
			amp,
			nbpts_cos,
			phi_grad,
			period_fact_grad,
			amp_grad,
			nbpts_cos_grad,
			extrude,
			export,
			export_name,
			export_path,
			sketch_visible,
			semi_debug,
			debug,
			debug_current_folder,
			log] = lecture_param(softpath + "/config.py")

		# Création du fichier de débogage & écriture des log de la fonction lecture_param
		if not debug_current_folder:	debug_current_folder = "log/"
		file_debug = create_file_debug(softpath + debug_current_folder)
		wdebug(log, file_debug)

		if lecture_param_ok:
			# Effacer les consoles Python et la Vue Rapport
			mw = Gui.getMainWindow()
			c = mw.findChild(QtGui.QPlainTextEdit, "Python console")
			c.clear()
			r = mw.findChild(QtGui.QTextEdit, "Report view")
			r.clear()

			# Initialisation des variables
			volume_max = dimlat_x * dimlat_y * dimlat_ep * 1e-3					# Volume maximal calculé (cm^3)
			temps_debut = time.time()											# Calcul de la durée d'exécution
			doc = App.newDocument()												# Création d'un nouveau document FreeCAD

			if gen_losange_basic:
				nom_body = "Body_Losange"
				if optimisation_masse:
					masse, pas_final, ep_finale, porosite = opti_masse(	
							doc,
							nom_body,
							"Pad_Losange",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							"Sketch_Losange",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							gen_losange,
							file_debug,
							wdebug,
							debug,
							tolerance,
							nb_pas_max,
							[0 for i in range(nb_pas_max + 1)],
							ep,
							0,
							correction_ep_par_pas,
							pourcentage_modification_correction,
							seuil_augmentation_correction,
							seuil_diminution_correction,
							objectif_masse,
							rho,
							volume_max,
							nb_motif_x_sg,
							nb_motif_y_sg,
							dimlat_ep,
							dimlat_x,
							dimlat_y,
							ep_plateaux_extremitees,
							semi_debug,
							debug,
							sketch_visible,
							extrude,
							"Sketch_Losange",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							nom_body,
							"Pad_Losange",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							gen_plateaux,
							generation_plateaux_extremitees,
							wdebug)

				else:
					gen_losange(	ep,
									doc,
									file_debug,
									nb_motif_x_sg,
									nb_motif_y_sg,
									dimlat_ep,
									dimlat_x,
									dimlat_y,
									ep_plateaux_extremitees,
									semi_debug,
									debug,
									sketch_visible,
									extrude,
									"Sketch_Losange",
									["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
									nom_body,
									"Pad_Losange",
									["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
									gen_plateaux,
									generation_plateaux_extremitees,
									wdebug)

			elif gen_hex_tri1_2D_aligne_basic:
				nom_body = "Body_Hex_Tri1_2D_Alignes"
				if optimisation_masse:
					masse, pas_final, ep_finale, porosite = opti_masse(	
							doc,
							nom_body,
							"Pad_Hex_Tri1_2D_Alignes",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							"Sketch_Hex_Tri1_2D_Alignes",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							gen_hex_tri1_2D_aligne,
							file_debug,
							wdebug,
							debug,
							tolerance,
							nb_pas_max,
							[0 for i in range(nb_pas_max + 1)],
							ep,
							0,
							correction_ep_par_pas,
							pourcentage_modification_correction,
							seuil_augmentation_correction,
							seuil_diminution_correction,
							objectif_masse,
							rho,
							volume_max,
							nb_motif_x_sg,
							nb_motif_y_sg,
							alpha_hex_tri1_2D,
							dimlat_x,
							dimlat_y,
							dimlat_ep,
							ep_plateaux_extremitees,
							semi_debug,
							debug,
							sketch_visible,
							extrude,
							"Sketch_Hex_Tri1_2D_Alignes",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							nom_body,
							"Pad_Hex_Tri1_2D_Alignes",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							gen_plateaux,
							generation_plateaux_extremitees,
							wdebug)

				else:
					gen_hex_tri1_2D_aligne(	ep,
											doc,
											file_debug,
											nb_motif_x_sg,
											nb_motif_y_sg,
											alpha_hex_tri1_2D,
											dimlat_x,
											dimlat_y,
											dimlat_ep,
											ep_plateaux_extremitees,
											semi_debug,
											debug,
											sketch_visible,
											extrude,
											"Sketch_Hex_Tri1_2D_Alignes",
											["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
											nom_body,
											"Pad_Hex_Tri1_2D_Alignes",
											["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
											gen_plateaux,
											generation_plateaux_extremitees,
											wdebug)

			elif gen_hex_tri1_2D_naligne_basic:
				nom_body = "Body_Hex_Tri1_2D_Alignes"
				if optimisation_masse:
					masse, pas_final, ep_finale, porosite = opti_masse(	
							doc,
							nom_body,
							"Pad_Hex_Tri1_2D_Alignes",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							"Sketch_Hex_Tri1_2D_Alignes",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							gen_hex_tri1_2D_naligne,
							file_debug,
							wdebug,
							debug,
							tolerance,
							nb_pas_max,
							[0 for i in range(nb_pas_max + 1)],
							ep,
							0,
							correction_ep_par_pas,
							pourcentage_modification_correction,
							seuil_augmentation_correction,
							seuil_diminution_correction,
							objectif_masse,
							rho,
							volume_max,
							nb_motif_x_sg,
							nb_motif_y_sg,
							alpha_hex_tri1_2D,
							dimlat_x,
							dimlat_y,
							dimlat_ep,
							ep_plateaux_extremitees,
							semi_debug,
							debug,
							sketch_visible,
							extrude,
							"Sketch_Hex_Tri1_2D_Alignes",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							nom_body,
							"Pad_Hex_Tri1_2D_Alignes",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							gen_plateaux,
							generation_plateaux_extremitees,
							wdebug)

				else:
					gen_hex_tri1_2D_naligne(	ep,
												doc,
												file_debug,
												nb_motif_x_sg,
												nb_motif_y_sg,
												alpha_hex_tri1_2D,
												dimlat_x,
												dimlat_y,
												dimlat_ep,
												ep_plateaux_extremitees,
												semi_debug,
												debug,
												sketch_visible,
												extrude,
												"Sketch_Hex_Tri1_2D_Alignes",
												["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
												nom_body,
												"Pad_Hex_Tri1_2D_Alignes",
												["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
												gen_plateaux,
												generation_plateaux_extremitees,
												wdebug)

			elif gen_tri_2D_basic:
				nom_body = "Body_Tri_2D"
				if optimisation_masse:
					masse, pas_final, ep_finale, porosite = opti_masse(	
							doc,
							nom_body,
							"Pad_Tri_2D",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							"Sketch_Tri_2D",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							gen_triangle_basic,
							file_debug,
							wdebug,
							debug,
							tolerance,
							nb_pas_max,
							[0 for i in range(nb_pas_max + 1)],
							ep,
							0,
							correction_ep_par_pas,
							pourcentage_modification_correction,
							seuil_augmentation_correction,
							seuil_diminution_correction,
							objectif_masse,
							rho,
							volume_max,
							nb_motif_x_sg,
							nb_motif_y_sg,
							alpha_tri_2D,
							dimlat_x,
							dimlat_y,
							dimlat_ep,
							ep_plateaux_extremitees,
							semi_debug,
							debug,
							sketch_visible,
							extrude,
							"Sketch_Tri_2D",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							nom_body,
							"Pad_Tri_2D",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							gen_plateaux,
							generation_plateaux_extremitees,
							wdebug)

				else:
					gen_triangle_basic(	ep,
										doc,
										file_debug,
										nb_motif_x_sg,
										nb_motif_y_sg,
										alpha_tri_2D,
										dimlat_x,
										dimlat_y,
										dimlat_ep,
										ep_plateaux_extremitees,
										semi_debug,
										debug,
										sketch_visible,
										extrude,
										"Sketch_Tri_2D",
										["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
										nom_body,
										"Pad_Tri_2D",
										["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
										gen_plateaux,
										generation_plateaux_extremitees,
										wdebug)

			elif gen_cos_2D_basic:
				nom_body = "Body_Cos_2D"
				if optimisation_masse:
					masse, pas_final, ep_finale, porosite = opti_masse(	
							doc,
							nom_body,
							"Pad_Cos_2D",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							"Sketch_Cos_2D",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							gen_cosinus,
							file_debug,
							wdebug,
							debug,
							tolerance,
							nb_pas_max,
							[0 for i in range(nb_pas_max + 1)],
							ep,
							0,
							correction_ep_par_pas,
							pourcentage_modification_correction,
							seuil_augmentation_correction,
							seuil_diminution_correction,
							objectif_masse,
							rho,
							volume_max,
							nb_motif_x_sg,
							nb_motif_y_sg,
							amp,
							period_fact,
							phi,
							nbpts_cos,
							plot_math_func,
							cosinus_fct,
							dimlat_x,
							dimlat_y,
							dimlat_ep,
							ep_plateaux_extremitees,
							semi_debug,
							debug,
							sketch_visible,
							extrude,
							"Sketch_Cos_2D",
							["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
							nom_body,
							"Pad_Cos_2D",
							["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
							gen_plateaux,
							generation_plateaux_extremitees,
							wdebug)

				else:
					gen_cosinus(	ep,
									doc,
									file_debug,
									nb_motif_x_sg,
									nb_motif_y_sg,
									amp,
									period_fact,
									phi,
									nbpts_cos,
									plot_math_func,
									cosinus_fct,
									dimlat_x,
									dimlat_y,
									dimlat_ep,
									ep_plateaux_extremitees,
									semi_debug,
									debug,
									sketch_visible,
									extrude,
									"Sketch_Cos_2D",
									["Sketch_Plateau_Dessous", "Sketch_Plateau_Dessus"],
									nom_body,
									"Pad_Cos_2D",
									["Pad_Plateau_Dessous", "Pad_Plateau_Dessus"],
									gen_plateaux,
									generation_plateaux_extremitees,
									wdebug)

			elif gen_losange_grad or gen_hex_tri1_2D_aligne_grad or gen_hex_tri1_2D_naligne_grad or gen_tri_2D_grad or gen_cos_2D_grad:
				# Création des listes pour les plateaux
				plateaux = []
				if generation_plateaux_extremitees:	plateaux.append(ep_plateaux_extremitees[0])
				plateaux += ep_plateaux
				if generation_plateaux_extremitees:	plateaux.append(ep_plateaux_extremitees[1])

				# Création des listes pour les noms des objets
				nb_couches = len(nb_y_par_couche)
				if gen_losange_grad:				nom_struct = "Losange"
				elif gen_hex_tri1_2D_aligne_grad:	nom_struct = "Hex_Tri_2D_aligne"
				elif gen_hex_tri1_2D_naligne_grad:	nom_struct = "Hex_Tri_2D_naligne"
				elif gen_tri_2D_grad:				nom_struct = "Tri_2D"
				elif gen_cos_2D_grad:				nom_struct = "Cos_2D"
				nom_sketch_par_couche = ["Sketch_" + nom_struct + str(i + 1) for i in range(nb_couches)]
				nom_pad_par_couche = ["Pad_" + nom_struct + str(i + 1) for i in range(nb_couches)]
				nom_sketch_plateaux = ["Sketch_Plateaux" + str(i + 1) for i in range(nb_couches + 1)]
				nom_pad_plateaux = ["Pad_Plateaux" + str(i + 1) for i in range(nb_couches + 1)]

				# Dimensions de chaques couches
				if dimlat_par_couche_manuel:	# Manuel
					dimlat_y = 0
					for dimlat in dimlat_par_couche:	dimlat_y += dimlat

				else:							# Automatique
					nb_losange_y = 0
					for nb_losange in nb_y_par_couche:	nb_losange_y += nb_losange
					dimlat_par_couche = [nb_y_par_couche[i] / nb_losange_y * dimlat_y for i in range(nb_couches)]

				if gen_losange_grad:
					nom_body = "Body_Losange"
					if optimisation_masse:
						masse, pas_final, ep_finale, porosite = opti_masse(	
								doc,
								nom_body,
								nom_pad_par_couche,
								nom_pad_plateaux,
								nom_sketch_par_couche,
								nom_sketch_plateaux,
								losange_grad,
								file_debug,
								wdebug,
								debug,
								tolerance,
								nb_pas_max,
								[0 for i in range(nb_pas_max + 1)],
								ep,
								0,
								correction_ep_par_pas,
								pourcentage_modification_correction,
								seuil_augmentation_correction,
								seuil_diminution_correction,
								objectif_masse,
								rho,
								volume_max,
								nb_couches,
								nb_y_par_couche,
								dimlat_par_couche,
								ep_par_couche,
								nom_sketch_par_couche,
								nom_pad_par_couche,
								dimlat_x,
								dimlat_ep,
								nb_x_par_couche,
								nom_sketch_plateaux,
								nom_pad_plateaux,
								nom_body,
								plateaux,
								gen_plateaux,
								gen_losange,
								sketch_visible,
								extrude,
								semi_debug,
								debug,
								wdebug)

					else:
						losange_grad(	ep,
										doc,
										file_debug,
										nb_couches,
										nb_y_par_couche,
										dimlat_par_couche,
										ep_par_couche,
										nom_sketch_par_couche,
										nom_pad_par_couche,
										dimlat_x,
										dimlat_ep,
										nb_x_par_couche,
										nom_sketch_plateaux,
										nom_pad_plateaux,
										nom_body,
										plateaux,
										gen_plateaux,
										gen_losange,
										sketch_visible,
										extrude,
										semi_debug,
										debug,
										wdebug)

				elif gen_hex_tri1_2D_aligne_grad:
					nom_body = "Body_Hex_Tri1_2D_Alignes"
					if optimisation_masse:
						masse, pas_final, ep_finale, porosite = opti_masse(	
								doc,
								nom_body,
								nom_pad_par_couche,
								nom_pad_plateaux,
								nom_sketch_par_couche,
								nom_sketch_plateaux,
								gen_hex_tri1_2D_aligne_grad_func,
								file_debug,
								wdebug,
								debug,
								tolerance,
								nb_pas_max,
								[0 for i in range(nb_pas_max + 1)],
								ep,
								0,
								correction_ep_par_pas,
								pourcentage_modification_correction,
								seuil_augmentation_correction,
								seuil_diminution_correction,
								objectif_masse,
								rho,
								volume_max,
								nb_couches,
								nb_x_par_couche,
								nb_y_par_couche,
								alpha_hex_tri1_2D_grad,
								dimlat_x,
								dimlat_par_couche,
								dimlat_ep,
								ep_par_couche,
								plateaux,
								semi_debug,
								debug,
								sketch_visible,
								extrude,
								nom_sketch_par_couche,
								nom_sketch_plateaux,
								nom_body,
								nom_pad_par_couche,
								nom_pad_plateaux,
								gen_plateaux,
								gen_hex_tri1_2D_aligne,
								wdebug)

					else:
						gen_hex_tri1_2D_grad_func(	ep,
													doc,
													file_debug,
													nb_couches,
													nb_x_par_couche,
													nb_y_par_couche,
													alpha_hex_tri1_2D_grad,
													dimlat_x,
													dimlat_par_couche,
													dimlat_ep,
													ep_par_couche,
													plateaux,
													semi_debug,
													debug,
													sketch_visible,
													extrude,
													nom_sketch_par_couche,
													nom_sketch_plateaux,
													nom_body,
													nom_pad_par_couche,
													nom_pad_plateaux,
													gen_plateaux,
													gen_hex_tri1_2D_aligne,
													wdebug)
					
				elif gen_hex_tri1_2D_naligne_grad:
					nom_body = "Body_Hex_Tri1_2D_NAlignes"
					if optimisation_masse:
						masse, pas_final, ep_finale, porosite = opti_masse(	
							doc,
							nom_body,
							nom_pad_par_couche,
							nom_pad_plateaux,
							nom_sketch_par_couche,
							nom_sketch_plateaux,
							gen_hex_tri1_2D_grad_func,
							file_debug,
							wdebug,
							debug,
							tolerance,
							nb_pas_max,
							[0 for i in range(nb_pas_max + 1)],
							ep,
							0,
							correction_ep_par_pas,
							pourcentage_modification_correction,
							seuil_augmentation_correction,
							seuil_diminution_correction,
							objectif_masse,
							rho,
							volume_max,
							nb_couches,
							nb_x_par_couche,
							nb_y_par_couche,
							alpha_hex_tri1_2D_grad,
							dimlat_x,
							dimlat_par_couche,
							dimlat_ep,
							ep_par_couche,
							plateaux,
							semi_debug,
							debug,
							sketch_visible,
							extrude,
							nom_sketch_par_couche,
							nom_sketch_plateaux,
							nom_body,
							nom_pad_par_couche,
							nom_pad_plateaux,
							gen_plateaux,
							gen_hex_tri1_2D_naligne,
							wdebug)

					else:
						gen_hex_tri1_2D_grad_func(	ep,
													doc,
													file_debug,
													nb_couches,
													nb_x_par_couche,
													nb_y_par_couche,
													alpha_hex_tri1_2D_grad,
													dimlat_x,
													dimlat_par_couche,
													dimlat_ep,
													ep_par_couche,
													plateaux,
													semi_debug,
													debug,
													sketch_visible,
													extrude,
													nom_sketch_par_couche,
													nom_sketch_plateaux,
													nom_body,
													nom_pad_par_couche,
													nom_pad_plateaux,
													gen_plateaux,
													gen_hex_tri1_2D_naligne,
													wdebug)

				elif gen_tri_2D_grad:
					nom_body = "Body_Tri"
					if optimisation_masse:
						masse, pas_final, ep_finale, porosite = opti_masse(	
							doc,
							nom_body,
							nom_pad_par_couche,
							nom_pad_plateaux,
							nom_sketch_par_couche,
							nom_sketch_plateaux,
							gen_triangle_grad,
							file_debug,
							wdebug,
							debug,
							tolerance,
							nb_pas_max,
							[0 for i in range(nb_pas_max + 1)],
							ep,
							0,
							correction_ep_par_pas,
							pourcentage_modification_correction,
							seuil_augmentation_correction,
							seuil_diminution_correction,
							objectif_masse,
							rho,
							volume_max,
							nb_couches,
							nb_x_par_couche,
							nb_y_par_couche,
							alpha_tri_2D_grad,
							dimlat_x,
							dimlat_par_couche,
							dimlat_ep,
							ep_par_couche,
							plateaux,
							semi_debug,
							debug,
							sketch_visible,
							extrude,
							nom_sketch_par_couche,
							nom_sketch_plateaux,
							nom_body,
							nom_pad_par_couche,
							nom_pad_plateaux,
							gen_plateaux,
							gen_triangle_basic,
							wdebug)

					else:
						gen_triangle_grad(	ep,
											doc,
											file_debug,
											nb_couches,
											nb_x_par_couche,
											nb_y_par_couche,
											alpha_tri_2D_grad,
											dimlat_x,
											dimlat_par_couche,
											dimlat_ep,
											ep_par_couche,
											plateaux,
											semi_debug,
											debug,
											sketch_visible,
											extrude,
											nom_sketch_par_couche,
											nom_sketch_plateaux,
											nom_body,
											nom_pad_par_couche,
											nom_pad_plateaux,
											gen_plateaux,
											gen_triangle_basic,
											wdebug)

				if gen_cos_2D_grad:
					nom_body = "Body_Cos"
					if optimisation_masse:
						masse, pas_final, ep_finale, porosite = opti_masse(	
								doc,
								nom_body,
								nom_pad_par_couche,
								nom_pad_plateaux,
								nom_sketch_par_couche,
								nom_sketch_plateaux,
								gen_cosinus_grad,
								file_debug,
								wdebug,
								debug,
								tolerance,
								nb_pas_max,
								[0 for i in range(nb_pas_max + 1)],
								ep,
								0,
								correction_ep_par_pas,
								pourcentage_modification_correction,
								seuil_augmentation_correction,
								seuil_diminution_correction,
								objectif_masse,
								rho,
								volume_max,
								nb_couches,
								ep_par_couche,
								nb_x_par_couche,
								nb_y_par_couche,
								amp_grad,
								period_fact_grad,
								phi_grad,
								nbpts_cos_grad,
								plot_math_func,
								cosinus_fct,
								dimlat_x,
								dimlat_par_couche,
								dimlat_ep,
								ep_plateaux,
								semi_debug,
								debug,
								sketch_visible,
								extrude,
								nom_sketch_par_couche,
								nom_sketch_plateaux,
								nom_body,
								nom_pad_par_couche,
								nom_pad_plateaux,
								gen_cosinus,
								True,
								wdebug)

					else:
						gen_cosinus_grad(	ep,
											doc,
											file_debug,nb_couches,
											ep_par_couche,
											nb_x_par_couche,
											nb_y_par_couche,
											amp_grad,
											period_fact_grad,
											phi_grad,
											nbpts_cos_grad,
											plot_math_func,
											cosinus_fct,
											dimlat_x,
											dimlat_par_couche,
											dimlat_ep,
											ep_plateaux,
											semi_debug,
											debug,
											sketch_visible,
											extrude,
											nom_sketch_par_couche,
											nom_sketch_plateaux,
											nom_body,
											nom_pad_par_couche,
											nom_pad_plateaux,
											gen_cosinus,
											True,
											wdebug)

			if optimisation_masse:
				# Affichage du graphe de convergeance
				affichage_calculs_masse(masse, objectif_masse, tolerance, pas_final, ep_finale, porosite)

			# Exportation en stl de la pièce
			export_body(doc, nom_body, export, export_path, export_name, debug, wdebug, file_debug)

			# Fin du programme
			wdebug("\n\n---------------------\n", file_debug)
			wdebug("--- Fin Programme ---\n", file_debug)
			wdebug("---------------------\n", file_debug)

			# Calcul de la durée d'exécution
			temps_fin = time.time()
			duree_exec = temps_fin - temps_debut
			if duree_exec >= 60:	# Conversion en minute si nécessaire
				duree_exec_min = int(duree_exec / 60)
				duree_exec_sec = round(duree_exec % 60, 0)
				wdebug("Temps d'exécution: {0}min {1}s\n".format(duree_exec_min, duree_exec_sec), file_debug)
			else:
				wdebug("Temps d'exécution: {0}s\n".format(round(duree_exec, 0)), file_debug)

			# Fermeture du fichier de déboggage
			if file_debug != None and debug:
				file_debug.close()

		else:
			print("La lecture des paramètres ne s'est pas terminée correctement !")

		return True

	def IsActive(self):
		return True

Gui.addCommand("EXEC", EXEC_Class())