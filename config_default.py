#:NE PAS EFFACER LES COMMENTAIRES
#:Tous les paramètres doivent être séparés par : au début et à
#:la fin de la chaîne de caractères sans espaces
#:Le fichier de configuration config.txt ne doit pas être déplacé ou supprimé
#:Les noms de variables ne doivent pas être modifiés.
#:
#:--------------------------------------
#: --- PARTIE METHODE DE GENERATION ---
#:
#: ** Dans cette partie, vous allez sélectionner la méthode à utiliser
#: ** pour générer une structure lattice. Les méthodes "basic" sont celles
#: ** où la structure lattice est brute (sans gradients). Les méthodes "grad"
#: ** quant à elles sont avec gradients (d'épaisseur ou de forme).
#:
#: ** ATTENTION : SEULEMENT UNE MÉTHODE NE DOIT ÊTRE SÉLECTIONNÉE
#:
#: /// OPTIMISATION DE LA MASSE \\\
#: ** Si optimisation_masse = True, l'optimisation de la masse est réalisée
#: ** et les variables objectif_masse, tolerance, nb_pas_max,
#: ** correction_ep_par_pas, pourcentage_modification_correction,
#: ** seuil_augmentation_correction, seuil_diminution_correction, rho
#: ** doivent-être renseignées
optimisation_masse:True:
#: ** Objectif de masse à atteindre avant l'arrêt des calculs (en g)
objectif_masse:18:
#: ** Tolérance sur l'objectif de masse
#: ** (objectif masse - tolérance >= masse calculée >= objectif masse + tolérance)
tolerance:1e-1:
#: ** Nombre d'itération maximale avant l'arrêt des calculs même si l'objectif
#: ** de masse n'est pas atteint
nb_pas_max:3:
#: ** Valeur de correction de l'épaisseur des parois à chaque pas
#: ** (augmentation ou diminution en mm)
correction_ep_par_pas:7e-3:
#: ** Pourcentage de modification de la variable correction_ep_par_pas utilisé
#: ** si la convergence est trop lente / rapide
pourcentage_modification_correction:0.05:
#: ** Seuil à partir duquel correction_ep_par_pas est augmenté / diminuer
#: METTRE FORMULE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
seuil_augmentation_correction:0.2:
seuil_diminution_correction:0.2:
#: ** Masse volumique du matériau utilisé pour l'impression (en g/cm^3)
rho:1.24:
#:
#: /// GÉNÉRATION DE STRUCTURES \\\
#: Structure à base de losanges : No1
gen_losange_basic:False:
gen_losange_grad:False:
#:
#: Structure à base d'hexagones et de triangles alignés : No2
gen_hex_tri1_2D_aligne_basic:False:
gen_hex_tri1_2D_aligne_grad:False:
#:
#: Structure à base d'hexagones et de triangles non alignés  : No3
gen_hex_tri1_2D_naligne_basic:False:
gen_hex_tri1_2D_naligne_grad:False:
#:
#: Structure à base de triangles : No4
gen_tri_2D_basic:False:
gen_tri_2D_grad:False:
#:
#: Structure à base de cosinus : No5
gen_cos_2D_basic:False:
gen_cos_2D_grad:True:
#:--------------------------------------
#:
#:-----------------------------------------
#: --- PARTIE GÉOMÉTRIE DES STRUCTURES ---
#: L'ensemble des valeurs ci-dessous sont exprimées en millimètre
#:
#: /// PLATEAUX LIANTS EXTREMITEES \\\
#: ** Les plateaux liants sont des pavés aux éxtrémités de la structures
#: ** qui ont pour but de lier les motifs pour homogénéiser la répartition
#: ** de la force d'impact.
#: ** Si generation_plateaux_extremitees = True les plateaux seront générés et 
#: ** ep_plateaux_dessous et ep_plateaux_dessus doivent être renseignés
generation_plateaux_extremitees:True:
#:
#: ** Choix de l'épaisseur des plateaux liant les extrémité de la structure (mm)
ep_plateau_dessous:0.4:
ep_plateau_dessus:0.4:
#:
#:
#: /// PROPRIÉTÉS GÉOMÉTRIQUES COMMUNES \\\
#: ** Choix de l'épaisseur des parois
#: ** Entrer un nombre réel positif
ep:0.6:
#:
#: ** Choix de l'épaisseur d'extrusion du modèle
#: ** Entrer un nombre réel positif
dimlat_ep:40:
#:
#: ** Choix du nombre de la longueur du modèle l'axe x et sur l'axe y
#: ** Entrer un nombre réel positif
dimlat_x:40:
dimlat_y:40:
#:
#:
#: /// GÉNÉRATION DE MOTIFS SANS GRADIENT \\\
#: ** Choix du nombre de losange sur l'axe x et sur l'axe y
#: ** Entrer un nombre entier
nb_motif_x_sg:8:
nb_motif_y_sg:4:
#:
#:
#: /// GÉNÉRATION DE MOTIFS AVEC GRADIENT \\\
#: ** Choix du nombre de losanges en y par couches
#: ** Les nombre de losanges doivent-être séparés par une ,
#: ** ATTENTION : Il ne doit pas il y avoir un espace !
nb_y_par_couche:4,3:
#:
#: ** Choix du nombre de losanges en x par couches
#: ** ATTENTION : Il doit il y avoir le même nombre de valeur que nb_y_par_couche
nb_x_par_couche:5,5:
#:
#: ** Épaisseur des couches (en y)
#: ** Si dimlat_par_couche_manuel = False, les dimensions des couches
#: ** Son choisies automatiquement au prorata du nombre de losanges y
#: ** par couche en fonction de la variable dimlat_y
#: ** Si dimlat_par_couche_manuel = True, il faut renseigner manuellement
#: ** les épaisseur de chaque couches
dimlat_par_couche_manuel:False:
#: ** ATTENTION : Il doit il y avoir le même nombre de valeur que nb_y_par_couche
dimlat_par_couche:13.3,17.7,0,0:
#:
#: ** Choix de l'épaisseur des parois de chaque couche
#: ** ep_par_couche est en pourcentage de l'épaisseur ep définie ci-dessus
#: ** ATTENTION : Il doit il y avoir le même nombre de valeur que nb_y_par_couche
ep_par_couche:1.1,1.0,0.9,0.8:
#:
#: ** Choix de l'épaisseur des plateaux liants les différentes couches en (mm)
#: ** Laisser la valeur à 0 si le plateau ne doit pas être créé
#: ** ATTENTION : Il doit il y avoir une valeur de moins que nb_y_par_couche
ep_plateaux:0.3,0.3,0.3:
#:
#: /// GÉNÉRATION DE LA STRUCTURE HEXAGONES + TRIANGLES1 2D ALIGNÉS OU NON \\\
#: Radians
#: ** Sans gradients
alpha_hex_tri1_2D:1.01:
#: ** Avec gradients
alpha_hex_tri1_2D_grad:1.01,0.95,0.87:
#:
#: /// GÉNÉRATION DE LA STRUCTURE TRIANGLES 2D \\\
#: Radians
#: ** Sans gradients
alpha_tri_2D:1.01:
#: ** Avec gradients
alpha_tri_2D_grad:1.01,0.95,0.87:
#:
#: /// GÉNÉRATION DE LA STRUCTURE COSINUS 2D SANS GRADIENTS \\\
#: *** nb_motif_y_sg représente le nombre de plateaux
#: ***
#: *** Déphasage du cosinus en radians (cos(x + phi))
#: *** Il est possible de renseigner plusieurs déphasages (un par cosinus
#: *** tracé). Il faudra donc commenter les lignes sans plusieurs déphasages
#: *** et s'assurer que phi_x et phi_x soient respectivements aussi longs que
#: *** le nombres de motifs en x et en y.
#: ATTENTION : Si phi_x contient pliseurs déphasages alors phi_y doit aussi
#: contenir plusieurs déphasages même s'ils sont identiques.
phi:0.0:
#:phi:0.0,0.0,0.0:
#: *** Facteur sur la période du cosinus (cos(x * period_fact))
#: *** Même chose que sur le déphasage il est possible de renseigner
#: *** plusieurs périodes.
period_fact:1.0:
#:period_fact:1.0,1.0,1.0:
#: *** Amplitude du cosinus (amp * cos(x))
#: *** Même chose que sur le déphasage il est possible de renseigner
#: *** plusieurs amplitudes.
amp:2.0:
#:amp:2.0,2.0,2.0:
#: *** Nombre de points de discrétisation du cosinus
#: *** nbpts_cos = 4 points par période minimum pour avoir une
#: *** bonne précision
nbpts_cos:80:
#:
#: /// GÉNÉRATION DE LA STRUCTURE COSINUS 2D AVEC GRADIENTS \\\
#: *** ATTENTION : DANS CETTE SECTION, LE DÉLIMITEUR DE COUCHE DE GRADIENT
#: *** EST LE CARACTÈRE "|" ET LE DÉLIMITEUR DE GRADIENT DANS LA COUCHE
#: *** (VARIATIONS D'UN PARAMÈTRE SUIVANT LE COSINUS DESSINÉ) EST LE
#: *** CARACTÈRE ",".
#: ***
#: *** nb_y_par_couche représente le nombre de plateaux par couche
#: ***
#: *** Déphasage du cosinus en radians (cos(x + phi))
#: *** Il est possible de renseigner plusieurs déphasages (un par cosinus
#: *** tracé). Il faudra donc commenter les lignes sans plusieurs déphasages
#: *** et s'assurer que phi_x et phi_x soient respectivements aussi longs que
#: *** le nombres de motifs en x et en y.
#: ATTENTION : Si phi_x contient pliseurs déphasages alors phi_y doit aussi
#: contenir plusieurs déphasages même s'ils sont identiques.
phi_grad:0.0|0.0:
#:phi_grad:0.0,0.0|0.0,0.0|0.0,0.0:
#: *** Facteur sur la période du cosinus (cos(x * period_fact))
#: *** Même chose que sur le déphasage il est possible de renseigner
#: *** plusieurs périodes.
period_fact_grad:1.0|1.0:
#:period_fact_grad:1.0,1.0|1.0,1.0|1.0,1.0:
#: *** Amplitude du cosinus (amp * cos(x))
#: *** Même chose que sur le déphasage il est possible de renseigner
#: *** plusieurs amplitudes.
amp_grad:2.0|2.0:
#:amp_grad:2.0,2.0|2.0,2.0|2.0,2.0:
#: *** Nombre de points de discrétisation du cosinus
#: *** nbpts_cos = 4 points par période minimum pour avoir une
#: *** bonne précision
nbpts_cos_grad:80|80:
#:
#:-----------------------------------------
#:
#:-----------------------------------------
#: --- PARTIE EXPORTATION DU MODÈLE 3D ---
#: ** Extrude l'esquisse de base 
#: ** True = Extruder l'essquisse / False = Ne pas extruder
extrude:True:
#:
#: ** Exporte la pièce au format stl
#: ** True = Exporter au format stl / False = Ne pas exporter
#: ** Si cette option est à True, export_path et export_name
#: ** doivent-être renseignés
#: ** ATTENTION : Si export = True, extrude doit être activé (extrude = True)
export:True:
#: ** export_name ne doit contenir uniquement le nom de l'exportation et sans extention
export_name:structure:
#: ** export_path ne doit contenir que le chemin à partir d'où le logiciel est avec le
#: ** dossier où vous voulez exporter les structures. ATTENTION à ne pas oublier "/"
#: ** à la fin du nom du dossier
export_path:/home/adrien/:
#:
#: ** Affiche l'(les)esquisse(s) de départ après l'extrusion
#: ** True = Laisser l'(les) essquisse(s) affichées / False = Cacher la/les essquisse(s)
sketch_visible:False:
#:-----------------------------------------
#:
#:-------------------------
#: --- PARTIE DEBOGAGE ---
#: ** Trace les lignes de construction
#: ** True = Oui / False = Non
semi_debug:True:
#: ** Affiche les actions dans le terminal et dans le fichier de débogage
debug:True:
#: ** Génère le fichier de déboggage dans le dossier "debug_current_folder"
debug_current_folder:log/:
#:-------------------------
