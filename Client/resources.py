"""Language Resources."""

class Resources():
    """Class containing language resources."""
    def __init__(self, language):
        if language == 'en':
            self.resource_language_english()
        elif language == 'fr':
            self.resource_language_french()
        else:
            raise NotImplementedError('Unsupported Language')

    def resource_language_english(self):
        """English Resources."""
        #ROOT
        self.title = 'Project M'
        #LOGIN UI
        self.username = 'Username'
        self.password = 'Password'
        self.log_in = 'Login'
        self.exit = 'Exit'
        self.register = 'Register'
        #REGISTER UI
        self.mail = 'E-Mail'
        self.number = 'Phone Number'
        self.confirmation_code = 'Confirmation Code'
        self.confirmation_sms = 'Your ProjectM Confirmation Code is : '
        #MAIN UI
        #FRAMES
        self.user_list_label = ' Online Users '
        self.output_label = ' Messages Received '
        self.input_label = ' Your Input : '
        #BUTTONS
        self.send = ' Send '
        #MENUS
        self.server_menu = 'Servers'
        self.server_infos = 'Server Infos'
        self.server_connect = 'Connect'
        self.manage_server = 'Manage Servers'
        self.add_server = 'Add'
        self.delete = 'Delete'
        self.edit = 'Edit'
        self.done = 'Done'
        self.cancel = 'Cancel'
        #Profile Menu
        self.profile = 'Profile'
        self.change_pseudo = 'Change Username'
        self.change_password = 'Change Password'
        #Change Dialbox
        self.new_pseudo_label = 'New Username : '
        self.old_pseudo_label = 'Old Username : '
        self.old_password_label = 'Old Password : '
        self.new_password_label = 'New Password : '
        self.username_label = 'Username : '
        self.password_label = 'Password : '
        self.password_changed = 'Password changed !'
        self.pseudo_changed = 'Username Changed !'
        self.pseudo_taken = 'This Username is already taken.'
        self.pseudo_too_short = 'Your new Username is too short.'
        self.password_too_short = 'Your new Password is too short.'
        self.password_non_identical = 'Both new fields must be identical.'
        self.password_wrong = 'Wrong Password'
        #ADD SERVER WINDOW
        self.server_name_label = 'Server Name : '
        self.address_label = 'Server Adress : '
        self.port_label = 'Server Port : '
        self.help_menu = 'Help'
        self.about = 'About'
        #ERROR OUTPUT
        self.connection_to_projectm_failed = 'Connection to ProjectM Servers Failed.'
        self.bad_name_pass_combo = 'Invalid Username or Password.\n'
        self.bad_name_regex = 'Username must be at least 4 characters length and only contains letters, numbers and "-" and "_".\n'
        self.name_taken = 'This Username already exists.\n'
        self.bad_mail_regex = 'This Email is not valid.\n'
        self.mail_taken = 'This Email already exists.\n'
        self.bad_phone_number_regex = 'This is not a valid phone number. Format must be : +(ind)(number)\n'
        self.phone_number_taken = 'This Phone Number is already in use.'
        self.pseudo_warning_title = 'Invalid Pseudo Length.'
        self.pseudo_warning_msg = 'Pseudo must be at least 5 characters length.'
        self.server_connect_empty_title = 'Connection Failed'
        self.server_connect_empty_msg = 'You did not select any Server.'
        #DIVERS
        self.time_format = '%H:%M:%S'

    def resource_language_french(self):
        """French Resources."""
        print('Not implemented yet.')
