import xml.etree.cElementTree as ET
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidgetItem)
from PyQt5 import QtWidgets
import Gui_for_Routes


class Routes_forma_class(QtWidgets.QMainWindow, Gui_for_Routes.Ui_Routes_forma):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Add_Router_table.clicked.connect(lambda: self.add_row_for_call(self.Routes_forma_Table))
        self.Create_btn.clicked.connect(lambda: self.save_in_xml_file_suers('Routes'))

    def add_row_for_call(self, table):
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)

        btn_del = QtWidgets.QPushButton()

        btn_del.setObjectName('call_del')

        btn_del.setText('Delete')

        table.setCellWidget(rowPosition, 1, btn_del)

        btn_del.clicked.connect(lambda: table.model().removeRow(table.currentIndex().row()))#Удаление строки из таблицы

    def save_in_xml_file_suers(self, foler):

        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Gate = login.find(foler)

        dict_from_codec_and_call = self.Codec_and_call_save_dict_func(self.Routes_forma_Table)

        if login.find(foler).text == None:
            login.find(".//{}".format(foler)).text = '0'

        ET.SubElement(Gate, "{}_{}".format(foler, login.find(".//{}".format(foler)).text), GUI_name=self.Route_name.text(), Gui_command = self.Command_arg.currentText(), Num_call= str(dict_from_codec_and_call['number_call']),
                      Source_Match = self.Source_Match.text(), Source_Pattern = self.Source_Pattern.text(), Source_result = self.Source_result.text(), Source_billing = self.Source_billing.text(),
                      Destination_Match = self.Destination_Match.text(), Destination_Pattern = self.Destination_Pattern.text(), Destination_result = self.Destination_result.text(), Destination_Billing = self.Destination_Billing.text()).text

        Codec_and_call_folder = Gate.find("{}_{}".format(foler, login.find(".//{}".format(foler)).text))

        for i in range(int(dict_from_codec_and_call['number_call'])):
            ET.SubElement(Codec_and_call_folder, 'call_{}'.format(str(i)), Schedule = dict_from_codec_and_call['Schedule_{}'.format(str(i))])

        login.find('.//{}'.format(foler)).text = str(int(login.find('.//{}'.format(foler)).text) + 1)

        tree = ET.ElementTree(root)
        tree.write("data\\filename2.xml")
        self.dumb_clean_func(self.Routes_forma_Table)
        self.close()

    def dumb_clean_func(self, table):
        self.Route_name.setText('')
        self.checkBox.setChecked(False)
        while table.rowCount() > 0:
            table.removeRow(0)

    def Codec_and_call_save_dict_func(self, table):
        dic_for_return = {}
        row_of_call = table.rowCount()
        for row in range(0, row_of_call):
            
            call_0 = table.item(row, 0)
            
            if call_0 != None:
                dic_for_return['Schedule_{}'.format(row)] = (call_0.text())
            else:
                dic_for_return['Schedule_{}'.format(row)] = ''

            #dic_for_return['call_check_{}'.format(str(row))] = (call_0.checkState())

        dic_for_return['number_call'] = row_of_call

        return dic_for_return

    def Edit_Services_form_func(self, row, folder):
        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Users = login.find(folder)
        curreant_User = Users.find('{}_{}'.format(folder, str(row)))

        for type_tag in Users.findall("{}_{}".format(folder, str(row))):
            self.Route_name.setText(type_tag.get('GUI_name'))
            self.Source_Match.setText(type_tag.get('Source_Match'))
            self.Source_Pattern.setText(type_tag.get('Source_Pattern'))
            self.Source_result.setText(type_tag.get('Source_result'))
            self.Source_billing.setText(type_tag.get('Source_billing'))
            self.Destination_Match.setText(type_tag.get('Destination_Match'))
            self.Destination_Pattern.setText(type_tag.get('Destination_Pattern'))
            self.Destination_result.setText(type_tag.get('Destination_result'))
            self.Destination_Billing.setText(type_tag.get('Destination_Billing'))
            index = self.Command_arg.findText(type_tag.get('Gui_command'))
            if index >= 0:
                self.Command_arg.setCurrentIndex(index)

            for i in range(int(type_tag.get('Num_call'))):
                self.add_row_for_call(self.Routes_forma_Table)
                for type_tag_2 in curreant_User.findall("call_{}".format(str(i))):
                    self.Routes_forma_Table.setItem(i, 0, QTableWidgetItem(str(type_tag_2.get('Schedule'))))
                    


