"""
Afficher les données.
HERMAN Adrien
21/11/2023
"""

# Modules de Python
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Modules du Logiciel
from bin.errors import *

def graphe(	data_x=[],
			data_y=[],
			label_x="",
			label_y="",
			titre="",
			fileName=[""],
			xlim_inf=False,
			xlim_sup=False,
			ylim_inf=False,
			ylim_sup=False,
			fig=None,
			ax=None,
			couleurs=['b','g','r','c','m','y','k'],
			type_lignes=['-','--',':','-.'],
			QWindow=None):
	"""
	Affichage d'un graphe xy.

	-----------
	Variables :
		- data_x / data_y        : Vecteurs des données x et y (Plusieurs vecteurs dans une variable [Vecteur1, Vecteur2, ...])
		- label_x / label_y      : Label des axes x et y
		- fileName               : Nom de fichier d'expérience
		- couleurs / type_lignes : Formattage des données dans le graphique
		- fig / ax               : Objets contenant le graphique
		- QWindow                : Objet fenêtre.
	-----------

	---------
	Retours :
	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	---------
	"""

	if fig == None and ax == None:
		fig, ax = plt.subplots()
	elif fig == None or ax == None:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="err",
										text="graphe\nERREUR : Les objets contenant les données du graphique ne sont pas corrects")

	ax.set_title(titre)
	ax.set_xlabel(label_x)
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	ax.set_ylabel(label_y)

	if type(data_x) != list or type(data_y) != list:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="err",
										text="graphe\nERREUR : Les types des arguments ne sont pas correctes.\n     type(data_x)={0}\n     type(data_y)={1}".format(type(data_x), type(data_y)))

		return None

	if len(data_x) != len(data_y) and len(data_x) != 0:
		print_or_addterminal_message(	QWindow=QWindow,
										type_msg="err",
										text="Le nombre de courbes en x et y ne sont pas les mêmes ou sont vides.\n     len(data_x)={0}\n     len(data_y)={1}".format(len(data_x), len(data_y)))

		return None

	for i in range(len(data_y)):
		if len(data_x[i]) != len(data_y[i]) and len(data_x[i]) != 0:
			print_or_addterminal_message(	QWindow=QWindow,
										type_msg="err",
										text="graphe\nERREUR : Les vecteurs de données doivent-être de même longueur et non vides.\n     len(data_x)={0}\n     len(data_y)={1}".format(len(data_x), len(data_y)))

			return None

		if type(fileName) == list:
			ax.plot(data_x[i], data_y[i], couleurs[i % len(couleurs)] + type_lignes[(i // len(couleurs)) % len(type_lignes)], label=fileName[i])

		else:
			print_or_addterminal_message(	QWindow=QWindow,
										type_msg="err",
										text="graphe\nERREUR : Le type du nom de fichier est incorrect !\n     type(fileName)={0}\n     fileName={1}".format(type(fileName), fileName))

	if (type(fileName) == str and fileName != "") or type(fileName) == list:
		ax.legend()

	ax.grid()

	if xlim_inf != False or xlim_sup != False:
		ax.set_xlim([xlim_inf, xlim_sup])

	if ylim_inf != False or ylim_sup != False:
		ax.set_ylim([ylim_inf, ylim_sup])

	if fig == None and ax == None:
		plt.show()