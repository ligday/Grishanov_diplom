import sys
from PyQt5 import QtWidgets
import Logic, Reg_log_class

def main():
    app = QtWidgets.QApplication(sys.argv)
    login = Reg_log_class.Login()
    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Logic.Save_class()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()



#Login, window = Logic.Save_class()