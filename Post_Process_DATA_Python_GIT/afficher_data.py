"""
Afficher les données
HERMAN Adrien
21/11/2023
"""

def graphe(data_x=[], data_y[], label_x="", label_y="", titre="", fileName="", couleurs=['b','g','r','c','m','y','k'], type_lignes=['-','--',':','-.']):
	"""
	Affichage d'un graphe xy.

	-----------
	Variables :
		- data_x / data_y : Vecteurs des données x et y (Plusieurs vecteurs dans une variable [Vecteur1, Vecteur2, ...])
		- label_x / label_y : Label des axes x et y
		- fileName : Nom de fichier d'expérience
		- couleurs / type_lignes : Formattage des données dans le graphique
		- plt / fig / ax : Objets contenant le graphique
	-----------
	"""

	fig, ax = plt.subplots()
	ax.set_title(titre)
	ax.set_xlabel(label_x)
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	ax.set_ylabel(label_y)

	if type(data_x) != list or type(data_y) != list:
		print("Les types des arguments ne sont pas correctes.\n     type(data_x)={0}\n     type(data_y)={1}".format(type(data_x), type(data_y)))

		return None

	if len(data_x) != len(data_y) and len(data_x) != 0:
		print("Le nombre de courbes en x et y ne sont pas les mêmes ou sont vides.\n     len(data_x)={0}\n     len(data_y)={1}".format(len(data_x), len(data_y)))

		return None

	for i in range(len(data_y)):
		if len(data_x[i]) != len(data_y[i]) and len(data_x[i]) != 0:
			print("Les vecteurs de données doivent-être de même longueur et non vides.\n     len(data_x)={0}\n     len(data_y)={1}".format(len(data_x), len(data_y)))

			return None

		if type(fileName) == str and fileName != "":
			ax.plot(data_x[i], data_y[i], couleurs[i % len(couleurs)] + type_lignes[(i // len(couleurs)) % len(type_lignes)], label=fileName[i])

		elif type(fileName) == list:
			ax.plot(data_x[i], data_y[i], couleurs[i % len(couleurs)] + type_lignes[(i // len(couleurs)) % len(type_lignes)], label=fileName[i])

		else:
			print("Le nom de fichier est erronné !")

			return None

	if (type(fileName) == str and fileName != "") or type(fileName) == list:
		ax.legend()

	plt.grid()

	return plt