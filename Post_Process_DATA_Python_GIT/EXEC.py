"""
Corps principal
HERMAN Adrien
21/11/2023
"""

# Modules de Python
import matplotlib.pyplot as plt
from statistics import mean

# Modules du Logiciel
from bin.lecture_param import *
from bin.lecture_ecriture_donnees import *
from bin.afficher_data import *
from bin.traitement_data import *

# Lecture des parmaètres du programme
[	type_fichier,
	superposer_courbes,
	nom_fichier,
	nom_dossier,
	calc_temps,
	enregistrer_data,
	nom_enregistrement,
	dossier_enregistrement,
	sppr_rollback,
	recherche_deb_impact,
	deb_impact_manuel,
	tmps_deb_impact,
	tarrage_dep,
	tarrage_tmps,
	detect_fin_essai,
	dep_max,
	calculer_energie,
	fact_force,
	fact_dep,
	taux_augmentation,
	nb_pas_avant_augmentation,
	calc_vitesse_impact,
	nbpts_vitesse_impact,
	afficher_dep_tmps,
	afficher_F_tmps,
	afficher_F_dep,
	afficher_sep] = lecture_param()

tmps_max_vitess_impact = 0.4 	# (ms) Temps maximal avant avertissement pour le calcul de la vitesse d'impact

if not superposer_courbes:	# Si on affiche qu'un seul fichier de données
	if type_fichier == "csv":
		# Lecture du fichier
		lignes = lire_fichier_csv_oscilo(filePath=nom_fichier)
		unite_F, unite_dep, echantillonage, date, heure = lire_en_tete_csv_oscilo(lignes=lignes)

		# Lecture du contenu du fichier
		F, dep = lire_contenu_csv_oscillo(lignes=lignes)

	elif type_fichier == "txt":
		F, dep, tmps, unite_F, unite_dep, echantillonage, date, heure = lire_fichier_txt_python(nom_fichier)

	if F != [] and dep != []:
		# Calcul de temps de l'essai
		if calc_temps and type_fichier != "txt":
			tmps = calc_temps_essai(dep=dep, echantillonage=echantillonage)

		elif type_fichier == "txt":
			print("L'option de calcul du temps de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Suppression du rollback
		if sppr_rollback and type_fichier != "txt":
			F, dep, tmps = suppr_rollback(F=F, dep=dep, tmps=tmps)

		elif type_fichier == "txt":
			print("L'option suppr_rollback n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Recherche du début de l'impact
		if taux_augmentation != None and nb_pas_avant_augmentation != None and recherche_deb_impact and not deb_impact_manuel and type_fichier != "txt":
			F, dep, tmps = recherche_debut_impact(	F=F,
													dep=dep,
													tmps=tmps,
													taux_augmentation=taux_augmentation,
													nb_pas_avant_augmentation=nb_pas_avant_augmentation,
													fileName=nom_fichier)
		elif (nb_pas_avant_augmentation == None or taux_augmentation == None) and recherche_deb_impact and type_fichier != "txt":
			print("La variable taux_augmentation et nb_pas_avant_augmentation doivent-être renseignées dans le fichier de configuration !")

		elif deb_impact_manuel and recherche_deb_impact and type_fichier != "txt":
			print("La recherche de début d'impact manuel ne peut pas être activée en même temps que la recherche d'impact automatique !")

		elif type_fichier == "txt":
			print("La détection du début d'impact automatique n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Début d'impact manuel
		if deb_impact_manuel and calc_temps and type_fichier != "txt":
			F, dep, tmps = debut_impact_manuel(	F=F,
												dep=dep,
												tmps=tmps,
												tmps_deb_impact=tmps_deb_impact)

		elif type_fichier == "txt":
			print("La détection du début d'impact manuel n'est sont pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Tarrage du déplacement et du temps
		if tarrage_dep and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
			dep = tare_dep(dep=dep)

		if tarrage_tmps and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
			tmps = tare_tmps(tmps=tmps)

		elif type_fichier == "txt":
			print("Le tarrage de temps / déplacement n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")
		
		# Suppression des données après la fin de l'impact
		impact_text = ""

		if detect_fin_essai and ((sppr_rollback and recherche_deb_impact and tarrage_dep) or deb_impact_manuel) and type_fichier != "txt":
			F, dep, tmps, impact = fin_essai(F=F, dep=dep, tmps=tmps, dep_max=dep_max)

			if impact:
				impact_text = " / Stop impacteur"
			elif impact == False:
				impact_text = " / Énergie totalement absobée"

		elif (not sppr_rollback or not recherche_deb_impact or not tarrage_dep) and not deb_impact_manuel:
			print("Les paramètres deb_impact_manuel ou sppr_rollback, recherche_deb_impact et tarrage_dep doivent-être activés pour effectuer la détection de fin d'impact !")

		elif type_fichier == "txt":
			print("La détection de la fin de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Calcul de l'énergie
		if calculer_energie:
			energie_impact = energie(F=F, dep=dep, fact_force=fact_force, fact_dep=fact_dep)

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
									heure=heure)

		elif type_fichier == "txt":
			print("L'enregistrement des données traitées ne peut pas être réalisée si ces données proviennent d'un fichier déjà traité (.txt)")

		# Calcul de la vitesse d'impact au début de l'essai
		if calc_vitesse_impact:
			calcul_ok_vimpact = True
			v_pts = []

			for i in range(nbpts_vitesse_impact):
				if len(tmps) > nbpts_vitesse_impact:
					v_pts.append(calc_vitesse(dep1=dep[i], dep2=dep[i+1], tmps1=tmps[i], tmps2=tmps[i+1]))
				else:
					v_pts = [0 for a in range(nbpts_vitesse_impact)]
					calcul_ok_vimpact = False
					break

			vitesse_impact_moyenne = mean(v_pts)

			# Afficher un avertissement si la vitesse d'impact ne peut pas être calculées
			if not calcul_ok_vimpact:
				print("ATTENTION : Le vecteur ne dispose pas d'assez de points pour calculer la vitesse d'impact !")

			else:
				# Afficher un avertissement si la vitesse d'impact est calculée trop loin dans le temps de l'essai
				if tmps[nbpts_vitesse_impact] >= tmps_max_vitess_impact:
					print("ATTENTION : La vitesse d'impact est calculée jusqu'à un temps élevé de l'essai !\n     tmps={0} >= {1}".format(tmps[nbpts_vitesse_impact], tmps_max_vitess_impact))

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
							titre=titre)
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
							fileName=[nom_fichier])
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
							fileName=[nom_fichier])

elif superposer_courbes:	# Si on affiche les fichiers de données d'un dossier
	# Lecture des fichiers
	fichiers = liste_fichier_dossier(path=nom_dossier, fileType="."+type_fichier)
	nb_fichiers = len(fichiers)

	if type_fichier == "csv":
		lignes = [lire_fichier_csv_oscilo(filePath=nom_dossier + f) for f in fichiers]
		en_tetes = [lire_en_tete_csv_oscilo(lignes=l) for l in lignes]

		# Lecture des contenus des fichiers
		F = [lire_contenu_csv_oscillo(lignes=l)[0] for l in lignes]
		dep = [lire_contenu_csv_oscillo(lignes=l)[1] for l in lignes]
	
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
			F[i], dep[i], tmps[i], unite_F[i], unite_dep[i], echantillonage[i], date[i], heure[i] = lire_fichier_txt_python(nom_dossier + fichiers[i])

		en_tetes = [unite_F, unite_dep, echantillonage, date, heure]

	if type_fichier != None and nb_fichiers != 0:
		# Calcul des temps des essais
		if calc_temps and type_fichier != "txt":
			tmps = [calc_temps_essai(dep=dep[i], echantillonage=en_tetes[i][2]) for i in range(len(dep))]

		elif type_fichier == "txt":
			print("L'option de calcul du temps de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Suppression du rollback
		if sppr_rollback and type_fichier != "txt":
			for i in range(len(F)):	F[i], dep[i], tmps[i] = suppr_rollback(F=F[i], dep=dep[i], tmps=tmps[i])

		elif type_fichier == "txt":
			print("L'option suppr_rollback n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Recherche du début de l'impact
		if taux_augmentation != None and nb_pas_avant_augmentation != None and recherche_deb_impact and not deb_impact_manuel and type_fichier != "txt":
			for i in range(len(F)):
				F[i], dep[i], tmps[i] = recherche_debut_impact(	F=F[i],
																dep=dep[i],
																tmps=tmps[i],
																taux_augmentation=taux_augmentation,
																nb_pas_avant_augmentation=nb_pas_avant_augmentation,
																fileName=fichiers[i])
		elif (nb_pas_avant_augmentation == None or taux_augmentation == None) and recherche_deb_impact and type_fichier != "txt":
			print("La vairiable taux_augmentation et nb_pas_avant_augmentation doivent-être renseignées dans le fichier de configuration !")

		elif deb_impact_manuel and recherche_deb_impact and type_fichier != "txt":
			print("La recherche de début d'impact manuel ne peut pas être activée en même temps que la recherche d'impact automatique !")

		elif type_fichier == "txt":
			print("La détection du début d'impact automatique n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Début d'impact manuel
		if deb_impact_manuel and calc_temps and type_fichier != "txt":
			for i in range(len(F)):
				F[i], dep[i], tmps[i] = debut_impact_manuel(F=F[i],
															dep=dep[i],
															tmps=tmps[i],
															tmps_deb_impact=tmps_deb_impact)

		elif type_fichier == "txt":
			print("La détection du début d'impact manuel n'est sont pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Tarrage du déplacement et du temps
		if tarrage_dep and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
			dep = [tare_dep(dep=d) for d in dep]
		
		if tarrage_tmps and (recherche_deb_impact or deb_impact_manuel) and type_fichier != "txt":
			tmps = [tare_tmps(tmps=t) for t in tmps]

		elif type_fichier == "txt":
			print("Le tarrage de temps / déplacement n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Suppression des données après la fin de l'impact
		impact_text = ""

		if detect_fin_essai and ((sppr_rollback and recherche_deb_impact and tarrage_dep) or deb_impact_manuel) and type_fichier != "txt":
			impact = [True for i in range(len(F))]
			for i in range(len(F)):
				F[i], dep[i], tmps[i], impact[i] = fin_essai(	F=F[i],
																dep=dep[i],
																tmps=tmps[i],
																dep_max=dep_max)
			
			if True in impact and False in impact:
				impact_text = " / " + str(impact.count(True)) + " stop impacteur & " + str(impact.count(False)) + " totalement absobées"
			elif True in impact:
				impact_text = " / Stop impacteur"
			else:
				impact_text = " / Énergie totalement absobée"

		elif (not sppr_rollback or not recherche_deb_impact or not tarrage_dep) and not deb_impact_manuel:
			print("Les paramètres deb_impact_manuel ou sppr_rollback, recherche_deb_impact et tarrage_dep doivent-être activés pour effectuer la détection de fin d'impact !")

		elif type_fichier == "txt":
			print("La détection de la fin de l'essai n'est pas disponnible sur des données déjà traitées (prevenant d'un fichier .txt)")

		# Calcul de l'énergie de chaque courbes
		if calculer_energie:
			energie_impact = [energie(	F=F[i],
										dep=dep[i],
										fact_force=fact_force,
										fact_dep=fact_dep) for i in range(len(F))]
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
									filePath=dossier_enregistrement + fichiers_enregistrement[i] + ".txt",
									unite_F=en_tetes[i][0],
									unite_dep=en_tetes[i][1],
									echantillonage=en_tetes[i][2],
									date=en_tetes[i][3],
									heure=en_tetes[i][4])

		# Calcul de la vitesse d'impact au début de l'essai
		if calc_vitesse_impact:
			vitesse_impact_moyenne_tab = []
			calcul_ok_vimpact = True

			for j in range(nb_fichiers):
				v_pts = []

				for i in range(nbpts_vitesse_impact):
					if len(tmps[j]) > nbpts_vitesse_impact:
						v_pts.append(calc_vitesse(dep1=dep[j][i], dep2=dep[j][i+1], tmps1=tmps[j][i], tmps2=tmps[j][i+1]))
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
				print("ATTENTION : L'un des vecteurs ne dispose pas d'assez de points pour calculer la vitesse d'impact !")
			
			else:
				# Afficher un avertissement si la vitesse d'impact est calculée trop loin dans le temps de l'essai
				if calcul_ok_vimpact:
					for j in range(nb_fichiers):
						if tmps[j][nbpts_vitesse_impact] >= tmps_max_vitess_impact:
							print("ATTENTION : La vitesse d'impact est calculée jusqu'à un temps élevé de l'essai !\n     tmps={0} >= {1}".format(tmps[j][nbpts_vitesse_impact], tmps_max_vitess_impact))

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
							titre=titre)

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
							fileName=fichiers)

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
							fileName=fichiers)
				
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

except:
	print("Impossible de redimensionner et/ou d'afficher le graphique !")