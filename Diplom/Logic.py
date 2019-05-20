import xml.etree.cElementTree as ET
import sys
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QWidget,QLineEdit, QGridLayout)
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidgetItem, QRadioButton)
from pygame import mixer
import Gui_for_main, Users_reg_forma, Gateways_forma, Services_forma, Routes_forma, Group_forma




class Save_class(QtWidgets.QMainWindow, Gui_for_main.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Save_btn.clicked.connect(lambda: self.Save_in_xml_file())
        self.Load_btn.clicked.connect(lambda: self.Load_func())
        self.Add_btn.clicked.connect(lambda: self.NTP_server.append(self.Add_string.text()))
        self.Rad_Add_server_btn.clicked.connect(lambda: self.Rad_Server_auth.append(self.Add_string_2.text()))
        self.Del_btn.clicked.connect(lambda: self.NTP_server.clear())
        self.Rad_Add_server_btn_2.clicked.connect(lambda: self.Rad_Server_auth.clear())
        self.Use_NTP.stateChanged.connect(lambda: self.NTP_Change())
        self.Users_edit_btn.clicked.connect(lambda: self.Users_reg.show())
        self.Edit_Radio.toggled.connect(lambda: self.change_btn_radio_btn(self.Users_table, 'Users', self.Edit_Radio))
        self.Edit_Radio_2.toggled.connect(lambda: self.change_btn_radio_btn(self.Gateways_table, 'Gate', self.Edit_Radio_2))
        self.Edit_Radio_3.toggled.connect(lambda: self.change_btn_radio_btn(self.Services_Table, 'Services', self.Edit_Radio_3))
        self.Edit_Radio_4.toggled.connect(lambda: self.change_btn_radio_btn(self.Routes_Table, 'Routes', self.Edit_Radio_4))
        self.Edit_Radio_5.toggled.connect(lambda: self.change_btn_radio_btn(self.Groups_Table, 'Groups', self.Edit_Radio_5))
        self.Edit_Radio_6.toggled.connect(lambda: self.change_btn_radio_btn(self.Prompts_Table, 'Prompts', self.Edit_Radio_6))
        self.Edit_Radio_7.toggled.connect(lambda: self.change_btn_radio_btn(self.Update_Table, 'Update', self.Edit_Radio_7))
        self.Users_reg = Users_reg_forma.Users_reg_class()
        self.Users_reg.Create_btn.clicked.connect(lambda: self.Load_table("Users", self.Users_table, self.Edit_Radio))
        self.Gate_forma = Gateways_forma.Gate_forma_class()
        self.Gateways_Add_btn.clicked.connect(lambda: self.Gate_forma.show())
        self.Gate_forma.create_btn.clicked.connect(lambda: self.Load_table('Gate', self.Gateways_table, self.Edit_Radio_2))
        self.Born_To_Serve = Services_forma.Services_forma_class()
        self.Born_To_Serve.Create_btn.clicked.connect(lambda: self.Load_table('Services', self.Services_Table, self.Edit_Radio_3))
        self.Services_Add_btn.clicked.connect(lambda: self.Born_To_Serve.show())
        self.routes_form = Routes_forma.Routes_forma_class()
        self.Routes_Add_btn.clicked.connect(lambda: self.routes_form.show())
        self.routes_form.Create_btn.clicked.connect(lambda: self.Load_table('Routes', self.Routes_Table, self.Edit_Radio_4))
        self.Groups = Group_forma.Groups_forma_class()
        self.Groups_Add_btn.clicked.connect(lambda: self.Groups.show())
        self.Groups.Create_btn.clicked.connect(lambda: self.Load_table('Groups', self.Groups_Table, self.Edit_Radio_5))
        self.Pro_Choose_path_btn.clicked.connect(lambda: self.Pro_Upload_prompt.setText(self.openFileNameDialog('.mp3')))
        self.Update_Choose_path_btn.clicked.connect(lambda: self.Update_Upload_prompt.setText(self.openFileNameDialog('')))
        self.Pro_Upload_btn.clicked.connect(lambda: self.Save_in_xml('Prompts', self.Prompts_Table, self.Edit_Radio_6))
        self.Update_Upload_btn.clicked.connect(lambda: self.Save_in_xml('Update', self.Update_Table, self.Edit_Radio_7))

    def openFileNameDialog(self, file_format):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*{})".format(file_format), options=options)
        if fileName:
            return (fileName)

    def Save_in_xml(self, folder, main_table, radio_btn):
        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Gate = login.find(folder)

        if login.find(folder).text == None:
            login.find(".//{}".format(folder)).text = '0'

        ET.SubElement(Gate, "{}_{}".format(folder, login.find(".//{}".format(folder)).text),
                      Upload=self.Pro_Upload_prompt.text(), Pro_Name=self.Pro_Name.text(), GUI_name=self.Update_Name.text()).text

        login.find('.//{}'.format(folder)).text = str(int(login.find('.//{}'.format(folder)).text) + 1)

        tree = ET.ElementTree(root)
        tree.write("data\\filename2.xml")
        self.Load_table(folder, main_table, radio_btn)

    def change_btn_radio_btn(self, main_table, text, radio_btn):
        rowPosition = main_table.rowCount()
        for i in range(rowPosition):
            child = self.findChild(QPushButton, "{}_Edit_btn_{}".format(text, i))
            child.setText(self.radio_btn_users_del_edi(radio_btn))

    def radio_btn_users_del_edi(self, rad_btn):

        if rad_btn.isChecked():
            return rad_btn.text()
        else:
            return 'Delete'

    def NTP_Change(self):
        if self.Use_NTP.isChecked():
            self.TimeZone.setEnabled(True)
            self.NTP_server.setEnabled(True)
            self.Add_string.setEnabled(True)
            self.Add_btn.setEnabled(True)
            self.Del_btn.setEnabled(True)

        else:
            self.TimeZone.setEnabled(False)
            self.NTP_server.setEnabled(False)
            self.Add_string.setEnabled(False)
            self.Add_btn.setEnabled(False)
            self.Del_btn.setEnabled(False)

    def Save_in_xml_file(self):

        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)

        massiv_of_main_save = ['Configuration', 'Radius', 'logs']

        for i in range(len(massiv_of_main_save)):
            for users in login.findall(massiv_of_main_save[i]):
                login.remove(users)

        ET.SubElement(login, "Configuration", IP_address_WAN = self.IP_address_WAN.text(), Netmask = self.Netmask.text(), Default_Gateway = self.Default_Gateway.text(), Hostname = self.Hostname.text(),
                      Domain = self.Domain.text(), DNS=self.DNS.text(), SSI = self.SSI.currentText(), IP_address_SMTP = self.IP_address_SMTP.text(), Port = self.Port.text(), Source = self.Source.text(),
                      Name_SIP=self.Name_SIP.text(), Unicast_port = self.Unicast_port.text(), Multicast_port_SMTP = self.Multicast_port_SMTP.text(), Multicast_port_gatekeeper = self.Multicast_port_gatekeeper.text(), Unicast = self.Unicast.text(),
                      Name_gatekeeper = self.Name_gatekeeper.text(), Confirm_password = self.Confirm_password.text(), New_password = self.New_password.text(), Old_password = self.Old_password.text(),
                      Time_hh = self.Time_hh.text(), Time_mm = self.Time_mm.text(), Date_dd = self.Date_dd.text(), Date_mm = self.Date_mm.text(), Date_yyyy = self.Date_yyyy.text(), TimeZone = self.TimeZone.currentText(),
                      NTP_server = self.NTP_server.toPlainText(), Use_NTP = str(self.Use_NTP.checkState()), Use_DHCP = str(self.Use_DHCP.checkState())).text

        ET.SubElement(login, 'Radius', Rad_Secret = self.Rad_Secret.text(), Reg_Retransmission_count=self.Reg_Retransmission_count.text(), Rad_Retransmission_interval= self.Rad_Retransmission_interval.text(),
                      Rad_Interim_msg_send_interval=self.Rad_Interim_msg_send_interval.text(), Rad_Max_call_time= self.Rad_Max_call_time.text(), Rad_Service_type= self.Rad_Service_type.text(), Rad_Framed_protocol=self.Rad_Framed_protocol.text(),
                      Rad_Nas_IP=self.Rad_Nas_IP.text(), Rad_Server_auth = self.Rad_Server_auth.toPlainText(), Rad_Ecb = str(self.Rad_Ecb.checkState()), Rad_Disc = str(self.Rad_Disc.checkState()), Rad_Auth_reg = str(self.Rad_Auth_reg.checkState()),
                      Rad_Auth_call= str(self.Rad_Auth_call.checkState()), Rad_send_boot=str(self.Rad_send_boot.checkState()), Rad_Send_accounting=str(self.Rad_Send_accounting.checkState()), Rad_Send_interim=str(self.Rad_Send_interim.checkState()),
                      Rad_Cisco_comp=str(self.Rad_Cisco_comp.checkState()), Rad_Send_called=str(self.Rad_Send_called.checkState()))

        ET.SubElement(login, 'logs', Logs_Keep_log=self.Logs_Keep_log.text(), Logs_Keep_User=self.Logs_Keep_User.text(), Logs_Keep_Admin=self.Logs_Keep_Admin.text(), Logs_Email_CDB=self.Logs_Email_CDB.text())

        tree = ET.ElementTree(root)
        tree.write("data\\filename2.xml")

    def Load_func(self):

        root = ET.parse('Data\\filename2.xml').getroot()

        login = root.find(root.find('Login_folder').text)

        self.NTP_server.clear()
        self.Rad_Server_auth.clear()

        for type_tag in login.findall('Configuration'):
            self.IP_address_WAN.setText(type_tag.get('IP_address_WAN'))
            self.NTP_server.append(type_tag.get('NTP_server'))
            self.Netmask.setText(type_tag.get('Netmask'))
            self.Default_Gateway.setText(type_tag.get('Default_Gateway'))
            self.Hostname.setText(type_tag.get('Hostname'))
            self.Domain.setText(type_tag.get('Domain'))
            self.DNS.setText(type_tag.get('DNS'))
            self.IP_address_SMTP.setText(type_tag.get('IP_address_SMTP'))
            self.Port.setText(type_tag.get('Port'))
            self.Source.setText(type_tag.get('Source'))
            self.Name_SIP.setText(type_tag.get('Name_SIP'))
            self.Unicast_port.setText(type_tag.get('Unicast_port'))
            self.Multicast_port_SMTP.setText(type_tag.get('Multicast_port_SMTP'))
            self.Multicast_port_gatekeeper.setText(type_tag.get('Multicast_port_gatekeeper'))
            self.Unicast.setText(type_tag.get('Unicast'))
            self.Name_gatekeeper.setText(type_tag.get('Name_gatekeeper'))
            self.Confirm_password.setText(type_tag.get('Confirm_password'))
            self.New_password.setText(type_tag.get('New_password'))
            self.Old_password.setText(type_tag.get('Old_password'))
            try:
                self.Time_hh.setValue(int(type_tag.get('Time_hh')))
                self.Time_mm.setValue(int(type_tag.get('Time_mm')))
                self.Date_dd.setValue(int(type_tag.get('Date_dd')))
                self.Date_mm.setValue(int(type_tag.get('Date_mm')))
                self.Date_yyyy.setValue(int(type_tag.get('Date_yyyy')))
            except:
                print('312312')
            index = self.SSI.findText(type_tag.get('SSI'))
            if index >= 0:
                self.SSI.setCurrentIndex(index)
            index = self.TimeZone.findText(type_tag.get('TimeZone'))
            if index >= 0:
                self.TimeZone.setCurrentIndex(index)
            if int(type_tag.get('Use_NTP')) == 0:
                self.Use_NTP.setChecked(False)
            else:
                self.Use_NTP.setChecked(True)

        for type_tag in login.findall('Radius'):
            self.Rad_Secret.setText(type_tag.get('Rad_Secret'))
            self.Reg_Retransmission_count.setText(type_tag.get('Reg_Retransmission_count'))
            self.Rad_Retransmission_interval.setText(type_tag.get('Rad_Retransmission_interval'))
            self.Rad_Interim_msg_send_interval.setText(type_tag.get('Rad_Interim_msg_send_interval'))
            self.Rad_Max_call_time.setText(type_tag.get('Rad_Max_call_time'))
            self.Rad_Service_type.setText(type_tag.get('Rad_Service_type'))
            self.Rad_Framed_protocol.setText(type_tag.get('Rad_Framed_protocol'))
            self.set_check_state_func(type_tag.get('Rad_Ecb'), self.Rad_Ecb)
            self.set_check_state_func(type_tag.get('Rad_Disc'), self.Rad_Disc)
            self.set_check_state_func(type_tag.get('Rad_Auth_reg'), self.Rad_Auth_reg)
            self.set_check_state_func(type_tag.get('Rad_Auth_call'), self.Rad_Auth_call)
            self.set_check_state_func(type_tag.get('Rad_send_boot'), self.Rad_send_boot)
            self.set_check_state_func(type_tag.get('Rad_Send_accounting'), self.Rad_Send_accounting)
            self.set_check_state_func(type_tag.get('Rad_Send_interim'), self.Rad_Send_interim)
            self.set_check_state_func(type_tag.get('Rad_Cisco_comp'), self.Rad_Cisco_comp)
            self.set_check_state_func(type_tag.get('Rad_Send_called'), self.Rad_Send_called)

        for type_tag in login.findall('logs'):
            print('32')
            self.Logs_Keep_log.setText(type_tag.get('Logs_Keep_log'))
            self.Logs_Keep_User.setText(type_tag.get('Logs_Ke'))
            self.Logs_Keep_Admin.setText(type_tag.get('Logs_Keep_Admin'))
            self.Logs_Email_CDB.setText(type_tag.get('Logs_Email_CDB'))

        self.Load_table("Users", self.Users_table, self.Edit_Radio)
        self.Load_table("Gate", self.Gateways_table, self.Edit_Radio_2)
        self.Load_table("Services", self.Services_Table, self.Edit_Radio_3)
        self.Load_table("Routes", self.Routes_Table, self.Edit_Radio_4)
        self.Load_table("Groups", self.Groups_Table, self.Edit_Radio_5)
        self.Load_table("Prompts", self.Prompts_Table, self.Edit_Radio_6)
        self.Load_table("Update", self.Update_Table, self.Edit_Radio_7)

    def set_check_state_func(self, text, check):
        if int(text) == 0:
            check.setChecked(False)
        else:
            check.setChecked(True)
            





            #self.Load_user_table()

    def Edit_user_btn_func_2(self):
        self.Users_reg.show()
        self.Users_reg.Edit_reg_form_func(self.Users_table.currentIndex().row())

    def Load_table(self, folder_from_login_to, main_table, radio_btn):

        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Users = login.find('{}'.format(folder_from_login_to))

        headercount = main_table.columnCount()

        while main_table.rowCount() > 0:
            main_table.removeRow(0)

        for row in range(len(Users.getchildren())):

            buttons = QtWidgets.QPushButton(self.radio_btn_users_del_edi(radio_btn))
            buttons.setObjectName("{}_Edit_btn_".format(folder_from_login_to) + str(row))

            buttons.clicked.connect(lambda: self.delete_row(main_table, radio_btn, folder_from_login_to, radio_btn))

            Table_radio_btn = QRadioButton("")
            Table_radio_btn.setEnabled(False)
            #Table_radio_btn.setChecked(True)
            #Table_radio_btn.toggled.connect(lambda: self.Activ())

            check = QtWidgets.QCheckBox()
            check.setObjectName('{}_check_'.format(folder_from_login_to) + str(row))
            rowPosition = main_table.rowCount()

            for type_tag in Users.findall('{}_{}'.format(folder_from_login_to, row)):
                phone_tag = type_tag.get('gur_Phone_num')
                name_tag = type_tag.get('GUI_name')
                Address_tag = type_tag.get('GUI_IP_Address')

            main_table.insertRow(rowPosition)

            for x in range(0, headercount, 1):
                if main_table.horizontalHeaderItem(x).text() == 'Enabled':
                    main_table.setCellWidget(row, x, check)
                elif main_table.horizontalHeaderItem(x).text() == 'Name':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('GUI_name'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Address':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('GUI_IP_Address'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Action':
                    main_table.setCellWidget(row, x, buttons)
                elif main_table.horizontalHeaderItem(x).text() == 'Phone':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('gur_Phone_num'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Command':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('Gui_command'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Match':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('Source_billing')) + '\\' + str(type_tag.get('Destination_Billing'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Pattern':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('Source_Pattern')) + '\\' + str(type_tag.get('Destination_Pattern'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Result':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('Source_result')) + '\\' + str(type_tag.get('Destination_result'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Criteria':
                    main_table.setItem(row, x, QTableWidgetItem(str(type_tag.get('Source_Match')) + '\\' + str(type_tag.get('Destination_Match'))))
                elif main_table.horizontalHeaderItem(x).text() == 'Transfer':
                    if str(type_tag.get('Transfer')) == '2':
                        main_table.setItem(row, x, QTableWidgetItem('True'))
                    else:
                        main_table.setItem(row, x, QTableWidgetItem('False'))
                elif main_table.horizontalHeaderItem(x).text() == 'Forward':
                    if str(type_tag.get('G_Forward')) == '2':
                        main_table.setItem(row, x, QTableWidgetItem('True'))
                    else:
                        main_table.setItem(row, x, QTableWidgetItem('False'))
                elif main_table.horizontalHeaderItem(x).text() == 'Conference':
                    if str(type_tag.get('G_Conference')) == '2':
                        main_table.setItem(row, x, QTableWidgetItem('True'))
                    else:
                        main_table.setItem(row, x, QTableWidgetItem('False'))
                elif main_table.horizontalHeaderItem(x).text() == 'Call waiting':
                    if str(type_tag.get('G_Call_waiting')) == '2':
                        main_table.setItem(row, x, QTableWidgetItem('True'))
                    else:
                        main_table.setItem(row, x, QTableWidgetItem('False'))
                elif main_table.horizontalHeaderItem(x).text() == 'Type':
                    main_table.setItem(row, x, QTableWidgetItem(type_tag.get('Gui_Type')))
                elif main_table.horizontalHeaderItem(x).text() == 'Prompt name':
                    main_table.setItem(row, x, QTableWidgetItem(type_tag.get('Pro_Name')))
                elif main_table.horizontalHeaderItem(x).text() == 'Date':
                    main_table.setItem(row, x, QTableWidgetItem(str(datetime.datetime.now())))
                elif main_table.horizontalHeaderItem(x).text() == 'Active':
                    main_table.setCellWidget(row, x, Table_radio_btn)

    def delete_row(self, main_table, radio, folder_from_login_to, radio_btn):
        if self.radio_btn_users_del_edi(radio) == 'Delete':

            Index = main_table.currentIndex()

            row = int(main_table.rowCount()) - 1

            root = ET.parse('Data\\filename2.xml').getroot()
            login = root.find(root.find('Login_folder').text)
            Users = login.find(folder_from_login_to)

            for element in Users.findall('{}_{}'.format(folder_from_login_to, Index.row())):
                Users.remove(element)

            i = Index.row()
            while i < int(row):
                for element in Users.iter('{}_{}'.format(folder_from_login_to, i + 1)):
                    element.tag = str('{}_{}'.format(folder_from_login_to, i))
                i = i + 1

            login.find('.//{}'.format(folder_from_login_to)).text = str(int(login.find('.//{}'.format(folder_from_login_to)).text) - 1)

            tree = ET.ElementTree(root)
            tree.write("data\\filename2.xml")

            self.Load_table(folder_from_login_to, main_table, radio_btn)
        else:
            self.Edit_btn_func(folder_from_login_to)

    def Edit_btn_func(self, folder):
        if folder == 'Users':
            self.Users_reg.show()
            self.Users_reg.Edit_reg_form_func(self.Users_table.currentIndex().row())
        elif folder == "Gate":
            self.Gate_forma.show()
            self.Gate_forma.Edit_Gate_form_func(self.Gateways_table.currentIndex().row())
        elif folder == "Services":
            self.Born_To_Serve.show()
            self.Born_To_Serve.Edit_Services_form_func(self.Services_Table.currentIndex().row(), 'Services')
        elif folder == "Routes":
            self.routes_form.show()
            self.routes_form.Edit_Services_form_func(self.Routes_Table.currentIndex().row(), 'Routes')
        elif folder == "Groups":
            self.Groups.show()
            self.Groups.Edit_Services_form_func(self.Groups_Table.currentIndex().row(), 'Groups')
        elif folder == "Update":
            rad_t = self.Update_Table.cellWidget(self.Update_Table.currentIndex().row(), 0)
            rad_t.setChecked(True)
            QtWidgets.QMessageBox.information(
                self, 'Error', 'Update is Active')
        elif folder == 'Prompts':
            root = ET.parse('Data\\filename2.xml').getroot()
            login = root.find(root.find('Login_folder').text)
            Gate = login.find('Prompts')

            for type_tag in Gate.findall('Prompts_{}'.format(self.Prompts_Table.currentIndex().row())):
                try:
                    mixer.init()
                    mixer.music.load(type_tag.get('Upload'))
                    mixer.music.play()
                except:
                    QtWidgets.QMessageBox.information(
                        self, 'Error', 'Record is corrapted. Please rewrite record.')

            tree = ET.ElementTree(root)
            tree.write("Data\\filename2.xml")

    def test(self):
        self.Edit_Radio_6.setText()