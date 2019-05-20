import xml.etree.cElementTree as ET
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidgetItem)
from PyQt5 import QtWidgets
import Gui_for_Groups


class Groups_forma_class(QtWidgets.QMainWindow, Gui_for_Groups.Ui_Group_forma):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Create_btn.clicked.connect(lambda: self.save_in_xml_file_suers('Groups'))
        self.Nazad_btn.clicked.connect(lambda: self.exit_func())

    def exit_func(self):
        self.dumb_clean_func()
        self.close()

    def save_in_xml_file_suers(self, foler):

        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Gate = login.find(foler)

        if login.find(foler).text == None:
            login.find(".//{}".format(foler)).text = '0'

        ET.SubElement(Gate, "{}_{}".format(foler, login.find(".//{}".format(foler)).text), GUI_name=self.G_Name.text(), Gui_Type = self.comboBox.currentText(), Transfer= str(self.G_Transfer.checkState()), G_Forward= str(self.G_Forward.checkState()),
                       G_Conference=str(self.G_Conference.checkState()), G_Call_waiting= str(self.G_Call_waiting.checkState())).text

        login.find('.//{}'.format(foler)).text = str(int(login.find('.//{}'.format(foler)).text) + 1)

        tree = ET.ElementTree(root)
        tree.write("Data\\filename2.xml")
        self.dumb_clean_func()
        self.close()

    def dumb_clean_func(self):
        self.G_Name.setText('')
        self.G_Enabled.setChecked(False)
        self.G_Transfer.setChecked(False)
        self.G_Forward.setChecked(False)
        self.G_Conference.setChecked(False)
        self.G_Call_waiting.setChecked(False)

    def Edit_Services_form_func(self, row, folder):
        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Users = login.find(folder)
        #curreant_User = Users.find('{}_{}'.format(folder, str(row)))

        print('12')

        for type_tag in Users.findall("{}_{}".format(folder, str(row))):
            self.G_Name.setText(type_tag.get('GUI_name'))
            index = self.comboBox.findText(type_tag.get('Gui_Type'))
            if index >= 0:
                self.comboBox.setCurrentIndex(index)

            if int(type_tag.get('Transfer')) == 2:
                self.G_Transfer.setChecked(True)
            else:
                self.G_Transfer.setChecked(False)

            if int(type_tag.get('G_Forward')) == 2:
                self.G_Forward.setChecked(True)
            else:
                self.G_Forward.setChecked(False)

            if int(type_tag.get('G_Conference')) == 2:
                self.G_Conference.setChecked(True)
            else:
                self.G_Conference.setChecked(False)

            if int(type_tag.get('G_Call_waiting')) == 2:
                self.G_Call_waiting.setChecked(True)
            else:
                self.G_Call_waiting.setChecked(False)
