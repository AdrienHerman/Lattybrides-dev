"""
Gestion des erreurs.
HERMAN Adrien
27/01/2024
"""

def print_or_addterminal_message(QWindow=None, type_msg="msg", text=""):
	"""
	Choisir entre afficher le message dans le terminal d'exécution
	ou dans le terminal de la fenêtre de l'application.

	-----------
	Variables :
		- QWindow 	: Objet fenêtre.
		- type_msg  : Type du message (msg=message, wrg=warning, err=erreur).
		- text    	: Texte à afficher dans le terminal.
	-----------
	"""

	if QWindow:
		if type_msg == "err":	QWindow.textEdit_terminal_addError(text)
		if type_msg == "wrg":	QWindow.textEdit_terminal_addWarning(text)
		if type_msg == "msg":	QWindow.textEdit_terminal_addText(text)

	else:
		print(text)