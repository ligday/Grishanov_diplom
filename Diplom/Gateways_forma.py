import xml.etree.cElementTree as ET
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidgetItem)
from PyQt5 import QtWidgets
import Gui_for_Gateway


class Gate_forma_class(QtWidgets.QMainWindow, Gui_for_Gateway.Ui_Gateway_forma):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Gateways_add_btn.clicked.connect(lambda: self.add_row_for_codec())
        self.create_btn.clicked.connect(lambda: self.save_in_xml_file_suers())
        self.Nazad_btn.clicked.connect(lambda: self.exit_func())

    def add_row_for_codec(self):

        rowPosition = self.Codec_Table.rowCount()
        self.Codec_Table.insertRow(rowPosition)

        buttons_del = QtWidgets.QPushButton()
        combo = QtWidgets.QComboBox()

        buttons_del.setText('Delete')
        combo.addItem("PyQt")
        combo.addItem("exp")

        self.Codec_Table.setCellWidget(rowPosition, 2, buttons_del)
        self.Codec_Table.setCellWidget(rowPosition, 0, combo)

        buttons_del.clicked.connect(lambda: self.delete_row())

    def delete_row(self):
        Index = self.Codec_Table.currentIndex()
        self.Codec_Table.model().removeRow(Index.row())

    def save_in_xml_file_suers(self):

        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Gate = login.find('Gate')

        dict_from_codec_and_call = self.Codec_and_call_save_dict_func()

        if login.find('Gate').text == None:
            login.find(".//Gate").text = '0'

        ET.SubElement(Gate, "Gate_{}".format(login.find(".//Gate").text), GUI_name=self.Gateway_name.text(), Signaling = self.Signaling.text(), IP_Address = self.IP_Address.text(), IP_Port = self.IP_Port.text(), Num_codec= str(dict_from_codec_and_call['number_codec']),
                      Login_registr=self.Login_registr.text(), Password_registr=self.Password_registr.text(), TTL_registr = self.TTL_registr.text(), Reg_Ser_name = self.Reg_Ser_name.text(), Reg_address = self.Reg_address.text(),
                      Reg_Port=self.Reg_Port.text(), Reg_Login=self.Reg_Login.text(), Reg_password=self.Reg_password.text(), Reg_TTL=self.Reg_TTL.text(), Reg_Security_type=self.Reg_Security_type.text(), Reg_Endpoint_type=self.Reg_Endpoint_type.text(),
                      Gen_NAT=self.Gen_NAT.text(), Gen_Fax=self.Gen_Fax.text(), Gen_conv=self.Gen_conv.text(), Gen_repack=self.Gen_repack.text(), Gen_DTMF=self.Gen_DTMF.text(), Gen_Early_Connect=self.Gen_Early_Connect.text(), Registration = self.Registration.currentText(),
                      Gen_Proxy_RBT = self.Gen_Proxy_RBT.text(), SIP_Ringback_Tone = self.SIP_Ringback_Tone.text(), SIP_Allow_Sip_Red= self.SIP_Allow_Sip_Red.text(), SIP_Allow_noproxy= self.SIP_Allow_noproxy.text(), DS_error_han = self.DS_error_han.currentText()).text

        Codec_and_call_folder = Gate.find("Gate_{}".format(login.find(".//Gate").text))

        for i in range(int(dict_from_codec_and_call['number_codec'])):
            ET.SubElement(Codec_and_call_folder, "codec_{}".format(str(i)), codec_FFP = dict_from_codec_and_call['codec_FFP_{}'.format(str(i))], codec_codec = dict_from_codec_and_call['codec_codec_{}'.format(str(i))])

        login.find('.//Gate').text = str(int(login.find('.//Gate').text) + 1)

        tree = ET.ElementTree(root)
        tree.write("data\\filename2.xml")
        self.dumb_clean_func()
        self.close()

    def Codec_and_call_save_dict_func(self):
        dic_for_return = {}
        row_of_codec = self.Codec_Table.rowCount()
        for row in range(0, row_of_codec):
            codec0 = self.Codec_Table.cellWidget(row, 0)
            codec1 = self.Codec_Table.item(row, 1)
            if codec1 != None:
                dic_for_return['codec_FFP_{}'.format(str(row))] = str(codec1.text())
            else:
                dic_for_return['codec_FFP_{}'.format(str(row))] = ''
            dic_for_return['codec_codec_{}'.format(str(row))] = str(codec0.currentText())

        dic_for_return['number_codec'] = row_of_codec

        return dic_for_return

    def exit_func(self):
        self.close()

    def dumb_clean_func(self):
        self.Gateway_name.setText('')
        self.Signaling.setText('')
        self.IP_Address.setText('')
        self.IP_Port.setText('')
        self.Login_registr.setText('')
        self.Password_registr.setText('')
        self.TTL_registr.setText('')
        self.Reg_Ser_name.setText('')
        self.Reg_address.setText('')
        self.Reg_Port.setText('')
        self.Reg_Login.setText('')
        self.Reg_password.setText('')
        self.Reg_TTL.setText('')
        self.Reg_Security_type.setText('')
        self.Reg_Endpoint_type.setText('')
        self.Gen_NAT.setText('')
        self.Gen_Fax.setText('')
        self.Gen_conv.setText('')
        self.Gen_repack.setText('')
        self.Gen_DTMF.setText('')
        self.Gen_Early_Connect.setText('')
        self.Gen_Proxy_RBT.setText('')
        self.SIP_Ringback_Tone.setText('')
        self.SIP_Allow_Sip_Red.setText('')
        self.SIP_Allow_noproxy.setText('')
        while self.Codec_Table.rowCount() > 0:
            self.Codec_Table.removeRow(0)

    def Edit_Gate_form_func(self, row):
        root = ET.parse('Data\\filename2.xml').getroot()
        login = root.find(root.find('Login_folder').text)
        Users = login.find('Gate')
        curreant_User = Users.find('Gate_{}'.format(str(row)))

        for type_tag in Users.findall("Gate_{}".format(str(row))):
            self.Gateway_name.setText(type_tag.get('GUI_name'))
            self.Signaling.setText(type_tag.get('Signaling'))
            self.IP_Address.setText(type_tag.get('IP_Address'))
            self.IP_Port.setText(type_tag.get('IP_Port'))
            self.Login_registr.setText(type_tag.get('Login_registr'))
            self.Password_registr.setText(type_tag.get('Password_registr'))
            self.TTL_registr.setText(type_tag.get('TTL_registr'))
            self.Reg_Ser_name.setText(type_tag.get('Reg_Ser_name'))
            self.Reg_address.setText(type_tag.get('Reg_address'))
            self.Reg_Port.setText(type_tag.get('Reg_Port'))
            self.Reg_Login.setText(type_tag.get('Reg_Login'))
            self.Reg_password.setText(type_tag.get('Reg_password'))
            self.Reg_TTL.setText(type_tag.get('Reg_TTL'))
            self.Reg_Security_type.setText(type_tag.get('Reg_Security_type'))
            self.Reg_Endpoint_type.setText(type_tag.get('Reg_Endpoint_type'))
            self.Gen_NAT.setText(type_tag.get('Gen_NAT'))
            self.Gen_Fax.setText(type_tag.get('Gen_Fax'))
            self.Gen_conv.setText(type_tag.get('Gen_conv'))
            self.Gen_repack.setText(type_tag.get('Gen_repack'))
            self.Gen_DTMF.setText(type_tag.get('Gen_DTMF'))
            self.Gen_Early_Connect.setText(type_tag.get('Gen_Early_Connect'))
            self.Gen_Proxy_RBT.setText(type_tag.get('Gen_Proxy_RBT'))
            self.SIP_Ringback_Tone.setText(type_tag.get('SIP_Ringback_Tone'))
            self.SIP_Allow_Sip_Red.setText(type_tag.get('SIP_Allow_Sip_Red'))
            self.SIP_Allow_noproxy.setText(type_tag.get('SIP_Allow_noproxy'))

            for i in range(int(type_tag.get('Num_codec'))):
                self.add_row_for_codec()
                for type_tag_2 in curreant_User.findall("codec_{}".format(str(i))):
                    codec = self.Codec_Table.cellWidget(i, 0)
                    index = codec.findText(type_tag_2.get('codec_codec'))
                    if index >= 0:
                        codec.setCurrentIndex(index)
                    self.Codec_Table.setItem(i, 1, QTableWidgetItem(str(type_tag_2.get('codec_FFP'))))