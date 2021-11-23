import sys
from PyQt5 import QtWidgets, QtGui
import Portal_UI
import SystemAdmin_UI
import CampAdmin_UI
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import CampAdmin
import SysAdmin


class CampAdminWindow(QMainWindow, CampAdmin_UI.Ui_camp_admin):
    def __init__(self, camp_name):
        super(CampAdminWindow, self).__init__()
        self.setupUi(self)

        # disable all input boxes (default)
        self.lineEdit_family_id.setEnabled(False)
        self.lineEdit_member_no.setEnabled(False)
        self.lineEdit_member_name.setEnabled(False)
        self.lineEdit_district_name.setEnabled(False)
        # disable both buttons (update, find)
        self.pushButton_fId_mNo_mName.setText("Disabled")
        self.pushButton_fId_mNo_mName.setEnabled(False)
        self.pushButton_district_itmTyp.setText("Disabled")
        self.pushButton_district_itmTyp.setEnabled(False)

        # disable labels of above buttons
        self.label_family_id.setEnabled(False)
        self.label_member_no.setEnabled(False)
        self.label_member_name.setEnabled(False)
        self.label_district_name.setEnabled(False)
        # disable these too
        self.label_item_type.setEnabled(False)
        self.comboBox_item_type.setEnabled(False)

        # for reading details of persons in camp
        self.pushButton_read_records.clicked.connect(self.read_my_tables)
        self.actionRead_Records.triggered.connect(self.read_my_tables)

        # for adding new person in camp
        self.pushButton_enter_new_record.clicked.connect(self.new_person_form)
        self.actionEnter_New_Record.triggered.connect(self.new_person_form)
        self.new_person_data = list()     # will become a list later on
        self.count = None
        self.new_person_win = CampAdmin.NewPerson()
        # for first member
        self.new_person_win.lineEdit_4.setText("self")
        self.new_person_win.lineEdit_4.setEnabled(False)

        # for updating details of person in camp
        # main button
        self.pushButton_update_details.clicked.connect(self.enable_update_fields)
        self.actionUpdate_details_of_a_person.triggered.connect(self.enable_update_fields)
        # below button
        self.pushButton_fId_mNo_mName.clicked.connect(self.person_details_update_form)
        self.details_update_win = CampAdmin.UpdatePerson()
        self.details_update_win.pushButton.clicked.connect(self.update_the_details)

        # find resource availability
        self.pushButton_find_resource.clicked.connect(self.ask_district)
        self.actionFind_Resource.triggered.connect(self.ask_district)
        self.resource_type_win = CampAdmin.ResourceType()
        # self.medical_res_win = CampAdmin.MedicalResource()
        # self.regular_res_win = CampAdmin.RegularResource()
        self.pushButton_district_itmTyp.clicked.connect(self.resource_type_select)
        self.resource_type_win.pushButton_2.clicked.connect(self.launch_appropriate_res_table)

        # request supply data
        self.pushButton_request_supply.clicked.connect(self.launch_supply_dialog)
        self.actionRequest_Supply_Data.triggered.connect(self.launch_supply_dialog)
        self.supply_rqst_dlg = CampAdmin.RequestSupply()
        self.supply_rqst_dlg.pushButton_submit.clicked.connect(self.make_supply_request)

        # update supply data
        self.pushButton_update_supply.clicked.connect(self.launch_update_supply_dialog)
        self.actionUpdate_Supply_Data.triggered.connect(self.launch_update_supply_dialog)
        self.update_supply_dlg = CampAdmin.UpdateSupply()
        self.update_supply_dlg.pushButton_submit.clicked.connect(self.make_supply_update)

        # find vacancies
        self.pushButton_find_vacancies.clicked.connect(self.get_district)
        self.actionFind_Vacancies_in_other_camps.triggered.connect(self.get_district)

        # new person in camp (window for getting new person's details)
        self.new_person_win.checkBox.clicked.connect(self.configure_injury_subform)
        self.new_person_win.checkBox_2.clicked.connect(self.configure_injury_subform)
        self.new_person_win.comboBox_2.currentIndexChanged.connect(self.toggle_recovery_percent)
        # when submit is pressed
        self.new_person_win.pushButton.clicked.connect(self.check_times)

        # view today all
        self.pushButton_today_view_all.clicked.connect(self.launch_today_view_all_window)
        self.actionView_Today.triggered.connect(self.launch_today_view_all_window)

        # exit
        self.pushButton_exit.clicked.connect(self.exit_now)

        # about
        self.actionAbout.triggered.connect(self.about)

        # initialize the object
        self.camp_name = camp_name
        # print(self.camp_name)
        self.__pswd = "IamCampAdmin88"
        self.admin = CampAdmin.CampAdmin(self.camp_name, self.__pswd)

    def new_person_form(self):
        self.new_person_win.show()

    def about(self):
        message = "Project RAHAT v1.0\t\t\n\nCreated By   - Suraj Singh\t\t\n" \
                  "Designation - B.Tech CSE student (2nd Year)" \
                  "\t\t\n\nContributor  - Vagish Baweja\t\t\nDesignation - B.Tech CSE student (2nd Year)\n"
        self.aboutMessage = QMessageBox.information(self, "About", message)

    # ------------------- To find vacancies in other camps -----------------------
    def get_district(self):
        self.ask_district()
        self.pushButton_district_itmTyp.setText('find..')

    def find_vacancies(self):
        print("in find vacancies")
        district = self.lineEdit_district_name.text().lower()
        self.data = self.admin.findVacancies(district)

        if type(self.data) is not list and 'error' in self.data.lower():
            QMessageBox.critical(self, "Error", self.data)
        elif len(self.data) == 0:
            QMessageBox.information(self, "Information", "Nothing found in this district!!\t")
        else:
            self.vacancies_win = CampAdmin.VacanciesInCamp()
            # if data is there in table then
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.vacancies_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.vacancies_win.show()

    # ------------------ update/add supply items in camp records --------
    def launch_update_supply_dialog(self):
        print("launching update supply dlg")
        self.update_supply_dlg.show()

    def make_supply_update(self):
        print("Marking supply updates")
        self.update_supply_dlg.close()
        itm_name = self.update_supply_dlg.lineEdit_item_name.text()
        category = self.update_supply_dlg.comboBox_category.currentText().lower()
        age_grp = self.update_supply_dlg.comboBox_age_group.currentText().lower()
        itm_type = self.update_supply_dlg.lineEdit_item_type.text().lower()
        itm_desc = self.update_supply_dlg.lineEdit_item_description.text().lower()
        itm_qty = self.update_supply_dlg.spinBox_quantity.text()

        data = (itm_name, category, age_grp, itm_type, itm_desc, itm_qty)
        self.response = self.admin.updateSupplyData(self.camp_name, data)
        print(self.response)
        self.update_supply_dlg.pushButton_reset.click()
        if "error" not in self.response.lower():
            QMessageBox.information(self, "Information", self.response)
        else:
            QMessageBox.critical(self, "Error", self.response)

    # ------------------ For item supply request --------------------------
    def launch_supply_dialog(self):
        print("launch supply dialog")
        self.supply_rqst_dlg.show()

    def make_supply_request(self):
        print("Making supply request!!")
        self.supply_rqst_dlg.close()
        itm_name = self.supply_rqst_dlg.lineEdit_item_name.text()
        itm_type = self.supply_rqst_dlg.comboBox_item_type.currentText()
        itm_desc = self.supply_rqst_dlg.lineEdit_item_desc.text()
        qty = self.supply_rqst_dlg.spinbox_quantity.text()
        data = (itm_name, itm_type, itm_desc, qty)
        self.response = self.admin.requestSupplyFromMain(self.camp_name, data)
        if "error" not in self.response.lower():
            QMessageBox.information(self, "Success", self.response)
        else:
            QMessageBox.critical(self, "Error", self.response)
        # clear the form
        self.supply_rqst_dlg.pushButton_reset.click()

    # --------------- For finding resource availability -----------------

    def ask_district(self):
        print("in")
        self.label_district_name.setEnabled(True)
        self.lineEdit_district_name.setEnabled(True)
        self.lineEdit_district_name.clear()
        self.lineEdit_district_name.setFocus()
        self.pushButton_district_itmTyp.setEnabled(True)
        self.pushButton_district_itmTyp.setText("Find...")
        self.pushButton_district_itmTyp.setAutoDefault(True)
        print("out")

    def resource_type_select(self):
        button_is = self.pushButton_district_itmTyp.text()
        self.label_district_name.setEnabled(False)
        self.lineEdit_district_name.setEnabled(False)
        self.pushButton_district_itmTyp.setText("Disabled")
        self.pushButton_district_itmTyp.setEnabled(False)
        print(button_is)
        if button_is == "Find...":
            self.resource_type_win.lineEdit.setFocus()
            self.resource_type_win.lineEdit.clear()
            self.resource_type_win.pushButton.setAutoDefault(True)
            self.resource_type_win.pushButton_2.setAutoDefault(True)
            self.resource_type_win.show()
        else:
            print("in final or res_type_sel")
            self.find_vacancies()

    def launch_appropriate_res_table(self):
        # close type select form
        self.resource_type_win.close()
        # both type table create (will see which reqd)
        self.regular_res_win = CampAdmin.RegularResource()
        self.medical_res_win = CampAdmin.MedicalResource()

        district = self.lineEdit_district_name.text()
        item_name = self.resource_type_win.lineEdit.text().lower()
        item_type = self.resource_type_win.comboBox.currentText().lower()
        # print(item_type)
        if item_type not in ("medical", "regular"):
            print("Please select a type")
            QMessageBox.critical(self, "Error", "Please select a type!!")
            return
        # resetting the type select form
        self.resource_type_win.pushButton.click()
        self.resource_type_win.comboBox.setCurrentIndex(0)
        # print("Before calling readItemAvail()")

        # get the data
        self.data = self.admin.readItemAvailability(district, item_name, item_type)
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    if item_type == "regular":
                        self.regular_res_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
                    elif item_type == "medical":
                        self.medical_res_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            if item_type == "regular":
                self.regular_res_win.show()
            else:
                self.medical_res_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "Nothing found in this district!!\t")

    # ---------------- for updating details of a person -------------------------------------

    def enable_update_fields(self):
        self.lineEdit_family_id.setEnabled(True)
        self.lineEdit_family_id.clear()
        self.lineEdit_family_id.setFocus()
        self.lineEdit_member_no.setEnabled(True)
        self.lineEdit_member_no.clear()
        # self.lineEdit_member_name.setEnabled(True)
        self.label_family_id.setEnabled(True)
        self.label_member_no.setEnabled(True)
        self.pushButton_fId_mNo_mName.setEnabled(True)
        self.pushButton_fId_mNo_mName.autoDefault()
        self.pushButton_fId_mNo_mName.setText("Update...")

    def person_details_update_form(self):
        family_id = self.lineEdit_family_id.text()
        member_no = self.lineEdit_member_no.text()
        if family_id == '' or member_no == '':
            QMessageBox.critical(self, "Error", "Family ID or Member No can't be empty!!")
        else:
            self.details_update_win.comboBox.setCurrentIndex(0)
            self.details_update_win.pushButton_2.click()
            self.details_update_win.show()

    def update_the_details(self):
        self.details_update_win.close()
        self.lineEdit_family_id.setEnabled(False)
        self.lineEdit_member_no.setEnabled(False)
        self.label_family_id.setEnabled(False)
        self.label_member_no.setEnabled(False)
        family_id = self.lineEdit_family_id.text()
        member_no = self.lineEdit_member_no.text()
        injury = self.details_update_win.comboBox.currentText()
        if 'Select' not in injury:
            injury = injury[0]
            injury_status = self.details_update_win.spinBox.text()
        else:
            injury = '-'
            injury_status = '-'

        leaving_today = self.details_update_win.checkBox.isChecked()
        if leaving_today:
            leaving_today = 'Y'
        else:
            leaving_today = 'N'

        print("Before setting data")
        self.data = [family_id, member_no, injury, injury_status, leaving_today]
        self.data = tuple(self.data)
        print("printing the data")
        print(self.data)
        self.response = self.admin.updateDetails(self.camp_name, self.data)
        if self.response.startswith('Error!'):
            QMessageBox.critical(self, "Error", self.response)
        else:
            QMessageBox.information(self, "Information", self.response)

    # ---------------- writing into camp (details of a new person) --------------------------
    def toggle_recovery_percent(self):
        # if recovery started is yes, then enable, if no the disable (toggles as options change)
        if self.new_person_win.comboBox_2.currentText() == "Yes":
            self.new_person_win.spinBox_2.setEnabled(True)
        else:
            self.new_person_win.spinBox_2.setEnabled(False)

    def configure_injury_subform(self):
        print("in configure injury form")
        # when person is in camp and has injury only then injury subform is enabled to be filled
        if self.new_person_win.checkBox.isChecked() and self.new_person_win.checkBox_2.isChecked():
            # enable injury subform (input fields)
            self.new_person_win.lineEdit_7.setEnabled(True)
            self.new_person_win.comboBox.setEnabled(True)
            self.new_person_win.comboBox_2.setEnabled(True)
            # enable injury subform (labels)
            self.new_person_win.label_9.setEnabled(True)
            self.new_person_win.label_10.setEnabled(True)
            self.new_person_win.label_11.setEnabled(True)
            self.new_person_win.label_12.setEnabled(True)
            self.new_person_win.label_14.setEnabled(True)
        else:
            print("In false block")
            # disable injury subform (input fields)
            self.new_person_win.lineEdit_7.setEnabled(False)
            self.new_person_win.comboBox.setEnabled(False)
            self.new_person_win.comboBox_2.setEnabled(False)
            # self.new_person_win.spinBox_2.setEnabled(False)
            # disable injury subform (labels)
            self.new_person_win.label_9.setEnabled(False)
            self.new_person_win.label_10.setEnabled(False)
            self.new_person_win.label_11.setEnabled(False)
            self.new_person_win.label_12.setEnabled(False)
            self.new_person_win.label_14.setEnabled(False)

    def check_times(self):
        # extract form data and store in self.new_person_data
        self.extract_data()

        # then check the counter, decrement no of persons
        self.count = int(self.new_person_win.spinBox_3.text()) - 1
        print(self.count)

        self.set_appropriate_default_1()

        if self.count > 0:
            self.new_person_form()
        else:
            self.new_person_win.close()
            print("Time to send all data for final action")
            self.response = self.admin.writeInto(self.camp_name, tuple(self.new_person_data))
            # print(self.response)
            QMessageBox.information(self, "Information", self.response)
            # this will clear the data also and also the admin
            self.set_appropriate_default_2()

    # -------------------- helpers of check_times --------------------
    def extract_data(self):
        tmpLst = list()
        tmpLst.append(self.new_person_win.lineEdit.text())
        tmpLst.append(self.new_person_win.spinBox.text())
        gender = ''
        if self.new_person_win.radioButton.isChecked():
            gender = 'M'
        else:
            gender = 'F'
        tmpLst.append(gender)
        tmpLst.append(self.new_person_win.lineEdit_4.text())
        tmpLst.append(self.new_person_win.lineEdit_5.text())
        tmpLst.append(self.new_person_win.lineEdit_6.text())
        tmpLst.append(self.new_person_win.spinBox_3.text())
        if self.new_person_win.checkBox.isChecked():
            tmpLst.append('Y')
        else:
            tmpLst.append('N')
        if self.new_person_win.checkBox_2.isChecked():
            tmpLst.append('Y')
        else:
            tmpLst.append('N')
        tmpLst = tuple(tmpLst)
        print(tmpLst)

        tmpLst2 = list()
        tmpLst2.append(self.new_person_win.lineEdit_7.text())
        tmpLst2.append(self.new_person_win.comboBox.currentText())
        tmpLst2.append(self.new_person_win.comboBox_2.currentText())
        tmpLst2.append(self.new_person_win.spinBox_2.text())
        tmpLst2 = tuple(tmpLst2)

        print("yes till here")
        one_packet = (tmpLst, tmpLst2)  # two tuples in single tuple (data of one person)
        self.new_person_data.append(one_packet)
        print(one_packet)

    def set_appropriate_default_1(self):
        self.new_person_win.spinBox_3.setEnabled(True)
        self.new_person_win.spinBox_3.setValue(self.count)
        self.new_person_win.spinBox_3.setEnabled(False)
        # but first update - total_family_members (spinbox3) then  lock
        print("count set")

        self.new_person_win.lineEdit_5.setEnabled(False)
        self.new_person_win.lineEdit_6.setEnabled(False)
        # lock : village/city loc in vill/city (lineEdit5, lineEdit6)

        self.new_person_win.lineEdit_4.setEnabled(True)
        # unlock lineEdit_4 (relation)
        print("Going to press Reset button")

        self.new_person_win.pushButton_2.click()
        # send reset signal to all : click the pushbutton2
        self.new_person_win.close()
        # close the window

        # checkboxes unchecked
        self.new_person_win.checkBox.setCheckState(False)
        self.new_person_win.checkBox_2.setCheckState(False)
        # injury record combo boxes set to default
        self.new_person_win.comboBox.setCurrentIndex(0)
        self.new_person_win.comboBox.setEnabled(False)
        self.new_person_win.comboBox_2.setCurrentIndex(0)
        self.new_person_win.comboBox_2.setEnabled(False)
        self.new_person_win.lineEdit_7.setEnabled(False)

        self.new_person_win.radioButton.setChecked(False)
        self.new_person_win.radioButton_2.setChecked(False)

    def set_appropriate_default_2(self):
        # once one family's full record is taken, clear the data from var
        self.new_person_data = list()
        # creating new object again (so family id etc will get updated)
        self.admin = CampAdmin.CampAdmin(self.camp_name,self.__pswd)
        self.new_person_win.lineEdit_4.setText("self")
        self.new_person_win.lineEdit_4.setEnabled(False)

        self.new_person_win.lineEdit_5.setEnabled(True)
        self.new_person_win.lineEdit_5.clear()

        self.new_person_win.lineEdit_6.setEnabled(True)
        self.new_person_win.lineEdit_6.clear()

        self.new_person_win.spinBox_3.setEnabled(True)

        self.new_person_win.lineEdit.setFocus()
    # -------------------- -------------------- -------------------- --------------------

    # ---------------- ---------------- ---------------- ---------------- ---------------- ----------------
    def exit_now(self):
        exit(0)
    # ------------------------ for reading tables ------------------------
    def read_my_tables(self):
        self.select_table = CampAdmin.SelectATable()
        self.select_table.pushButton.clicked.connect(self.launch_main_table_window)
        self.select_table.pushButton_2.clicked.connect(self.launch_injury_table_window)
        self.select_table.pushButton_3.clicked.connect(self.launch_regular_supply_table_window)
        self.select_table.pushButton_4.clicked.connect(self.launch_medical_supply_table_window)
        self.select_table.pushButton_5.clicked.connect(self.launch_my_camp_info_window)
        self.select_table.pushButton_6.clicked.connect(self.launch_today_view_all_window)
        self.select_table.show()

    def launch_main_table_window(self):
        self.main_table_win = CampAdmin.MainTable()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "main_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    # self.tmp_label.setMargin(0)
                    # self.tmp_label.setFont(QFont(("MS Shell Dlg 2", 8)))
                    # self.tmp_label.setStyleSheet("QLabel {background-color: red;}")
                    # self.tmp_label.setLineWidth("1")
                    self.main_table_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.main_table_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_injury_table_window(self):
        self.injury_table_win = SysAdmin.InjuryTable()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "injury_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.injury_table_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.injury_table_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_regular_supply_table_window(self):
        self.regular_supply_win = SysAdmin.RegularSupply()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "regular_supply_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.regular_supply_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.regular_supply_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_medical_supply_table_window(self):
        self.medical_supply_win = SysAdmin.MedicalSupply()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "medical_supply_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.medical_supply_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.medical_supply_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_my_camp_info_window(self):
        self.my_camp_win = SysAdmin.MyCamp()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "my_camp_info")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.my_camp_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.my_camp_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_today_view_all_window(self):
        self.today_view_win = SysAdmin.TodayAll()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "today_all")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.today_view_win.gridLayout_2.addWidget(self.tmp_label, i + 1, j)
            # show
            self.today_view_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    # -------------------------------------------------------------------------------------------------------

    def setup_for_update_table_details(self):
            self.label_family_id.setEnabled(True)
            self.label_member_no.setEnabled(True)
            self.label_member_name.setEnabled(True)

            self.lineEdit_family_id.setEnabled(True)
            self.lineEdit_family_id.clear()
            self.lineEdit_member_no.setEnabled(True)
            self.lineEdit_member_no.clear()
            self.lineEdit_member_name.setEnabled(True)
            self.lineEdit_member_name.clear()

            self.pushButton_fId_mNo_mName.setEnabled(True)
            self.pushButton_fId_mNo_mName.setText("Update")


class SysAdminWindow(QMainWindow, SystemAdmin_UI.Ui_MainWindow):
    def __init__(self):
        super(SysAdminWindow, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.setup_for_create_database)
        self.actionRegister_camp.triggered.connect(self.setup_for_create_database)
        self.pushButton_2.clicked.connect(self.setup_for_drop_database)
        self.actionUn_Register_camp.triggered.connect(self.setup_for_drop_database)
        self.pushButton_3.clicked.connect(self.list_all_registered_camps)
        self.actionList_all_camp_details_2.triggered.connect(self.list_all_registered_camps)
        self.pushButton_4.clicked.connect(self.setup_for_read_database)
        self.actionRead_a_camp_2.triggered.connect(self.setup_for_read_database)

        self.pushButton_5.clicked.connect(self.select_one_of_all_tbl)
        self.actionList_all_camp_details_3.triggered.connect(self.select_one_of_all_tbl)
        print(1)
        self.one_selector = SysAdmin.SelectOneOfAllDetails()
        print(2)
        self.one_selector.pushButton_basic_details.clicked.connect(self.list_all_basic_details)
        self.one_selector.pushButton_demand_n_feedback.clicked.connect(self.list_all_demand_feedback)

        self.pushButton_6.clicked.connect(self.exit_now)
        self.actionExit.triggered.connect(self.exit_now)
        self.actionLogout.triggered.connect(self.exit_now)
        self.actionAbout.triggered.connect(self.about)

        # this is the button below the field asking campName
        self.pushButton_7.setText("Disabled")
        self.pushButton_7.setEnabled(False)
        self.pushButton_7.setAutoDefault(True)
        # later functions enable this, then this line is required
        self.pushButton_7.clicked.connect(self.call_appropriate)

        # if this window is visible that means authentication was done successfully
        self.camp_name = None
        self.__pswd = "IamSysAdmin99"
        self.admin = SysAdmin.SysAdmin(self.__pswd)

        self.response = None        # used in create_database to find if camp registered successfully
        self.createDbase_step1 = SysAdmin.GetDetails()      # getDetails Window of camp while registering
        self.createDbase_step2 = SysAdmin.GetMemDetails()   # getMember details window of camp while registering
        self.members_data = []
        self.camp_data = []
        self.times = None
        # very important to keep such signals out of fns that repeat, otherwise the signals get multiplied
        # this calls member data forms n times (n = no of support members entered)
        self.createDbase_step2.pushButton.clicked.connect(self.check_times)

        # used in read a table
        self.select_table = None
        self.data = None

    def call_appropriate(self):
        txt = self.pushButton_7.text()

        if txt == "Proceed":
            tmp_camp = "camp" + self.lineEdit.text()
            # if camp is present, then creation abort
            if self.admin.isPresentCamp(tmp_camp):
                self.label_6.setText(tmp_camp + " registration failed as the camp already exists")
                QMessageBox.critical(self, "Error",
                                     tmp_camp + " registration failed as the camp already exists!!\t\t")
            elif tmp_camp == '':
                QMessageBox.critical(self, "Error", "Camp name can't be empty!!\t\t")
            else:
                self.get_details()

        elif txt == "DeRegister":
            tmp_camp = "camp" + self.lineEdit.text()
            if tmp_camp != '':
                self.drop_database()
            else:
                QMessageBox.critical(self, "Error", "Camp name can't be empty!!\t\t")
        elif txt == "Read":
            self.read_a_database()

        self.pushButton_7.setEnabled(False)
        self.pushButton_7.setText("Disabled")

    # ----------------------- About -----------------------
    def about(self):
        message = "Project RAHAT v1.0\t\t\n\nCreated By   - Suraj Singh\t\t\n" \
                  "Designation - B.Tech CSE student (2nd Year)" \
                  "\t\t\n\nContributor  - Vagish Baweja\t\t\nDesignation - B.Tech CSE student (2nd Year)\n"
        self.aboutMessage = QMessageBox.information(self, "About", message)

    # ----------------------- For listing all database names (registered camp names) -----------------------
    def list_all_registered_camps(self):
        self.pushButton_7.setText("Disabled")
        self.pushButton_7.setEnabled(False)
        all_databases_list = self.admin.listAllDatabases()[3:]
        # leaving top 3 camps (are of postgres server)

        all_databases = "All Camp (Names) currently registered are:\n\n"
        for db in all_databases_list:
            all_databases += db + '\n'
        self.label_4.setText('')
        self.label_4.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.label_4.setText(all_databases)
        # auto expand (to be used every time new text is set)
        self.label_4.adjustSize()

    # ----------------------- For displaying information of a 'specific camp' -----------------------
    def setup_for_read_database(self):
        print("Read a database signal received")
        print("before focus")
        # display all databases in side label
        self.list_all_registered_camps()

        # connect to camp id line
        self.lineEdit.setFocus()
        self.lineEdit.clear()
        self.pushButton_7.setText("Read")
        self.pushButton_7.setEnabled(True)

    def read_a_database(self):
        print("Read a database signal received")
        # extract camp id and make camp_name
        self.camp_name = "camp" + self.lineEdit.text()

        # restructure
        self.data = self.admin.readCamp(self.camp_name)
        # print(self.data)
        # print("here")
        if self.data[0] == '-1':
            QMessageBox.critical(self, "Invalid", self.camp_name + " is not a registered camp!!\t")
        else:
            self.label_4.setText('')
            self.label_4.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
            self.label_4.setText(self.data[0])
            self.label_4.adjustSize()
            self.select_table = SysAdmin.SelectATable()
            if 'main_table2021' not in self.data[1]:
                # disable main_table button
                self.select_table.pushButton.setEnabled(False)
            elif 'injury_table2021' not in self.data[1]:
                self.select_table.pushButton_2.setEnabled(False)
            elif 'regular_supply_table2021' not in self.data[1]:
                self.select_table.pushButton_3.setEnabled(False)
            elif 'medical_supply_table2021' not in self.data[1]:
                self.select_table.pushButton_4.setEnabled(False)
            elif 'my_camp_info' not in self.data[1]:
                self.select_table.pushButton_5.setEnabled(False)
            elif 'today_all' not in self.data[1]:
                self.select_table.pushButton_6.setEnabled(False)

            self.select_table.show()
            self.select_table.pushButton.clicked.connect(self.launch_main_table_window)
            self.select_table.pushButton_2.clicked.connect(self.launch_injury_table_window)
            self.select_table.pushButton_3.clicked.connect(self.launch_regular_supply_table_window)
            self.select_table.pushButton_4.clicked.connect(self.launch_medical_supply_table_window)
            self.select_table.pushButton_5.clicked.connect(self.launch_my_camp_info_window)
            self.select_table.pushButton_6.clicked.connect(self.launch_today_view_all_window)

    def launch_main_table_window(self):
        self.main_table_win = SysAdmin.MainTable()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "main_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    # self.tmp_label.setMargin(0)
                    # self.tmp_label.setFont(QFont(("MS Shell Dlg 2", 8)))
                    # self.tmp_label.setStyleSheet("QLabel {background-color: red;}")
                    # self.tmp_label.setLineWidth("1")
                    self.main_table_win.gridLayout.addWidget(self.tmp_label, i+1, j)
            # show
            self.main_table_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_injury_table_window(self):
        self.injury_table_win = SysAdmin.InjuryTable()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "injury_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.injury_table_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.injury_table_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_regular_supply_table_window(self):
        self.regular_supply_win = SysAdmin.RegularSupply()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "regular_supply_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.regular_supply_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.regular_supply_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_medical_supply_table_window(self):
        self.medical_supply_win = SysAdmin.MedicalSupply()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "medical_supply_table2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.medical_supply_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.medical_supply_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_my_camp_info_window(self):
        self.my_camp_win = SysAdmin.MyCamp()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "my_camp_info")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.my_camp_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            # show
            self.my_camp_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def launch_today_view_all_window(self):
        self.today_view_win = SysAdmin.TodayAll()
        # get the data
        self.data = self.admin.readTable(self.camp_name, "today_all")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tmp_label.setFrameShape(QFrame.Panel)
                    self.tmp_label.setMinimumHeight(25)
                    self.today_view_win.gridLayout_2.addWidget(self.tmp_label, i + 1, j)
            # show
            self.today_view_win.show()
            print("shown")
        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    # ----------------------- For De-registering camp -----------------------
    def setup_for_drop_database(self):
        print("Drop database signal received")
        print("before focus")

        self.lineEdit.setFocus()
        self.lineEdit.clear()
        self.pushButton_7.setText("DeRegister")
        self.pushButton_7.setEnabled(True)

    def drop_database(self):
        print("Drop database signal2 received")

        self.camp_name = "camp" + self.lineEdit.text()
        self.data = self.admin.deRegister_step1(self.camp_name)
        print(self.data)
        if self.data == -1:
            QMessageBox.critical(self, "Invalid", "Error!! No such camp exists!!\t")
            self.label_6.setText(self.camp_name + " camp does not exists!!")
        else:
            self.response = QMessageBox.question(self, "Are You Sure", self.data)

            if self.response == QMessageBox.Yes:
                self.admin.deRegister_step2(self.camp_name)
                QMessageBox.information(self, "Information", self.camp_name + " de-registered successfully.")
                self.label_6.setText(self.camp_name + " successfully de-registered.")
            elif self.response == QMessageBox.No:
                QMessageBox.information(self, "Abort", self.camp_name + " de-registration aborted!!")
                self.label_6.setText(self.camp_name + " de-registration Abort!!")

    # ----------------------- For registering camp -----------------------
    def setup_for_create_database(self):
        print("Create database signal received")
        print("before focus")

        self.lineEdit.setFocus()
        self.lineEdit.clear()
        self.pushButton_7.setText("Proceed")
        self.pushButton_7.setEnabled(True)

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
            QMessageBox.critical(self, "Error", self.camp_name + " registration failed as the camp already exists!!\t\t")

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

    # ----------------------- ----------------------- -----------------------

    def select_one_of_all_tbl(self):
        self.one_selector.show()

    def list_all_basic_details(self):
        self.pushButton_7.setText("Disabled")
        self.pushButton_7.setEnabled(False)

        print("List all camps and their details signal received")
        self.camp_det_win = SysAdmin.CampDetSupportMem()
        # get the data
        print("window created")

        self.data = self.admin.readTable("all_camp_details", "campdet2021")
        self.data2 = self.admin.readTable("all_camp_details", "support_members2021")
        print(self.data)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data  (basic details :campdet2021 table)
            for i in range(len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.camp_det_win.gridLayout.addWidget(self.tmp_label, i + 1, j)

        if len(self.data2) != 0:
            # set the data  (support member details :support_members2021 table)
            # fill this table half
            half = len(self.data2) // 2
            print(half)
            for i in range(half):
                for j in range(len(self.data2[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data2[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.camp_det_win.gridLayout_2.addWidget(self.tmp_label, i + 1, j)

            for i in range(half, len(self.data2)):
                for j in range(len(self.data2[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data2[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.camp_det_win.gridLayout_4.addWidget(self.tmp_label, i-half + 1, j)

        if len(self.data) != 0 or len(self.data2) != 0:
            self.camp_det_win.show()

        else:
            QMessageBox.critical(self, "Empty", "The table is empty!!\t")

    def list_all_demand_feedback(self):
        self.pushButton_7.setText("Disabled")
        self.pushButton_7.setEnabled(False)

        print("List all camps and their details signal received")
        self.demand_feedback_win = SysAdmin.DemandFeedback()
        # get the data
        print("window created")
        self.data = self.admin.readTable("all_camp_details", "demand2021")
        self.data2 = self.admin.readTable("all_camp_details", "feedback2021")
        print(self.data)
        print(self.data2)

        # if data is there in table then
        if len(self.data) != 0:
            # set the data  (basic details :campdet2021 table)
            half = len(self.data) // 2
            print("in1")
            for i in range(half):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.demand_feedback_win.gridLayout.addWidget(self.tmp_label, i + 1, j)
            print("process half")
            for i in range(half, len(self.data)):
                for j in range(len(self.data[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.demand_feedback_win.gridLayout_2.addWidget(self.tmp_label, i-half + 1, j)
            print("1 done")

        if len(self.data2) != 0:
            # set the data  (basic details :campdet2021 table)
            half = len(self.data2) // 2
            print("in2")
            for i in range(half):
                for j in range(len(self.data2[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data2[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.demand_feedback_win.gridLayout_3.addWidget(self.tmp_label, i + 1, j)
            print("Process")
            for i in range(half, len(self.data2)):
                for j in range(len(self.data2[i])):
                    self.tmp_label = QLabel()
                    self.tmp_label.setText(str(self.data2[i][j]))
                    self.tmp_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                    self.tmp_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.demand_feedback_win.gridLayout_4.addWidget(self.tmp_label, i - half + 1, j)
            print("2 done")

        if len(self.data) != 0 or len(self.data2) != 0:
            self.demand_feedback_win.show()
        else:
            QMessageBox.critical(self, "Empty", "No data sets found")


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
        print(self.which_portal, self.__pswd, self.camp_id)
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
            QMessageBox.critical(self, "Error", "Wrong Password!!\t")
            exit(-1)
        # if password is correct then System Admin window will pop up else exit()
        # create and show sysAdminWindow
        del self.admin
        self.win = SysAdminWindow()
        self.win.showMaximized()

    def camp_admin_window(self):
        print("Success signal from camp_admin_window")
        self.camp_name = "camp" + self.camp_id
        print(self.camp_name)
        try:
            self.admin = CampAdmin.CampAdmin(self.camp_name, self.__pswd)
        except:
            QMessageBox.critical(self, "Error", "Wrong Password!!\t\t")
            exit(-1)
        # if password is correct then Camp Admin window will pop up else exit()
        self.win = CampAdminWindow(self.camp_name)
        # self.win.camp_name_label.setText(self.camp_name)
        # self.win.camp_name_label.hide()
        del self.admin
        self.win.showMaximized()


app = QApplication(sys.argv)
window = ControllerWindow()  # this is the controller window (but never shown)
app.exec()
