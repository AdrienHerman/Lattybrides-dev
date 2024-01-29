"""
Fonction contenant toute la suite d'instruction
pour le traitement des données expérimentales.
29/01/2024
HERMAN Adrien
"""

# Modules de Python
import matplotlib.pyplot as plt
from statistics import mean

# Modules du Logiciel
from bin.lecture_param import *
from bin.lecture_ecriture_donnees import *
from bin.afficher_data import *
from bin.traitement_data import *
from bin.errors import *

def exec_traitement(QWindow=None,
					superposer_courbes=False,
					nom_fichier="",
					nom_dossier="",
					type_fichier="CSV",
					calc_temps=True,
					enregistrer_data=False,
					nom_enregistrement="",
					dossier_enregistrement="",
					sppr_rollback=True,
					recherche_deb_impact=True,
					taux_augmentation=0.9,
					nb_pas_avant_augmentation=1,
					deb_impact_manuel=False,
					tmps_deb_impact=200.0,
					tarrage_dep=True,
					tarrage_tmps=True,
					detect_fin_essai=True,
					dep_max=19.73,
					calculer_energie=True,
					fact_force=1,
					fact_dep=1e-3,
					calc_vitesse_impact=False,
					nbpts_vitesse_impact=3,
					afficher_dep_tmps=True,
					afficher_F_tmps=True,
					afficher_F_dep=True,
					afficher_sep=False,
					tmps_max_vitess_impact=0.4):
	"""
	Exécution du traitement des données.

	-----------
	Variables :
		- QWindow                : Objet fenêtre.
		- conf                   : Voir le fichier config_default.conf.
		- tmps_max_vitess_impact : Temps maximal (ms) avant avertissement pour le calcul de la vitesse d'impact
	-----------

	---------
	Retours :
		- bool : True si l'opération a réussie sinon False
	---------
	"""

	if not superposer_courbes:	# Si on affiche qu'un seul fichier de données
		# Lecture des fichiers
		fichiers = liste_fichier_dossier(path=nom_dossier + "/", fileType="."+type_fichier, QWindow=QWindow)

		if not nom_fichier in fichiers:
			print_or_addterminal_message(	QWindow=QWindow,
											type_msg="err",
											text="exec_traitement ERREUR : Le fichier sélectionné n'existe pas ou le type de fichier associé n'est pas correct !")

			return False

		else:
			if type_fichier == "csv":
				# Lecture du fichier
				lignes = lire_fichier_csv_oscilo(filePath=nom_dossier + "/" + nom_fichier, QWindow=QWindow)
				unite_F, unite_dep, echantillonage, date, heure = lire_en_tete_csv_oscilo(lignes=lignes)

				# Lecture du contenu du fichier
				F, dep = lire_contenu_csv_oscillo(lignes=lignes, QWindow=QWindow)

			elif type_fichier == "txt":
				F, dep, tmps, unite_F, unite_dep, echantillonage, date, heure = lire_fichier_txt_python(nom_fichier)

			if F != [] and dep != []:
				# Calcul de temps de l'essai
				if calc_temps and type_fichier != "txt":
					tmps = calc_temps_essai(dep=dep, echantillonage=echantillonage, QWindow=QWindow)

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : L'option de calcul du temps de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Suppression du rollback
				if sppr_rollback and type_fichier != "txt":
					F, dep, tmps = suppr_rollback(F=F, dep=dep, tmps=tmps, QWindow=QWindow)

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : L'option sppr_rollback n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Recherche du début de l'impact
				if taux_augmentation != None and nb_pas_avant_augmentation != None and recherche_deb_impact and not deb_impact_manuel and type_fichier != "txt":
					F, dep, tmps = recherche_debut_impact(	F=F,
															dep=dep,
															tmps=tmps,
															taux_augmentation=taux_augmentation,
															nb_pas_avant_augmentation=nb_pas_avant_augmentation,
															fileName=nom_fichier,
															QWindow=QWindow)
				elif (nb_pas_avant_augmentation == None or taux_augmentation == None) and recherche_deb_impact and type_fichier != "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="err",
													text="exec_traitement La variable taux_augmentation et nb_pas_avant_augmentation doivent-être renseignées dans le fichier de configuration !")
					return False

				elif deb_impact_manuel and recherche_deb_impact and type_fichier != "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="err",
													text="exec_traitement La recherche de début d'impact manuel ne peut pas être activée en même temps que la recherche d'impact automatique !")
					return False

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : La détection du début d'impact automatique n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Début d'impact manuel
				if deb_impact_manuel and calc_temps and type_fichier != "txt":
					F, dep, tmps = debut_impact_manuel(	F=F,
														dep=dep,
														tmps=tmps,
														tmps_deb_impact=tmps_deb_impact,
														QWindow=QWindow)

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : La détection du début d'impact manuel n'est sont pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Tarrage du déplacement et du temps
				if tarrage_dep and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
					dep = tare_dep(dep=dep, QWindow=QWindow)

				if tarrage_tmps and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
					tmps = tare_tmps(tmps=tmps, QWindow=QWindow)

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : Le tarrage de temps / déplacement n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")
				
				# Suppression des données après la fin de l'impact
				impact_text = ""

				if detect_fin_essai and ((sppr_rollback and recherche_deb_impact and tarrage_dep) or deb_impact_manuel) and type_fichier != "txt":
					F, dep, tmps, impact = fin_essai(F=F, dep=dep, tmps=tmps, dep_max=dep_max, QWindow=QWindow)

					if impact:
						impact_text = " / Stop impacteur"
					elif impact == False:
						impact_text = " / Énergie totalement absorbée"

				elif (not sppr_rollback or not recherche_deb_impact or not tarrage_dep) and not deb_impact_manuel:
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="err",
													text="exec_traitement Les paramètres deb_impact_manuel ou sppr_rollback, recherche_deb_impact et tarrage_dep doivent-être activés pour effectuer la détection de fin d'impact !")
					return False

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : La détection de la fin de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Calcul de l'énergie
				if calculer_energie:
					energie_impact = energie(F=F, dep=dep, fact_force=fact_force, fact_dep=fact_dep, QWindow=QWindow)

				# Enregistrement des données traitées
				if enregistrer_data and type_fichier != "txt":
					enregistrer_donnees(	F=F,
											dep=dep,
											tmps=tmps,
											calc_temps=calc_temps,
											filePath=dossier_enregistrement + nom_enregistrement + ".txt",
											unite_F=unite_F,
											unite_dep=unite_dep,
											echantillonage=echantillonage,
											date=date,
											heure=heure,
											QWindow=QWindow)

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : L'enregistrement des données traitées ne peut pas être réalisée si ces données proviennent d'un fichier déjà traité (.txt)")

				# Calcul de la vitesse d'impact au début de l'essai
				if calc_vitesse_impact:
					calcul_ok_vimpact = True
					v_pts = []

					for i in range(nbpts_vitesse_impact):
						if len(tmps) > nbpts_vitesse_impact:
							v_pts.append(calc_vitesse(dep1=dep[i], dep2=dep[i+1], tmps1=tmps[i], tmps2=tmps[i+1], QWindow=QWindow))
						else:
							v_pts = [0 for a in range(nbpts_vitesse_impact)]
							calcul_ok_vimpact = False
							break

					vitesse_impact_moyenne = mean(v_pts)

					# Afficher un avertissement si la vitesse d'impact ne peut pas être calculées
					if not calcul_ok_vimpact:
						print_or_addterminal_message(	QWindow=QWindow,
														type_msg="wrg",
														text="exec_traitement WARNING : Le vecteur ne dispose pas d'assez de points pour calculer la vitesse d'impact !")

					else:
						# Afficher un avertissement si la vitesse d'impact est calculée trop loin dans le temps de l'essai
						if tmps[nbpts_vitesse_impact] >= tmps_max_vitess_impact:
							print_or_addterminal_message(	QWindow=QWindow,
															type_msg="wrg",
															text="exec_traitement WARNING : La vitesse d'impact est calculée jusqu'à un temps élevé de l'essai !\n     tmps={0} >= {1}".format(tmps[nbpts_vitesse_impact], tmps_max_vitess_impact))

					# Création des trois graphes dans une figure
					if afficher_sep:
						figs = [0, 0, 0]
						axs = [0, 0, 0]

						for i in range([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True)):
							figs[i], axs[i] = plt.subplots()

					elif not afficher_sep and [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) > 0:
						fig, axs = plt.subplots([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True), 1)

					if afficher_sep != None:
						i = 0

						if afficher_dep_tmps:
							if afficher_sep:
								fig = figs[i]
								ax = axs[i]
							else:
								if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
									ax = axs
								else:
									ax = axs[i]

							# Titre du graphique
							titre = ""
							
							if calculer_energie:
								titre = "Énergie Calculée = " + str(round(energie_impact, 2)) + " J" + impact_text

							if calc_vitesse_impact:
								if titre != "":	titre += " / "

								if not calcul_ok_vimpact:
									titre += "Vitesse d'Impact = NON CALCULABLE !"
								else:
									titre += "Vitesse Impact = " + str(round(vitesse_impact_moyenne, 2)) + "m/s"

							graphe(	data_x=[tmps],
									data_y=[dep],
									fig=fig,
									ax=ax,
									label_x="Temps (ms)",
									label_y="Déplacement ({0})".format(unite_dep),
									fileName=[nom_fichier],
									titre=titre,
									QWindow=QWindow)
							i += 1

						if afficher_F_tmps:
							if afficher_sep:
								fig = figs[i]
								ax = axs[i]
							else:
								if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
									ax = axs
								else:
									ax = axs[i]

							titre = ""

							if (afficher_dep_tmps == None or not afficher_dep_tmps) or afficher_sep:
								# Titre du graphique
								titre = ""
								
								if calculer_energie:
									titre = "Énergie Calculée = " + str(round(energie_impact, 2)) + " J" + impact_text

								if calc_vitesse_impact:
									if titre != "":	titre += " / "

								if not calcul_ok_vimpact:
									titre += "Vitesse d'Impact = NON CALCULABLE !"
								else:
									titre += "Vitesse Impact = " + str(round(vitesse_impact_moyenne, 2)) + "m/s"

							graphe(	data_x=[tmps],
									data_y=[F],
									label_x="Temps (ms)",
									label_y="Force ({0})".format(unite_F),
									titre=titre,
									fig=fig,
									ax=ax,
									fileName=[nom_fichier],
									QWindow=QWindow)
							i += 1

						if afficher_F_dep:
							if afficher_sep:
								fig = figs[i]
								ax = axs[i]
							else:
								if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
									ax = axs
								else:
									ax = axs[i]

							titre = ""

							if ((afficher_dep_tmps == None or not afficher_dep_tmps) and (afficher_F_tmps == None or not afficher_F_tmps)) or afficher_sep:
								# Titre du graphique
								titre = ""
								
								if calculer_energie:
									titre = "Énergie Calculée = " + str(round(energie_impact, 2)) + " J" + impact_text

								if calc_vitesse_impact:
									if titre != "":	titre += " / "

								if not calcul_ok_vimpact:
									titre += "Vitesse d'Impact = NON CALCULABLE !"
								else:
									titre += "Vitesse Impact = " + str(round(vitesse_impact_moyenne, 2)) + "m/s"

							graphe(	data_x=[dep],
									data_y=[F],
									label_x="Déplacement ({0})".format(unite_dep),
									label_y="Force ({0})".format(unite_F),
									titre=titre,
									fig=fig,
									ax=ax,
									fileName=[nom_fichier],
									QWindow=QWindow)

	elif superposer_courbes:	# Si on affiche les fichiers de données d'un dossier
		# Lecture des fichiers
		fichiers = liste_fichier_dossier(path=nom_dossier, fileType="."+type_fichier, QWindow=QWindow)
		nb_fichiers = len(fichiers)

		if nb_fichiers <= 1:
			print_or_addterminal_message(	QWindow=QWindow,
											type_msg="err",
											text="exec_traitement ERREUR : Il n'y a pas assez de fichiers pour superposer les courbes !")
			return False

		else:
			if type_fichier == "csv":
				lignes = [lire_fichier_csv_oscilo(filePath=nom_dossier + "/" + f, QWindow=QWindow) for f in fichiers]
				for l in lignes:
					if len(l) == 0:
						print_or_addterminal_message(	QWindow=QWindow,
														type_msg="err",
														text="exec_traitement ERREUR : Le fichier lu est vide !")
						return False
				
				en_tetes = [lire_en_tete_csv_oscilo(lignes=l, QWindow=QWindow) for l in lignes]

				# Lecture des contenus des fichiers
				F = [lire_contenu_csv_oscillo(lignes=l, QWindow=QWindow)[0] for l in lignes]
				dep = [lire_contenu_csv_oscillo(lignes=l, QWindow=QWindow)[1] for l in lignes]
			
			elif type_fichier == "txt":
				F = [None for i in range(nb_fichiers)]
				dep = [None for i in range(nb_fichiers)]
				tmps = [None for i in range(nb_fichiers)]
				unite_F = [None for i in range(nb_fichiers)]
				unite_dep = [None for i in range(nb_fichiers)]
				echantillonage = [None for i in range(nb_fichiers)]
				date = [None for i in range(nb_fichiers)]
				heure = [None for i in range(nb_fichiers)]

				for i in range(nb_fichiers):
					F[i], dep[i], tmps[i], unite_F[i], unite_dep[i], echantillonage[i], date[i], heure[i] = lire_fichier_txt_python(nom_dossier + "/" + fichiers[i], QWindow=QWindow)
					if F[i] == [] and dep[i] == [] and tmps[i] == [] and unite_F[i] == "" and unite_dep[i] == "" and echantillonage[i] == .0 and date[i] == "" and heure[i] == "":
						print_or_addterminal_message(	QWindow=QWindow,
														type_msg="err",
														text="exec_traitement ERREUR : Le fichier lu est vide !")
						return False

				en_tetes = [[unite_F[i], unite_dep[i], echantillonage[i], date[i], heure[i]] for i in range(nb_fichiers)]

			if type_fichier != None and nb_fichiers != 0:
				# Calcul des temps des essais
				if calc_temps and type_fichier != "txt":
					tmps = [calc_temps_essai(dep=dep[i], echantillonage=en_tetes[i][2], QWindow=QWindow) for i in range(len(dep))]

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : L'option de calcul du temps de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Suppression du rollback
				if sppr_rollback and type_fichier != "txt":
					for i in range(len(F)):	F[i], dep[i], tmps[i] = suppr_rollback(F=F[i], dep=dep[i], tmps=tmps[i], QWindow=QWindow)

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : L'option suppr_rollback n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Recherche du début de l'impact
				if taux_augmentation != None and nb_pas_avant_augmentation != None and recherche_deb_impact and not deb_impact_manuel and type_fichier != "txt":
					for i in range(len(F)):
						F[i], dep[i], tmps[i] = recherche_debut_impact(	F=F[i],
																		dep=dep[i],
																		tmps=tmps[i],
																		taux_augmentation=taux_augmentation,
																		nb_pas_avant_augmentation=nb_pas_avant_augmentation,
																		fileName=fichiers[i],
																		QWindow=QWindow)

				elif (nb_pas_avant_augmentation == None or taux_augmentation == None) and recherche_deb_impact and type_fichier != "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="err",
													text="exec_traitement ERREUR : La variable taux_augmentation et nb_pas_avant_augmentation doivent-être renseignées dans le fichier de configuration !")
					return False

				elif deb_impact_manuel and recherche_deb_impact and type_fichier != "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="err",
													text="exec_traitement ERREUR : La recherche de début d'impact manuel ne peut pas être activée en même temps que la recherche d'impact automatique !")
					return False

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : La détection du début d'impact automatique n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Début d'impact manuel
				if deb_impact_manuel and calc_temps and type_fichier != "txt":
					for i in range(len(F)):
						F[i], dep[i], tmps[i] = debut_impact_manuel(F=F[i],
																	dep=dep[i],
																	tmps=tmps[i],
																	tmps_deb_impact=tmps_deb_impact,
																	QWindow=QWindow)

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : La détection du début d'impact manuel n'est sont pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Tarrage du déplacement et du temps
				if tarrage_dep and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
					dep = [tare_dep(dep=d, QWindow=QWindow) for d in dep]
				
				if tarrage_tmps and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
					tmps = [tare_tmps(tmps=t, QWindow=QWindow) for t in tmps]

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : Le tarrage de temps / déplacement n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Suppression des données après la fin de l'impact
				impact_text = ""

				if detect_fin_essai and ((sppr_rollback and recherche_deb_impact and tarrage_dep) or deb_impact_manuel) and type_fichier != "txt":
					impact = [True for i in range(len(F))]
					for i in range(len(F)):
						F[i], dep[i], tmps[i], impact[i] = fin_essai(	F=F[i],
																		dep=dep[i],
																		tmps=tmps[i],
																		dep_max=dep_max,
																		QWindow=QWindow)
					
					if True in impact and False in impact:
						impact_text = " / " + str(impact.count(True)) + " stop impacteur & " + str(impact.count(False)) + " totalement absobées"
					elif True in impact:
						impact_text = " / Stop impacteur"
					else:
						impact_text = " / Énergie totalement absorbée"

				elif (not sppr_rollback or not recherche_deb_impact or not tarrage_dep) and not deb_impact_manuel:
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="err",
													text="exec_traitement ERREUR : Les paramètres deb_impact_manuel ou sppr_rollback, recherche_deb_impact et tarrage_dep doivent-être activés pour effectuer la détection de fin d'impact !")
					return False

				elif type_fichier == "txt":
					print_or_addterminal_message(	QWindow=QWindow,
													type_msg="wrg",
													text="exec_traitement WARNING : La détection de la fin de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

				# Calcul de l'énergie de chaque courbes
				if calculer_energie:
					energie_impact = [energie(	F=F[i],
												dep=dep[i],
												fact_force=fact_force,
												fact_dep=fact_dep,
												QWindow=QWindow) for i in range(len(F))]
					energie_moyenne = 0
					for e in energie_impact:	energie_moyenne += e
					energie_moyenne /= len(energie_impact)

				# Enregistrement des données traitées
				if enregistrer_data and type_fichier != "txt":
					fichiers_enregistrement = []
					for i in range(len(fichiers)):
						fichiers_enregistrement.append(fichiers[i].split(".")[0])

					for i in range(len(F)):
						enregistrer_donnees(F=F[i],
											dep=dep[i],
											tmps=tmps[i],
											calc_temps=calc_temps,
											filePath=dossier_enregistrement + "/" + fichiers_enregistrement[i] + ".txt",
											unite_F=en_tetes[i][0],
											unite_dep=en_tetes[i][1],
											echantillonage=en_tetes[i][2],
											date=en_tetes[i][3],
											heure=en_tetes[i][4],
											QWindow=QWindow)

				# Calcul de la vitesse d'impact au début de l'essai
				if calc_vitesse_impact:
					vitesse_impact_moyenne_tab = []
					calcul_ok_vimpact = True

					for j in range(nb_fichiers):
						v_pts = []

						for i in range(nbpts_vitesse_impact):
							if len(tmps[j]) > nbpts_vitesse_impact:
								v_pts.append(calc_vitesse(dep1=dep[j][i], dep2=dep[j][i+1], tmps1=tmps[j][i], tmps2=tmps[j][i+1], QWindow=QWindow))
							else:
								v_pts = [0 for a in range(nbpts_vitesse_impact)]
								calcul_ok_vimpact = False
								break

						if calcul_ok_vimpact:
							vitesse_impact_moyenne_tab.append(mean(v_pts))
						else:
							vitesse_impact_moyenne_tab.append(0)
							break

					vitesse_impact_moyenne = mean(vitesse_impact_moyenne_tab)

					# Afficher un avertissement si la vitesse d'impact ne peut pas être calculées
					if not calcul_ok_vimpact:
						print_or_addterminal_message(	QWindow=QWindow,
														type_msg="wrg",
														text="exec_traitement WARNING : L'un des vecteurs ne dispose pas d'assez de points pour calculer la vitesse d'impact !")
					
					else:
						# Afficher un avertissement si la vitesse d'impact est calculée trop loin dans le temps de l'essai
						if calcul_ok_vimpact:
							for j in range(nb_fichiers):
								if tmps[j][nbpts_vitesse_impact] >= tmps_max_vitess_impact:
									print_or_addterminal_message(	QWindow=QWindow,
																	type_msg="wrg",
																	text="exec_traitement WARNING : La vitesse d'impact est calculée jusqu'à un temps élevé de l'essai !\n     tmps={0} >= {1}".format(tmps[j][nbpts_vitesse_impact], tmps_max_vitess_impact))

					# Création des trois graphes dans une figure
					if afficher_sep:
						figs = [0, 0, 0]
						axs = [0, 0, 0]

						for i in range([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True)):
							figs[i], axs[i] = plt.subplots()

					elif not afficher_sep and [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) > 0:
						fig, axs = plt.subplots([afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True), 1)
					
					if afficher_sep != None:
						i = 0
						j = 0

						if afficher_dep_tmps:
							# Titre du graphique
							titre = ""
							
							if calculer_energie:
								titre = "Énergie Calculée = " + str(round(energie_moyenne, 2)) + " J" + impact_text

							if calc_vitesse_impact:
								if titre != "":	titre += " / "

								if not calcul_ok_vimpact:
									titre += "Vitesse d'Impact = NON CALCULABLE !"
								else:
									titre += "Vitesse Impact = " + str(round(vitesse_impact_moyenne, 2)) + "m/s"

							if afficher_sep:
								fig = figs[i]
								ax = axs[i]

							else:
								if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
									ax = axs
								else:
									ax = axs[i]

							graphe(	data_x=tmps,
									data_y=dep,
									fig=fig,
									ax=ax,
									label_x="Temps (ms)",
									label_y="Déplacement ({0})".format(en_tetes[j][1]),
									fileName=fichiers,
									titre=titre,
									QWindow=QWindow)

							i += 1

						if afficher_F_tmps:
							titre = ""

							if not afficher_dep_tmps or afficher_sep:
								# Titre du graphique
								titre = ""
								
								if calculer_energie:
									titre = "Énergie Calculée = " + str(round(energie_moyenne, 2)) + " J" + impact_text

								if calc_vitesse_impact:
									if titre != "":	titre += " / "

									if not calcul_ok_vimpact:
										titre += "Vitesse d'Impact = NON CALCULABLE !"
									else:
										titre += "Vitesse Impact = " + str(round(vitesse_impact_moyenne, 2)) + "m/s"
							else:
								titre = ""

							if afficher_sep:
								fig = figs[i]
								ax = axs[i]
							else:
								if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
									ax = axs
								else:
									ax = axs[i]

							graphe(	data_x=tmps,
									data_y=F,
									label_x="Temps (ms)",
									label_y="Force ({0})".format(en_tetes[j][0]),
									titre=titre,
									fig=fig,
									ax=ax,
									fileName=fichiers,
									QWindow=QWindow,)

							i += 1

						if afficher_F_dep:
							titre = ""

							if not afficher_dep_tmps and not afficher_F_tmps or afficher_sep:
								# Titre du graphique
								titre = ""
								
								if calculer_energie:
									titre = "Énergie Calculée = " + str(round(energie_moyenne, 2)) + " J" + impact_text

								if calc_vitesse_impact:
									if titre != "":	titre += " / "

									if not calcul_ok_vimpact:
										titre += "Vitesse d'Impact = NON CALCULABLE !"
									else:
										titre += "Vitesse Impact = " + str(round(vitesse_impact_moyenne, 2)) + "m/s"
							else:
								titre = ""

							if afficher_sep:
								fig = figs[i]
								ax = axs[i]
							else:
								if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
									ax = axs
								else:
									ax = axs[i]

							graphe(	data_x=dep,
									data_y=F,
									label_x="Déplacement ({0})".format(en_tetes[j][1]),
									label_y="Force ({0})".format(en_tetes[j][0]),
									titre=titre,
									fig=fig,
									ax=ax,
									fileName=fichiers,
									QWindow=QWindow)
						
						j += 1

	try:
		if afficher_sep != None:
			i = 0

			if afficher_dep_tmps:
				if afficher_sep:
					fig = figs[i]
					ax = axs[i]
				else:
					if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
						ax = axs
					else:
						ax = axs[i]

				fig.set_figheight(6)
				fig.set_figwidth(10)

				i += 1

			if afficher_F_tmps:
				if afficher_sep:
					fig = figs[i]
					ax = axs[i]
				else:
					if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
						ax = axs
					else:
						ax = axs[i]

				fig.set_figheight(6)
				fig.set_figwidth(10)

				i += 1

			if afficher_F_dep:
				if afficher_sep:
					fig = figs[i]
					ax = axs[i]
				else:
					if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) == 1:
						ax = axs
					else:
						ax = axs[i]

				fig.set_figheight(6)
				fig.set_figwidth(10)

		if [afficher_dep_tmps, afficher_F_dep, afficher_F_tmps].count(True) != 0:
			plt.subplots_adjust(left=0.075, right=0.975, top=0.94, bottom=0.08, hspace=0.36, wspace=0.2)
			plt.show()

		return True

	except:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="err",
										text="exec_traitement ERREUR : Impossible de redimensionner et/ou d'afficher le graphique !")
		return False