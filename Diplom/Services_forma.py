import xml.etree.cElementTree as ET
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidgetItem)
from PyQt5 import QtWidgets
import Gui_for_services


class Services_forma_class(QtWidgets.QMainWindow, Gui_for_services.Ui_Services_forma):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Add_serv_table.clicked.connect(lambda: self.add_row_for_call(self.Services_forma_Table))
        self.Create_btn.clicked.connect(lambda: self.save_in_xml_file_suers('Services'))
        self.Nazad_btn.clicked.connect(lambda: self.exit_func())

    def exit_func(self):
        self.dumb_clean_func(self.Services_forma_Table)
        self.close()

    def add_row_for_codec(self, table):

        rowPosition = table.rowCount()
        table.insertRow(rowPosition)

        buttons_del = QtWidgets.QPushButton()
        combo = QtWidgets.QComboBox()

        buttons_del.setText('Delete')
        combo.addItem("PyQt")
        combo.addItem("exp")

        table.setCellWidget(rowPosition, 5, buttons_del)

    def add_row_for_call(self, table):
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)

        check = QtWidgets.QCheckBox()
        combo = QtWidgets.QComboBox()
        btn_del = QtWidgets.QPushButton()

        check.setObjectName('call_check_' + str(rowPosition))
        combo.setObjectName('call_cbox_' + str(rowPosition))
        btn_del.setObjectName('call_del')

        check.setChecked(True)
        combo.addItem("PyQt")
        combo.addItem("exp")
        btn_del.setText('Delete')

        table.setCellWidget(rowPosition, 0, check)
        table.setCellWidget(rowPosition, 1, combo)
        table.setCellWidget(rowPosition, 5, btn_del)

        btn_del.clicked.connect(lambda: table.model().removeRow(table.currentIndex().row()))#Удаление строки из таблицы

    def save_in_xml_file_suers(self, foler):

        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Gate = login.find(foler)

        dict_from_codec_and_call = self.Codec_and_call_save_dict_func(self.Services_forma_Table)

        if login.find(foler).text == None:
            login.find(".//{}".format(foler)).text = '0'

        ET.SubElement(Gate, "{}_{}".format(foler, login.find(".//{}".format(foler)).text), GUI_name=self.Services_SerName.text(), Gui_command = self.Services_command.currentText(), Num_call= str(dict_from_codec_and_call['number_call'])).text

        Codec_and_call_folder = Gate.find("{}_{}".format(foler, login.find(".//{}".format(foler)).text))


        for i in range(int(dict_from_codec_and_call['number_call'])):
            ET.SubElement(Codec_and_call_folder, 'call_{}'.format(str(i)), call_Source = dict_from_codec_and_call['call_Source_{}'.format(str(i))],
                          call_Ashedule = dict_from_codec_and_call['call_Ashedule_{}'.format(str(i))], call_FwdN = dict_from_codec_and_call['call_FwdN_{}'.format(str(i))],
                          call_check = str(dict_from_codec_and_call['call_check_{}'.format(str(i))]), call_FwdC= dict_from_codec_and_call['call_FwdC_{}'.format(str(i))])

        login.find('.//{}'.format(foler)).text = str(int(login.find('.//{}'.format(foler)).text) + 1)

        tree = ET.ElementTree(root)
        tree.write("data\\filename2.xml")
        self.dumb_clean_func(self.Services_forma_Table)
        self.close()

    def dumb_clean_func(self, table):
        self.Services_SerName.setText('')
        self.Services_enabled_check.setChecked(False)
        while table.rowCount() > 0:
            table.removeRow(0)

    def Codec_and_call_save_dict_func(self, table):
        dic_for_return = {}
        row_of_call = table.rowCount()
        for row in range(0, row_of_call):
            call_0 = table.cellWidget(row, 0)
            call_1 = table.cellWidget(row, 1)
            call_2 = table.item(row, 2)
            call_3 = table.item(row, 3)
            call_4 = table.item(row, 4)
            if call_2 != None:
                dic_for_return['call_Source_{}'.format(row)] = (call_2.text())
            else:
                dic_for_return['call_Source_{}'.format(row)] = ''

            if call_3 != None:
                dic_for_return['call_Ashedule_{}'.format(row)] = (call_3.text())
            else:
                dic_for_return['call_Ashedule_{}'.format(str(row))] = ''

            if call_4 != None:
                dic_for_return['call_FwdN_{}'.format(row)] = (call_4.text())
            else:
                dic_for_return['call_FwdN_{}'.format(str(row))] = ''

            dic_for_return['call_check_{}'.format(str(row))] = (call_0.checkState())
            dic_for_return['call_FwdC_{}'.format(str(row))] = (call_1.currentText())

        dic_for_return['number_call'] = row_of_call

        return dic_for_return

    def Edit_Services_form_func(self, row, folder):
        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Users = login.find(folder)
        curreant_User = Users.find('{}_{}'.format(folder, str(row)))

        for type_tag in Users.findall("{}_{}".format(folder, str(row))):
            self.Services_SerName.setText(type_tag.get('GUI_name'))
            index = self.Services_command.findText(type_tag.get('Gui_command'))
            if index >= 0:
                self.Services_command.setCurrentIndex(index)

            for i in range(int(type_tag.get('Num_call'))):
                self.add_row_for_call(self.Services_forma_Table)
                for type_tag_2 in curreant_User.findall("call_{}".format(str(i))):
                    call = self.Services_forma_Table.cellWidget(i, 1)
                    index = call.findText(type_tag_2.get('call_FwdC'))
                    if index >= 0:
                        call.setCurrentIndex(index)
                    self.Services_forma_Table.setItem(i, 2, QTableWidgetItem(str(type_tag_2.get('call_Source'))))
                    self.Services_forma_Table.setItem(i, 3, QTableWidgetItem(str(type_tag_2.get('call_Ashedule'))))
                    self.Services_forma_Table.setItem(i, 4, QTableWidgetItem(str(type_tag_2.get('call_FwdN'))))
                    call_che = self.Services_forma_Table.cellWidget(i, 0)
                    if int(type_tag_2.get('call_check')) == 2:
                        call_che.setChecked(True)
                    else:
                        call_che.setChecked(False)

