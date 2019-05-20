import xml.etree.cElementTree as ET
import Gui_users_reg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidgetItem)
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox


class Users_reg_class(QtWidgets.QMainWindow, Gui_users_reg.Ui_Users_create):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.gur_Registration.currentIndexChanged.connect(lambda: self.Reg_func())
        self.Create_btn.clicked.connect(lambda: self.save_in_xml_file_suers())
        self.Add_Codec_btn.clicked.connect(lambda: self.add_row_for_codec())
        self.Add_call_table_btn.clicked.connect(lambda: self.add_row_for_call())
        self.Nazad_btn.clicked.connect(lambda: self.check_for_registration())

    def Reg_func(self):
        print(self.gur_Registration.currentText())
        if self.gur_Registration.currentText() == 'Enabled':
            self.gur_Login.setEnabled(True)
            self.gur_Password.setEnabled(True)
            self.gur_TTL.setEnabled(True)
            self.gur_IP_Address.setEnabled(True)
            self.gur_IP_port.setEnabled(True)
        elif self.gur_Registration.currentText() == 'Disabled':
            self.gur_Login.setEnabled(False)
            self.gur_Password.setEnabled(False)
            self.gur_TTL.setEnabled(False)
            self.gur_IP_Address.setEnabled(True)
            self.gur_IP_port.setEnabled(True)
        else:
            self.gur_Login.setEnabled(True)
            self.gur_Password.setEnabled(True)
            self.gur_TTL.setEnabled(True)
            self.gur_IP_Address.setEnabled(False)
            self.gur_IP_port.setEnabled(False)

    def delete_row(self, call_or_codex):
        if call_or_codex:
            Index = self.Codec_Table.currentIndex()
            self.Codec_Table.model().removeRow(Index.row())
        else:
            Index = self.Call_Table.currentIndex()
            self.Call_Table.model().removeRow(Index.row())

    def save_in_xml_file_suers(self):

        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Users = login.find('Users')

        if login.find('Users').text == None:
            login.find(".//Users").text = '0'

        dict_from_codec_and_call = self.Codec_and_call_save_dict_func()
        print(dict_from_codec_and_call['number_codec'])

        ET.SubElement(Users, "Users_{}".format(login.find(".//Users").text), GUI_name=self.gur_User_name.text(), gur_Phone_num = self.gur_Phone_num.text(), gur_Signaling = self.gur_Signaling.text(), GUI_IP_Address = self.gur_IP_Address.text(),
                      gur_IP_port=self.gur_IP_port.text(), gur_Email=self.gur_Email.text(), gur_Pin_code = self.gur_Pin_code.text(), gur_Web_password = self.gur_Web_password.text(), gur_TTL = self.gur_TTL.text(),
                      gur_NAT=self.gur_NAT.text(), gur_Fax=self.gur_Fax.text(), gur_Convert=self.gur_Convert.text(), gur_Repacketize=self.gur_Repacketize.text(), gur_DTMF=self.gur_DTMF.text(), gur_Connect=self.gur_Connect.text(),
                      gur_RBT=self.gur_RBT.text(), gur_Tone=self.gur_Tone.text(), gur_Sip=self.gur_Sip.text(), gur_Password=self.gur_Password.text(), gur_Login=self.gur_Login.text(), gur_noproxy=self.gur_noproxy.text(),
                      ODL_dis = self.comboBox.currentText(), gur_Registration = self.gur_Registration.currentText(), Num_codec= str(dict_from_codec_and_call['number_codec']), Num_call= str(dict_from_codec_and_call['number_call'])).text

        Codec_and_call_folder = Users.find("Users_{}".format(login.find(".//Users").text))

        for i in range(int(dict_from_codec_and_call['number_codec'])):
            ET.SubElement(Codec_and_call_folder, "codec_{}".format(str(i)), codec_FFP = dict_from_codec_and_call['codec_FFP_{}'.format(str(i))], codec_codec = dict_from_codec_and_call['codec_codec_{}'.format(str(i))])

        for i in range(int(dict_from_codec_and_call['number_call'])):
            ET.SubElement(Codec_and_call_folder, 'call_{}'.format(str(i)), call_Source = dict_from_codec_and_call['call_Source_{}'.format(str(i))],
                          call_Ashedule = dict_from_codec_and_call['call_Ashedule_{}'.format(str(i))], call_FwdN = dict_from_codec_and_call['call_FwdN_{}'.format(str(i))],
                          call_check = str(dict_from_codec_and_call['call_check_{}'.format(str(i))]), call_FwdC= dict_from_codec_and_call['call_FwdC_{}'.format(str(i))])

        login.find('.//Users').text = str(int(login.find('.//Users').text) + 1)

        tree = ET.ElementTree(root)
        tree.write("data\\filename2.xml")
        self.dumb_clean_func()
        self.close()

    def add_row_for_codec(self):

        rowPosition = self.Codec_Table.rowCount()
        self.Codec_Table.insertRow(rowPosition)

        buttons_del = QtWidgets.QPushButton()
        combo = QtWidgets.QComboBox()

        #buttons_del.setObjectName('Codec_del_' + str(rowPosition))
        #combo.setObjectName('cbox_' + str(rowPosition))

        buttons_del.setText('Delete')
        combo.addItem("PyQt")
        combo.addItem("exp")

        self.Codec_Table.setCellWidget(rowPosition, 2, buttons_del)
        self.Codec_Table.setCellWidget(rowPosition, 0, combo)

        buttons_del.clicked.connect(lambda: self.delete_row(True))

    def add_row_for_call(self):
        rowPosition = self.Call_Table.rowCount()
        self.Call_Table.insertRow(rowPosition)

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

        self.Call_Table.setCellWidget(rowPosition, 0, check)
        self.Call_Table.setCellWidget(rowPosition, 1, combo)
        self.Call_Table.setCellWidget(rowPosition, 5, btn_del)

        btn_del.clicked.connect(lambda: self.delete_row(False))
        #self.check.stateChanged.connect(lambda: print(rowPosition))

    def Codec_and_call_save_dict_func(self):
        dic_for_return = {}
        row_of_codec = self.Codec_Table.rowCount()
        row_of_call = self.Call_Table.rowCount()
        for row in range(0, row_of_codec):
            codec0 = self.Codec_Table.cellWidget(row, 0)
            codec1 = self.Codec_Table.item(row, 1)
            if codec1 != None:
                dic_for_return['codec_FFP_{}'.format(str(row))] = str(codec1.text())
            else:
                dic_for_return['codec_FFP_{}'.format(str(row))] = ''
            dic_for_return['codec_codec_{}'.format(str(row))] = str(codec0.currentText())
        for row in range(0, row_of_call):
            call_0 = self.Call_Table.cellWidget(row, 0)
            call_1 = self.Call_Table.cellWidget(row, 1)
            call_2 = self.Call_Table.item(row, 2)
            call_3 = self.Call_Table.item(row, 3)
            call_4 = self.Call_Table.item(row, 4)
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

        dic_for_return['number_codec'] = row_of_codec
        dic_for_return['number_call'] = row_of_call

        return dic_for_return

    def check_for_registration(self):#Оставленна на потом REG == ip adress IP Port, dis == login password TTL
        if self.gur_Registration.currentText() == 'Enabled':
            print('1')
        elif self.gur_Registration.currentText() == 'Required':
            print('2')
        else:
            print('3')


    def Edit_reg_form_func(self, row):
        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Users = login.find('Users')
        curreant_User = Users.find('Users_{}'.format(str(row)))

        for type_tag in Users.findall("Users_{}".format(str(row))):
            self.gur_User_name.setText(type_tag.get('GUI_name'))
            self.gur_Phone_num.setText(type_tag.get('gur_Phone_num'))
            self.gur_Signaling.setText(type_tag.get('gur_Signaling'))
            self.gur_IP_Address.setText(type_tag.get('GUI_IP_Address'))
            self.gur_IP_port.setText(type_tag.get('gur_IP_port'))
            self.gur_Email.setText(type_tag.get('gur_Email'))
            self.gur_Pin_code.setText(type_tag.get('gur_Pin_code'))
            self.gur_Web_password.setText(type_tag.get('gur_Web_password'))
            self.gur_Login.setText(type_tag.get('gur_Login'))
            self.gur_Password.setText(type_tag.get('gur_Password'))
            self.gur_TTL.setText(type_tag.get('gur_TTL'))
            self.gur_NAT.setText(type_tag.get('gur_NAT'))
            self.gur_Fax.setText(type_tag.get('gur_Fax'))
            self.gur_Convert.setText(type_tag.get('gur_Convert'))
            self.gur_Repacketize.setText(type_tag.get('gur_Repacketize'))
            self.gur_DTMF.setText(type_tag.get('gur_DTMF'))
            self.gur_Connect.setText(type_tag.get('gur_Connect'))
            self.gur_Tone.setText(type_tag.get('gur_Tone'))
            self.gur_Sip.setText(type_tag.get('gur_Sip'))
            self.gur_noproxy.setText(type_tag.get('gur_noproxy'))
            self.gur_RBT.setText(type_tag.get('gur_RBT'))
            index = self.comboBox.findText(type_tag.get('ODL_dis'))
            if index >= 0:
                self.comboBox.setCurrentIndex(index)
            index = self.gur_Registration.findText(type_tag.get('gur_Registration'))
            if index >= 0:
                self.gur_Registration.setCurrentIndex(index)

            for i in range(int(type_tag.get('Num_codec'))):
                self.add_row_for_codec()
                for type_tag_2 in curreant_User.findall("codec_{}".format(str(i))):
                    codec = self.Codec_Table.cellWidget(i, 0)
                    index = codec.findText(type_tag_2.get('codec_codec'))
                    if index >= 0:
                        codec.setCurrentIndex(index)
                    self.Codec_Table.setItem(i, 1, QTableWidgetItem(str(type_tag_2.get('codec_FFP'))))

            for i in range(int(type_tag.get('Num_call'))):
                self.add_row_for_call()
                for type_tag_2 in curreant_User.findall("call_{}".format(str(i))):
                    call = self.Call_Table.cellWidget(i, 1)
                    index = call.findText(type_tag_2.get('call_FwdC'))
                    if index >= 0:
                        call.setCurrentIndex(index)
                    self.Call_Table.setItem(i, 2, QTableWidgetItem(str(type_tag_2.get('call_Source'))))
                    self.Call_Table.setItem(i, 3, QTableWidgetItem(str(type_tag_2.get('call_Ashedule'))))
                    self.Call_Table.setItem(i, 4, QTableWidgetItem(str(type_tag_2.get('call_FwdN'))))
                    call_che = self.Call_Table.cellWidget(i, 0)
                    if int(type_tag_2.get('call_check')) == 2:
                        call_che.setChecked(True)
                    else:
                        call_che.setChecked(False)


    def dumb_clean_func(self):
        self.gur_User_name.setText('')
        self.gur_Phone_num.setText('')
        self.gur_Signaling.setText('')
        self.gur_IP_Address.setText('')
        self.gur_IP_port.setText('')
        self.gur_Email.setText('')
        self.gur_Pin_code.setText('')
        self.gur_Web_password.setText('')
        self.gur_Login.setText('')
        self.gur_Password.setText('')
        self.gur_TTL.setText('')
        self.gur_NAT.setText('')
        self.gur_Fax.setText('')
        self.gur_Convert.setText('')
        self.gur_Repacketize.setText('')
        self.gur_DTMF.setText('')
        self.gur_Connect.setText('')
        self.gur_RBT.setText('')
        self.gur_Tone.setText('')
        self.gur_Sip.setText('')
        self.gur_noproxy.setText('')
        while self.Call_Table.rowCount() > 0:
            self.Call_Table.removeRow(0)
        while self.Codec_Table.rowCount() > 0:
            self.Codec_Table.removeRow(0)





