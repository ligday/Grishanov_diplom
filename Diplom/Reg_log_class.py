from PyQt5 import QtWidgets
import unicodedata as ud
import os
# from mainwindow import Ui_MainWindow
import xml.etree.cElementTree as ET
import os.path

class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonRegister = QtWidgets.QPushButton('Registration', self)
        self.buttonLogin = QtWidgets.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonRegister.clicked.connect(self.create_write)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        layout.addWidget(self.buttonRegister)
        self.textName.textChanged.connect(lambda: self.proverka_na_exist())
        self.textPass.textChanged.connect(lambda: self.proverka_na_exist())

        self.exist_of_text = False

        #self.exit_from_reg = False


    def handleLogin(self):
        if os.path.exists("data\\filename2.xml"):
            root = ET.parse('Data\\filename2.xml').getroot()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'No registered users')
            return
        if not root.find('U_' + self.textName.text()) == None:
            if root.find('U_' + self.textName.text()).text == self.textPass.text():
                for log in root.findall('Login_folder'):
                    root.remove(log)
                login_folder = ET.Element('Login_folder')
                root.append(login_folder)
                root.find('Login_folder').text = 'U_' + self.textName.text()
                tree = ET.ElementTree(root)
                tree.write("data\\filename2.xml")
                #root.find('U_' + self.textName.text()).text
                self.accept()
            else:
                print(root.find('U_' + self.textName.text()).text, self.textPass.text())
                QtWidgets.QMessageBox.warning(
                    self, 'Error', 'Wrong password')
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'This login does not exist')

    def create_write(self):
        if not Login.only_roman_chars(self.textName.text()) == True or not Login.only_roman_chars(self.textPass.text()) == True:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Only latin letters')
            return
        if not self.exist_of_text:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Please, enter the text')
            return
        if os.path.exists("data\\filename2.xml"):
            root = ET.parse('Data\\filename2.xml').getroot()
            if not root.find('U_' + self.textName.text()) == None:
                QtWidgets.QMessageBox.warning(
                    self, 'Error', 'This user already exist!')
                return
        else:
            root = ET.Element("root")

        Users = ET.Element('U_' + self.textName.text())
        users_of_user_table = ET.Element('Users')
        Gateways_E = ET.Element('Gate')
        Services = ET.Element('Services')
        Routes = ET.Element('Routes')
        Groups = ET.Element('Groups')
        Prompts = ET.Element('Prompts')
        Update = ET.Element('Update')

        root.append(Users)
        Users.append(users_of_user_table)
        Users.append(Gateways_E)
        Users.append(Services)
        Users.append(Routes)
        Users.append(Groups)
        Users.append(Prompts)
        Users.append(Update)


        Users.find(".//Prompts").text = '5'
        text_of_prom = ['User is not available', 'Wait', 'User no answer', 'User is busy', 'Music on hold']

        for i in range(5):

            ET.SubElement(Prompts, "Prompts_{}".format(str(i)),
                            Upload=os.getcwd() + '\\Prompts' + '\\{}'.format(text_of_prom[i]) + '.mp3',
                            Pro_Name='{}'.format(text_of_prom[i])).text

        root.find('U_' + self.textName.text()).text = self.textPass.text()

        tree = ET.ElementTree(root)
        tree.write("data\\filename2.xml")
        QtWidgets.QMessageBox.information(
            self, 'Error', 'You are successfully registered')

    def proverka_na_exist(self):
        if self.textName.text().replace(' ', '') != '' and self.textPass.text().replace(' ', '') != '':
            self.exist_of_text = True
        else:
            self.exist_of_text = False

    def only_roman_chars(unistr):
        return all(Login.is_latin(uchr)
                   for uchr in unistr
                   if uchr.isalpha())

    def is_latin(uchr):
        latin_letters = {}
        try:
            return latin_letters[uchr]
        except KeyError:
            return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

#class Window(QtWidgets.QMainWindow):
#    def __init__(self, parent=None):
#        super(Window, self).__init__(parent)
#        # self.ui = Ui_MainWindow()
#        # self.ui.setupUi(self)
#
#if __name__ == '__main__':

#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    login = Login()

#    if login.exec_() == QtWidgets.QDialog.Accepted:
#        window = Window()