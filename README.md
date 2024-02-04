<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/FreeCAD016-logo.svg" width="128" height="128" /></td><td><img src="https://github.com/AdrienHerman/PLP/blob/main/image.png" width="128" /></td></tbody></table>

# PLP23INT16 : Étude de la capacité d'absorption de diverses structures lattices hybrides à gradients de réseau

## Branche "last_stable"
Ceci est la branche "last_stable" à utiliser pour générer des structures ou pour analyser les données expérimentales.
Pour bénéficier des dernières avancées, veuillez aller à la branche "dev" mais elle peut être instable.

# Partie Génération des Structures

## Dépendances
Les modules python nécessaires au bon fonctionnement du code de génération des structures sont les suivantes :
```
 - os (Installé de base)
 - sys (Installé de base)
 - math (Installé de base)
 - datetime
 - matplotlib
 - PySide
```
L'exécution du code de génération des structures doit obligatoirement se faire via FreeCAD (voir partie utilisation).
**_ATTENTION : La dernière version de FreeCAD Testée avec ce code est la version 21.1 !_**  

## Configuration

## Génération de structures :

 <table>
		<thead>
			<tr>
				<th colspan="8">Paramètres d'optimisation de la masse</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>optimisation_masse</td><td>True / False</td><td>True = l'optimisation de la masse est réalisée et les variables objectif_masse, tolerance, nb_pas_max, correction_ep_par_pas, pourcentage_modification_correction, seuil_augmentation_correction, seuil_diminution_correction, rho doivent-être renseignées</td></tr>
			<tr><td>objectif_masse</td><td>nb réel positif</td><td>Objectif de masse à atteindre avant l'arrêt des calculs (en g)</td></tr>
			<tr><td>tolerance</td><td>nb réel positif</td><td>Tolérance sur l'objectif de masse : objectif masse - tolérance >= masse calculée >= objectif masse + tolérance</td></tr>
			<tr><td>nb_pas_max</td><td>nb entier positif</td><td>Nombre d'itération maximale avant l'arrêt des calculs même si l'objectif de masse n'est pas atteint</td></tr>
			<tr><td>correction_ep_par_pas</td><td>nb réel positif </td><td>Valeur de correction de l'épaisseur des parois à chaque pas (augmentation ou diminution en mm)</td></tr>
			<tr><td>pourcentage_modification_correction</td><td>nb entier positif</td><td>Pourcentage de modification de la variable correction_ep_par_pas utilisé si la convergence est trop lente / rapide</td></tr>
			<tr><td>seuil_augmentation_correction</td><td>nb entier positif</td><td>Seuil à partir duquel correction_ep_par_pas est augmentée</td></tr>
		<tr><td>seuil_diminution_correction</td><td>nb entier positif</td><td>Seuil à partir duquel correction_ep_par_pas est diminuée</td></tr>
			<tr><td>rho</td><td>nb entier positif</td><td>Masse volumique du matériau utilisé pour l'impression (en g/cm^3)</td></tr>
	</tbody>
</table>
 
 ## Méthodes de Génération
 
 <table>
		<thead>
			<tr>
				<th colspan="3">Méthode de Génération de Structure à Utiliser</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>gen_motif_basic</td><td>True / False</td><td>True = Génère des motifs sans gradient</td></tr>
			<tr><td>gen_motif_grad</td><td>True / False</td><td>True = Génère des motifs avec gradient</td></tr>
	</tbody>
</table>

## Géométrie des structures

<table>
		<thead>
			<tr>
				<th colspan="4">Plateaux liants les extrémités des structures</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>generation_plateaux_extremitees</td><td>True/False</td><td>True = Génère des plateaux liants aux extrémités de la structure pour lier les motifs et homogénéiser la répartition de la force d'impact. Si True, ep_plateaux_dessous et ep_plateaux_dessus doivent être renseignés</td></tr>
			<tr><td>ep_plateau_dessous</td><td>nb réel positif</td><td>Choix de l'épaisseur du plateau inférieur liant les extrémité de la structure (mm)</td></tr>
			<tr><td>ep_plateau_dessus</td><td>nb réel positif</td><td>Choix de l'épaisseur du plateau supérieur liant les extrémité de la structure (mm)</td></tr>
	</tbody>
</table>

<br>
<br>

<table>
		<thead>
			<tr>
				<th colspan="5">Propriétés géométriques communes </th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>ep</td><td>nb réel positif</td><td>Choix de l'épaisseur des parois (mm)</td></tr>
			<tr><td>dimlat_ep</td><td>nb réel positif</td><td>Choix de l'épaisseur d'extrusion du modèle (mm)</td></tr>
			<tr><td>dimlat_x</td><td>nb réel positif</td><td>Choix du nombre de la longueur du modèle l'axe x (mm)</td></tr>
			<tr><td>dimlat_y</td><td>nb réel positif</td><td>Choix du nombre de la longueur du modèle l'axe y (mm)</td></tr>
	</tbody>
</table>

<br>
<br>

<table>
		<thead>
			<tr>
				<th colspan="3">Génération de structures sans gradients</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>nb_motif_x_lb</td><td>Nombre entier positif</td><td>Choix du nombre de motifs sur l'axe x </td></tr>
			<tr><td>nb_motif_y_lb</td><td>Nombre entier positif</td><td>Choix du nombre de motifs sur l'axe y</td></tr>
			<tr><td>nom_sketch_motif_basic</td><td>pad_motif</td><td>Renseigne le nom du pad du motif</td></tr>
			<tr><td>nom_sketch_motif_basic</td><td>sketch_motif</td><td>Renseigne le nom de l'esquisse du motif</td></tr>
	</tbody>
</table>  
<br>  

<table>
		<thead>
			<tr>
				<th colspan="6">Génération de gradient</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>nb_y_par_couche</td><td>liste nb entier </td><td>Choix du nombre de motifs en y par couches. Les nombre de motifs doivent-être séparés par une "," ATTENTION : Il ne doit pas il y avoir un espace entre les valeurs !</td></tr>
			<tr><td>nb_x_par_couche</td><td>liste nb entier </td><td>Choix du nombre de motifs en x par couches. Les nombre de motifs doivent-être séparés par une "," ATTENTION : Il ne doit pas il y avoir un espace entre les valeurs !</td></tr>
			<tr><td>dimlat_par_couche_manuel</td><td>True / False</td><td>Si dimlat_par_couche_manuel = False, les dimensions des couches sont choisies automatiquement au prorata du nombre de motifs y par couche en fonction de la variable dimlat_y. Si dimlat_par_couche_manuel = True, il faut renseigner manuellement les épaisseur de chaque couches. ATTENTION : Il doit il y avoir le même nombre de valeur que nb_y_par_couche</td></tr>
			<tr><td>ep_par_couche</td><td>nb réel positif</td><td>Choix de l'épaisseur par couche ATTENTION : Il doit il y avoir le même nombre de valeur que nb_y_par_couche</td></tr>
			<tr><td>ep_plateaux</td><td>nb réel positif</td><td>Choix de l'épaisseur des plateaux liant les extrémité de la structure. Laisser la valeur à 0 si le plateau ne doit pas être créé. ATTENTION : Il doit il y avoir une valeur de moins que nb_y_par_couche</td></tr>
	</tbody>
</table>

## Exportation du modèle 3D

<table>
		<thead>
			<tr>
				<th colspan="3">Paramètres d'exportation du modèle</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>extrude</td><td>True / False</td><td>True = Extrude l'esquisse de base</td></tr>
			<tr><td>export</td><td>True / False</td><td>True = exporte la pièce au format .stl. Si True, export_path et export_name doivent être renseignés.  ATTENTION : Si export = True, extrude doit être activé (extrude = True) </td></tr>
			<tr><td>export_name</td><td>structure</td><td>export_name ne doit contenir uniquement le nom de l'exportation et sans extention</td></tr>
			<tr><td>export_path</td><td>STRUCTURES_GENEREES/</td><td>export_path ne doit contenir que le chemin à partir d'où le logiciel est avec le dossier où vous voulez exporter les structures. ATTENTION à ne pas oublier "/" à la fin du nom du dossier</td></tr>	
			<tr><td>sketch_visible</td><td>True / False</td><td>True = Laisser l'(les) esquisse(s) affichées après l'extrusion / False = Cacher la/les esquisse(s)</td></tr>		
	</tbody>
</table>

<br>
<br>

<table>
		<thead>
			<tr>
				<th colspan="3">Paramètres de débogage</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>semi_debug</td><td>True / False</td><td>True = Trace les ligne de construction</td></tr>
			<tr><td>debug</td><td>True / False</td><td>True = Affiche les actions dans le terminal et dans le fichier de débogage</td></tr>
			<tr><td>debug_current_folder</td><td>True / False</td><td>True = Génère le fichier de débogage dans le dossier "debug" du répertoire courant. Sinon Générer le fichier de débogage dans le dossier indiqué dans la variable</td></tr>
	</tbody>
</table>

## Utilisation

Dans cette partie nous allons vous expliquer la démarche à suivre afin de générer vos structures.
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/génération.png" width="800"/></td></tbody></table>
Le dossier Generation Structures Python s'organise de la manière suivante : 
Dans le dossier log se situe l'historique de génération du code. Vous pouvez donc y retrouver les éventuelles erreur qui peuvent survenir. 
Dans le dossier bin se situe l'ensemble du code python. Chaque fonction peut être utilisée sous forme de bibliothèque python pour d'autres programmes. 
Dans le dossier STRUCTURES_GENEREES se situe les structures générées après l'exécution du programme. 

Dans un premier temps, il vous faut télécharger le logiciel FreeCAD. Nous avons travaillé avec le version 0.21.2. Voici un lien qui vous permettra de le télécharger :  
<a href="https://www.freecad.org/downloads.php?lang=fr">Lien de téléchargement FreeCAD</a> 
Une fois l'installation faite, vous pouvez télécharger le dossier ZIP contenant les programmes. 
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/téléchargement du code 1.png" width="800"/></td></tbody></table>
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/téléchargement du code 2.png" width="800"/></td></tbody></table>
Sélectionnez code en vert (comme sur l'image) puis, Download ZIP. Le téléchargement va commencer. 
Ensuite, vous pouvez ouvrir le dossier puis le "déziper" 
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/dézipage.png" width="800"/></td></tbody></table>

Une fois cette étape effectuée, vous pouvez désormais ouvrir FreeCAD. 
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/freeCad.png" width="800"/></td></tbody></table>
Rendez vous ensuite dans Fichier > Ouvrir et sélectionnez le fichier EXEC.py situé dans /PLP-last_stable/Generation Structures Python
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/Fichier.png" width="800"/></td></tbody></table>
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/ouverture exec.png" width="800"/></td></tbody></table>
Le fichier va donc s'ouvrir avec FreeCAD et le code s'affiche.
A la ligne 13, renseignez le chemin de l'emplacement du fichier EXEC.py.
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/changement chemin.png" width="800"/></td></tbody></table>
Une fois ce changement effectué, le programme est prêt à générer la structure.
Pour lancer les calculs, cliquez sur la flèche verte en haut de l'écran.
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/flèche verte.png" width="800"/></td></tbody></table>
Les calculs se lancent. Une fois qu'ils sont finis, un graphe s'affiche et la pièce s'enregistre dans le dossier  STRUCTURES_GENEREES.
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/emplacement struct.png" width="800"/></td></tbody></table>

Si vous souhaitez modifier les paramètres de la structure, vous pouvez le faire dans le fichier config.txt où l'ensemble des paramètres sont décrit dans la section précédente de ce document. Puis, enregistrer le fichier et relancer les calculs avec la flèche verte.

  
# Partie Analyse des Données Expérimentales

## Dépendances

Les modules python nécessaires au bon fonctionnement du code d'analyse des données sont les suivantes :
```
 - matplotlib
 - scipy
 - os (Installé de base)
```
Pour obtenir les dépendances précédentes, il faut ouvrir un terminal et renseigner la commande suivante : 
#### Sur Windows & MacOS
```
 pip install matplotlib scipy 
 ```
#### Sur Linux avec Python3
 ```
 pip3 install matplotlib scipy 
 ```
 Si jamais pip n'est pas installé sur votre ordinateur, voici des tutos pour l'obtenir :  
<a href="https://stacklima.com/comment-installer-pip-dans-macos/">Tuto sous MacOS</a>  
<a href="https://waytolearnx.com/2020/06/comment-installer-pip-pour-python-sur-windows.html">Tuto sous Windows</a>  
<a href="https://ubunlog.com/fr/pip-instalacion-conceptos-basicos-ubuntu-20-04/">Tuto sous Linux (Ubuntu)</a>  

Le message d'erreur ci-après peut survenir : 
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/Erreur_pip.png" width="800"/></td></tbody></table>

Dans ce cas, exécuter la commande suivante : 
#### Sur Windows
```
python.exe -m pip install --upgrade pip
```
#### Sur MacOs
 ```
python -m pip install --upgrade pip
```
#### Sur Linux avec Python3
```
python3 pip install --upgrade pip
``` 
avant de relancer la commande précédente.

## Utilisation
L'objectif de ce programme est de générer des courbes qui permettent l'analyse des données expérimentales recueillies. 
Le programme est capable de calculer calcul la vitesse d'impact, l'énergie.
<table><tbody><td><img src="https://github.com/AdrienHerman/PLP/blob/main/post_trait.png" width="800"/></td></tbody></table>
Le dossier Post-Process DATA Python s'organise de la manière suivante : 
Dans le dossier bin se situe l'ensemble du code python. Chaque fonction peut être utilisée sous forme de bibliothèque python pour d'autres programmes. 
Dans le dossier DATA se situe l'ensemble des données expérimentales. 
Pour exécuter le programme ouvrez le dossier Post-Process DATA Python puis exécuter le fichier EXEC.py.
Sur Windows, double cliquez sur le fichier pour le lancer.
Sur linux, renseignez la commande suivante : 
```
python3 EXEC.py
``` 
Vous pouvez modifier les paramètres de traitements des données expérimentales dans le fichier config.txt.


### Configuration
Pour la configuration de l'analyse, vous pouvez ouvrir le fichier config.txt.  
Explication de la syntaxe : "#:" indique un commentaire.  
Lorsque l'on renseigne des paramètres, on les espaces par ":" puis on finit par ":".  
image
<table>
		<thead>
			<tr>
				<th colspan="3">Paramètres de Lecture des Données</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>superposer_courbes</td><td>True / False</td><td>True = Lecture des données du dossier renseigné dans la variable nom_dossier et superpose toutes les courbes</td></tr>
			<tr><td>calc_temps</td><td>True / False</td><td>True = Calcul le temps des donnée de l'essai</td></tr>
	</tbody>
</table>

<br>
<br>

<table>
		<thead>
			<tr>
				<th colspan="3">Paramètres d'enregistrement des Données</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>enregistrer_data</td><td>True / False</td><td>True = Enregistre les donnée dans un fichier .txt</td></tr>
			<tr><td>nom_enregistrement</td><td>STRUCT_X_XX</td><td>Renomme le fichier d'enregistrement des données</td></tr>
	</tbody>
</table>


Dans un premier temps on choisit si l'on souhaite superposer les courbes ou non (True ou False). Ensuite, on sélectionne la structure que l'on veut analyser. On l'appelle par son nom : DATA/STRUCT_X_XX.CSV dans le bon dossier DATA/X/. 

Ensuite, on choisit ou non de calculer les donnée de temps de l'essai.
On enregistre les données lu dans un fichier texte que l'on nomme STRUCT_X_XX dans le dossier DATA/X/.

<br>
<br>

<table>
		<thead>
			<tr>
				<th colspan="7">Paramètres de traitement des données</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>sppr_rollback<td>True / False</td><td>True = Supprime les données correspondantes à des boucles de retour en arrière</td></tr>
			<tr><td>recherche_deb_impact</td><td>True / False</td><td>True = Recherche le début de l'impact automatiquement. Si True, la variable taux_augmentation doit-être renseignée</td></tr>
			<tr><td>tarrage_dep</td><td>True / False</td><td>True = Remet la valeur de déplacement à 0. Si True, recherche_deb_impact doit être True</td></tr>
			<tr><td>tarrage_tmps</td><td>True / False</td><td>True = Remet la valeur du temps à 0. Si True, recherche_deb_impact doit être True</td></tr>
			<tr><td>detect_fin_essai</td><td>True / False</td><td>True = la détection de la fin de l'essai est activée et la variable dep_max doit-être renseignée. Si True, sppr_rollback, recherche_deb_impact et tarrage_dep doivent être True</td></tr>
			<tr><td>calculer_energie</td><td>True / False</td><td>True = Le calcul de l'énergie est effectué avec la méthode de Simpson. On peut changer les unités avec fact_force et fact_dep </td></tr>
	</tbody>
</table>

<br>
<br>

<table>
		<thead>
			<tr>
				<th colspan="3">Paramètres d'affichage graphique</th>
		    </tr>
		</thead>
		<tbody>
			<tr align="center"><td>Nom Variable</td><td>Valeurs Possibles</td><td>Explication Valeur</td></tr>
			<tr><td>afficher_dep_tmps</td><td>True / False</td><td>True = Permet d'afficher le graphique déplacement en fonction du temps</td></tr>
			<tr><td>afficher_F_tmps</td><td>True / False</td><td>True = Permet d'afficher le graphique force en fonction du temps</td></tr>	
			<tr><td>afficher_F_dep</td><td>True / False</td><td>True = Permet d'afficher le graphique force en fonction du déplacement</td></tr>		
			<tr><td>afficher_sep</td><td>True / False</td><td>True = Permet d'afficher les graphique sur des fenêtre séparées. Si False, les 3 graphiques sont sur la même fenêtre</td></tr>	
	</tbody>
</table>

### Exécution
Vous pouvez désormais lancer l'analyse des données expérimentales. 
Pour ce faire, dans la fenêtre de commande, vous allez pouvoir lancer l'instruction suivante : 
#### Sur Windows
```
EXEC.py
```
#### Sur Linux avec Python3
```
python3 EXEC.py
```
#### Sur MacOS
```
python EXEC.py
```

### Modification du Code