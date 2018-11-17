class I18N():
	def __init__(self, language):
		if language == 'en':self.resourceLanguageEnglish()
		elif language == 'de':self.resourceLanguageGerman()
		else: raise NotImplementedError('Unsupported Language')

	def resourceLanguageEnglish(self):
		self.title = 'Python Graphical User Interface'
		self.file = 'File'
		self.new = 'New'
		self.exit = 'Exit'
		self.help = 'Help'
		self.about = 'About'

		self.WIDGET_LABEL = ' Widgets Frame '
		self.disabled = 'Disabled'
		self.unchecked = 'Unchecked'
		self.toggle = 'Toggle'

		self.colors = ['Blue', 'Gold', 'Red']
		self.colorsIn = ['in Blue', 'in Gold', 'in Red']

		self.timezones = 'Display Timezones'
		self.localtz = 'Local Timezone'
		self.getTime = 'Current Time'

		self.labelsFrame = ' Labels wihtin a Frame '
		self.chooseNumber = 'Choose a number : '
		self.label1 = 'Label 1'
		self.label2 = 'Label 2'
		self.label3 = 'Label 3'

		self.mgrFiles = ' Manage Files '

		self.browseTo = 'Browse to File...'
		self.copyTo = 'Copy File to : '

	def resourceLanguageGerman(self):
		self.title = 'Python Grafische Benutzeroberflaeche'
		self.file  = "Datei"
		self.new   = "Neu"
		self.exit  = "Schliessen"
		self.help  = "Hilfe"
		self.about = "Ueber"
		self.WIDGET_LABEL = ' Widgets Rahmen '
		self.disabled  = "Deaktiviert"
		self.unchecked = "NichtMarkiert"
		self.toggle    = "Markieren"
		self.colors   = ["Blau", "Gold", "Rot"]
		self.colorsIn = ["in Blau", "in Gold", "in Rot"]
		self.timezones = 'Display Timezones en DEUTSCHE'
		self.localtz = 'Local Timezones en DEUTSCHE'
		self.getTime = 'Current Time en DEUTSCH'
		self.labelsFrame  = ' EtikettenimRahmen '
		self.chooseNumber = "WaehleeineNummer:"
		self.label1       = "Etikette 1"
		self.label2       = "Etikette 2"
		self.label3       = "Etikette 3"
		self.mgrFiles = ' DateienOrganisieren '
		self.browseTo = "WaehleeineDatei... "
		self.copyTo   = "KopiereDateizu : "