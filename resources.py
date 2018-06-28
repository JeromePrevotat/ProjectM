#Resources File

from datetime import datetime

class Resources():
	def __init__(self, language):
		if language == 'en':self.resourceLanguageEnglish()
		elif language == 'fr':self.resourceLanguageFrench()
		else: raise NotImplementedError('Unsupported Language')

	def resourceLanguageEnglish(self):
		#ROOT
		self.title = 'Project M'
		#LOGIN UI
		self.username = 'Username'
		self.password = 'Password'
		self.logIn = 'Login'
		self.exit = 'Exit'
		self.register = 'Register'
		#REGISTER UI
		self.mail = 'E-Mail'
		#MAIN UI
		#FRAMES
		self.userListLabel = ' Online Users '
		self.outputLabel = ' Messages Received '
		self.inputLabel = ' Your Input : '
		#BUTTONS
		self.send = ' Send '
		#MENUS
		self.serverMenu = 'Servers'
		self.serverInfos = 'Server Infos'
		self.serverConnect = 'Connect'

		self.manageServer = 'Manage Servers'
		self.addserver = 'Add'
		self.delete = 'Delete'
		self.edit = 'Edit'
		self.done = 'Done'
		self.cancel = 'Cancel'

		self.profile = 'Profile'
		self.personal = 'Personal Informations'
		#ADD SERVER WINDOW
		self.serverNameLabel = 'Server Name : '
		self.adressLabel = 'Server Adress : '
		self.portLabel = 'Server Port : '
		#PERSONNAL INFORMATIONS WINDOW
		self.pseudoLabel = 'Pseudo : '
		self.pseudoWarningTitle = 'Invalid Pseudo Length'
		self.pseudoWarningMsg = 'Pseudo must be at least 5 characters length.'
		self.helpMenu = 'Help'
		self.about = 'About'
		#DIVERS
		self.timeFormat = '%H:%M:%S'

	def resourceLanguageFrench(self):
		#ROOT
		self.title = 'Projet M'
		#LOGIN UI
		self.username = 'Nom d\'utilisateur'
		self.password = 'Mot de passe'
		self.logIn = 'Connexion'
		self.exit = 'Quitter'
		self.register = 'S\'enregistrer'
		#REGISTER UI
		self.mail = 'E-Mail'
		#FRAMES
		self.userListLabel = ' Utilisateurs en Ligne '
		self.outputLabel = ' Messages Reçus '
		self.inputLabel = ' Votre Message : '
		#BUTTONS
		self.send = ' Envoyer '
		#MENUS
		self.serverMenu = 'Serveurs'
		self.serverInfos = 'Informations du Serveur'
		self.serverConnect = 'Connexion'

		self.manageServer = 'Gestion des Serveurs'
		self.addserver = 'Ajouter'
		self.delete = 'Supprimer'
		self.edit = 'Editer'
		self.done = 'Terminer'
		self.cancel = 'Annuler'

		self.profile = 'Profil'
		self.personal = 'Informations Personnelles'
		#ADD SERVER WINDOW
		self.serverNameLabel = 'Server Name : '
		self.adressLabel = 'Server Adress : '
		self.portLabel = 'Server Port : '
		#PERSONNAL INFORMATIONS WINDOW
		self.pseudoLabel = 'Pseudo'
		self.pseudoWarningTitle = 'Longueur de Pseudo invalide'
		self.pseudoWarningMsg = 'Votre Pseudo doit contenir au moins 5 caractères.'
		self.helpMenu = 'Aide'
		self.about = 'À propos'
		#DIVERS
		self.timeFormat = 'De <xxx> à %H:%M:%S :\n\t'