import sys
from PyQt5 import QtWidgets, QtCore
import Portal_UI
import SystemAdmin_UI
from PyQt5.QtWidgets import *
from CampAdmin import CampAdmin
import SysAdmin


class SysAdminWindow(QMainWindow, SystemAdmin_UI.Ui_MainWindow):
    def __init__(self):
        super(SysAdminWindow, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.setup_for_create_database)
        self.pushButton_3.clicked.connect(self.drop_database)
        self.pushButton_2.clicked.connect(self.read_a_database)
        self.pushButton_4.clicked.connect(self.list_camps_n_details)
        self.pushButton_5.clicked.connect(self.exit_now)
        # this is the button below the field asking campName
        self.pushButton_6.setText("Disabled")
        self.pushButton_6.setEnabled(False)
        self.pushButton_6.setAutoDefault(True)

        # later functions enable this, then this line is required
        self.pushButton_6.clicked.connect(self.call_appropriate)
        # if this window is visible that means authentication was done successfully
        self.admin = None
        self.camp_name = None
        self.__pswd = "IamSysAdmin99"

        self.response = None        # used in create_database to find if camp registered successfully
        self.createDbase_step1 = SysAdmin.GetDetails()      # getDetails Window of camp while registering
        self.createDbase_step2 = SysAdmin.GetMemDetails()   # getMember details window of camp while registering
        self.members_data = []
        self.camp_data = []
        self.times = None
        # very important to keep such signals out of fns that repeat, otherwise the signals get multiplied
        self.createDbase_step2.pushButton.clicked.connect(self.check_times)

    def call_appropriate(self):
        txt = self.pushButton_6.text()
        if txt == "Proceed":
            self.get_details()
        elif txt == "UnRegister":
            self.drop_database()

        self.pushButton_6.setEnabled(False)
        self.pushButton_6.setText("Disabled")

    def setup_for_create_database(self):
        print("Create database signal received")
        self.admin = SysAdmin.SysAdmin(self.__pswd)
        print("before focus")

        self.lineEdit.setFocus()
        self.lineEdit.clear()
        self.pushButton_6.setText("Proceed")
        self.pushButton_6.setEnabled(True)

    def get_details(self):
        self.createDbase_step1.show()
        self.setEnabled(False)
        self.createDbase_step1.pushButton.clicked.connect(self.get_member_details)

    def get_member_details(self):
        print(self.createDbase_step1.lineEdit.text())
        self.createDbase_step1.setEnabled(False)
        self.times = int(self.createDbase_step1.spinBox_2.text())
        print(self.times)
        self.createDbase_step2.show()

    def check_times(self):
        tmpLst = list()
        tmpLst.append(self.createDbase_step2.lineEdit.text())
        tmpLst.append(self.createDbase_step2.lineEdit_2.text())
        tmpLst.append(self.createDbase_step2.lineEdit_3.text())
        tmpLst.append(self.createDbase_step2.lineEdit_4.text())
        tmpLst = tuple(tmpLst)
        self.members_data.append(tmpLst)
        self.times -= 1
        self.createDbase_step1.spinBox_2.setValue(self.times)
        self.createDbase_step2.pushButton_2.click()
        self.createDbase_step2.close()

        if self.times > 0:
            self.get_member_details()
        else:
            self.create_database()

    def create_database(self):
        self.camp_data.append(self.createDbase_step1.lineEdit.text())
        self.camp_data.append(self.createDbase_step1.lineEdit_2.text())
        self.camp_data.append(self.createDbase_step1.lineEdit_3.text())
        self.camp_data.append(self.createDbase_step1.lineEdit_4.text())
        self.camp_data.append(self.createDbase_step1.lineEdit_5.text())
        self.camp_data.append(self.createDbase_step1.lineEdit_6.text())
        self.camp_data.append(self.createDbase_step1.lineEdit_7.text())
        self.camp_data.append(self.createDbase_step1.lineEdit_8.text())
        self.camp_data.append(len(self.members_data))
        self.camp_data.append(self.createDbase_step1.spinBox.text())

        print(self.camp_data)
        print(self.members_data)
        self.createDbase_step1.close()
        self.createDbase_step2.close()

        self.camp_name = "camp" + self.lineEdit.text()
        self.response = self.admin.registerCamp(self.camp_name, self.camp_data, self.members_data)
        if self.response == 0:
            self.label_6.setText(self.camp_name + " successfully registered.")
            QMessageBox.information(self, "Information", self.camp_name + " registered successfully.")
        else:
            self.label_6.setText(self.camp_name + " registration failed as the camp already exists")
            QMessageBox.critical(self, "Error", self.camp_name + " registration failed as the camp already exists!!")

        # enable the main window of System Administrator
        self.setEnabled(True)
        # both forms are editable (as we disabled them in way, so enable again[because below we reset them])
        self.createDbase_step1.setEnabled(True)
        self.createDbase_step2.setEnabled(True)
        # clear the contents in both the forms [reset]
        self.createDbase_step1.pushButton_2.click()
        self.createDbase_step2.pushButton_2.click()
        # reset the data (not required anymore)
        self.camp_data = []
        self.members_data = []

    def drop_database(self):
        print("Drop database signal received")

    def read_a_database(self):
        print("Read a database signal received")

    def list_camps_n_details(self):
        print("List all camps and their details signal received")

    def exit_now(self):
        print("Exit signal received")
        self.close()
        exit(0)


class Portal(QMainWindow, Portal_UI.Ui_mainWindow):

    def __init__(self):
        super(Portal, self).__init__()
        self.setupUi(self)

        # connect button is disabled [will enable when a valid role/portal is selected]
        self.pushButton.setEnabled(False)

        # makes Connect and Reset button trigger-able by Enter key also
        self.pushButton.setAutoDefault(True)
        self.pushButton_2.setAutoDefault(True)

        # disable both entry entry boxes (campId, password) [will enable when a valid role/portal is selected]
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.reset_clicked)
        self.comboBox.currentIndexChanged.connect(self.combo_box_index_changed)

        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def combo_box_index_changed(self, index):
        # for campAdmin (camp name box)
        if index == 2:
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.setEnabled(False)

        # for password and connect button (until an option is selected, password field and connect button are disabled)
        if index == 0:
            self.lineEdit_2.setEnabled(False)
            self.pushButton.setEnabled(False)
        else:
            self.lineEdit_2.setEnabled(True)
            self.pushButton.setEnabled(True)

    def reset_clicked(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.comboBox.setCurrentIndex(0)
        print("Reset")


class ControllerWindow(QMainWindow):
    def __init__(self):
        super(ControllerWindow, self).__init__()
        self.setWindowTitle("RAHAT V1.0")

        self.which_portal = None
        self.__pswd = None
        self.camp_id = None
        self.win = None
        self.admin = None

        # call portal selector
        self.portal_selector = Portal()
        self.portal_selector.show()
        # connect button signal connected to connect_clicked() slot
        self.portal_selector.pushButton.clicked.connect(self.connect_clicked)

    def connect_clicked(self):
        print("Connect")
        # get data items
        self.which_portal = self.portal_selector.comboBox.currentIndex()
        self.__pswd = self.portal_selector.lineEdit_2.text()
        self.camp_id = self.portal_selector.lineEdit.text()
        # print(self.which_portal, self.__pswd, self.camp_id)
        self.portal_selector.close()

        # proceed according to portal choice
        if self.which_portal == 1:
            self.system_admin_window()
        else:
            self.camp_admin_window()

    def system_admin_window(self):
        print("Success signal from system_admin_window")
        try:
            self.admin = SysAdmin.SysAdmin(self.__pswd)
        except:
            QMessageBox.critical(self, "Error", "Wrong Password")
            exit(-1)
        # if password is correct then System Admin window will pop up else exit()
        # create and show sysAdminWindow
        self.win = SysAdminWindow()
        self.win.showMaximized()

    def camp_admin_window(self):
        print("Success signal from camp_admin_window")
        self.camp_name = "camp" + self.camp_id
        try:
            self.admin = CampAdmin(self.camp_name, self.__pswd)
        except:
            QMessageBox.critical(self, "Error", "Wrong Password")
            exit(-1)
        # if password is correct then Camp Admin window will pop up else exit()


app = QApplication(sys.argv)
window = ControllerWindow()  # this is the controller window (but never shown)
app.exec()
