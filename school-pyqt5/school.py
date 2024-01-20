from PyQt5.QtCore import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con
from datetime import date
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog,QPrintPreviewDialog  #importing library to print receipt

ui, _ = loadUiType("school.ui") # connecting ui to python

class MainApp(QMainWindow, ui):
     def __init__(self):
     	QMainWindow.__init__(self)
     	self.setupUi(self)


     	self.tabWidget.setCurrentIndex(0)  # for making username as opening page
     	self.tabWidget.tabBar().setVisible(False)  # hide tabs
     	self.menubar.setVisible(False)  # hide menu bar
     	self.b01.clicked.connect(self.login) # moving to home page

     	self.menu11.triggered.connect(self.show_add_new_student_tab) # submenu for adding new student
     	self.b12.clicked.connect(self.save_student_details)   #button for saving the student details
     	self.menu12.triggered.connect(self.show_edit_or_delete_student_tab) # submenu for edit/delete stduent
     	self.cb21.currentIndexChanged.connect(self.fill_details_when_combo_box_selected) # for editing details data fills automatically
     	self.b21.clicked.connect(self.edit_student_details) # button for edit student details
     	self.b22.clicked.connect(self.delete_student_details) # button for delete student details

     	self.menu21.triggered.connect(self.show_mark_tab) # button for show marks tab
     	self.b31.clicked.connect(self.save_mark_details) # button for saving marks
     	self.cb32.currentIndexChanged.connect(self.fill_exam_names_in_combobox_for_registration_number_selected) 
     	self.b32.clicked.connect(self.fill_exam_details_in_textbox_for_examname_selected) # for editing details data fills automatically
     	self.b33.clicked.connect(self.update_mark_details) # button for edit marks
     	self.b34.clicked.connect(self.delete_mark_details) # button for delete marks

     	self.menu31.triggered.connect(self.show_attendance_tab) # button for show attendance tab
     	self.b41.clicked.connect(self.save_attendance_details) # button for saving attendance details
     	self.cb42.currentIndexChanged.connect(self.fill_date_in_combobox_for_reg_no_selected) # for editing details data fills automatically   	
     	self.b42.clicked.connect(self.fill_attendance_status) # button for fill attendance
     	self.b43.clicked.connect(self.update_attendance_details) # button for update attendace
     	self.b44.clicked.connect(self.delete_attendance_details) # button for delete attendance 
     
     	self.menu41.triggered.connect(self.show_fees_tab) # button for show fees tab
     	self.b51.clicked.connect(self.save_fees_details) # button for save fees details
     	self.b81.clicked.connect(self.print_file) # button for print the receipt
     	self.b82.clicked.connect(self.cancel_print) # button for cancel the print
     	self.cb52.currentIndexChanged.connect(self.fill_receipt_details_in_textboxes_for_receipt_combo_selected) # data fill automatically
     	self.b52.clicked.connect(self.update_fees_details) # button for update fees details
     	self.b53.clicked.connect(self.delete_fees_details) # button for delete fees details


     	self.menu51.triggered.connect(self.show_report) # submenu for display stduent report 
     	self.menu52.triggered.connect(self.show_report) # submenu for display student marks
     	self.menu53.triggered.connect(self.show_report) # submenu for display student attendance
     	self.menu54.triggered.connect(self.show_report) # submenu for display student fees


     	self.menu61.triggered.connect(self.logout) # menu for logout

     ##### login form #####

     def login(self):
     	un = self.tb01.text() # username
     	pw = self.tb02.text() # password
     	if (un == "admin" and pw == "admin"):
     		self.menubar.setVisible(True)  # enables the menu bar 
     		self.tabWidget.setCurrentIndex(1)  # show the current form and enable the menu bar
     	else:
     		QMessageBox.information(self,"school management system","Invalid admin login details, Try again !")
     		self.l01.setText("Invalid admin login details, Try again !")
    
    ##### add new student######

     def show_add_new_student_tab(self):
    	 self.tabWidget.setCurrentIndex(2)
    	 self.fill_next_registration_number()

     def fill_next_registration_number(self):  # automatically fill the next reg number
     	try:
     		rn = 0
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from student")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				rn += 1
     		self.tb11.setText(str(rn+1))
     	except con.Error as e:
        		print("Error occured in select student reg number"+ e)       

     def save_student_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.tb11.text()
     		full_name = self.tb12.text()
     		gender = self.cb11.currentText()  	
     		date_of_birth = self.tb13.text()
     		age = self.tb14.text()
     		address = self.mtb11.toPlainText()
     		phone = self.tb15.text()
     		email = self.tb16.text()
     		standard = self.cb12.currentText()

     		qry = "insert into student (registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)" # store in dbms
     		value = (registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard)
     		cursor.execute(qry,value)
     		mydb.commit()

     		self.l11.setText("Student details saved sucessfully")
     		QMessageBox.information(self, "School management system","student details added sucessfully")

     		#### after filling all text box clear and return to home page#####
     		self.tb11.setText("")
     		self.tb12.setText("")
     		self.tb13.setText("")
     		self.tb14.setText("")
     		self.tb15.setText("")
     		self.tb16.setText("")
     		self.mtb11.setText("")
     		self.tabWidget.setCurrentIndex(1)
     	except con.Error as e:
          	self.l11.setText("Error in save student form " + e)

    ##### FILL THE DETAILS AUTOMATICALLY AFTER SELECTION OF REG NUMBER######

     def show_edit_or_delete_student_tab(self):
    	 self.tabWidget.setCurrentIndex(3)
    	 self.fill_registration_number_in_combobox()

     def fill_registration_number_in_combobox(self):  # automatically fill the next reg number
     	try:
     		self.cb21.clear()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from student")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				self.cb21.addItem(str(stud[1]))
     	except con.Error as e:
        		print("Error occured in fill reg number in combobox"+ e)       

     def fill_details_when_combo_box_selected(self):  # automatically fill the next reg number
     	try:
     		
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from student where registration_number = '"+ self.cb21.currentText() +"'")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				self.tb21.setText(str(stud[2]))
     				self.tb26.setText(str(stud[3]))
     				self.tb22.setText(str(stud[4]))
     				self.tb23.setText(str(stud[5]))
     				self.mtb21.setText(str(stud[6]))
     				self.tb24.setText(str(stud[7]))
     				self.tb25.setText(str(stud[8]))
     				self.tb27.setText(str(stud[9]))

     	except con.Error as e:
        		print("Error occured in fill details when combobox selected"+ e)       

       ##### edit student details##### 		
     def edit_student_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.cb21.currentText()
     		full_name = self.tb21.text()
     		gender = self.tb26.text()  	
     		date_of_birth = self.tb22.text()
     		age = self.tb23.text()
     		address = self.mtb21.toPlainText()
     		phone = self.tb24.text()
     		email = self.tb25.text()
     		standard = self.tb27.text()

     		qry = "update student set full_name = '"+ full_name +"',gender = '"+ gender +"',date_of_birth = '"+ date_of_birth +"',age = '"+ age +"',address = '"+ address +"',phone = '"+phone+"',email = '"+ email +"',standard ='"+ standard +"' where registration_number = '"+ registration_number +"'" #updating 
     		cursor.execute(qry)
     		mydb.commit()

     		self.l21.setText("Student details modified sucessfully")
     		QMessageBox.information(self, "School management system","student details modified sucessfully")
     		
     		self.tb21.setText("")
     		self.tb22.setText("")
     		self.tb23.setText("")
     		self.tb24.setText("")
     		self.tb25.setText("")
     		self.tb26.setText("")
     		self.tb27.setText("")
     		self.mtb21.setText("")
     		self.tabWidget.setCurrentIndex(1)
     	except con.Error as e:
          	self.l21.setText("Error in edit student form " + e)

     def delete_student_details(self):
     	m = QMessageBox.question(self,"Delete", "Are you sure want to delete this student details", QMessageBox.Yes|QMessageBox.No)
     	if m == QMessageBox.Yes:
	     	try:
	     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
	     		cursor = mydb.cursor()    
	     		registration_number = self.cb21.currentText()
	
	     		qry = "delete from student where registration_number = '"+ registration_number +"'" #updating 
	     		cursor.execute(qry)
	     		mydb.commit()

	     		self.l21.setText("Student details deleted sucessfully")
	     		QMessageBox.information(self, "School management system","student details deleted sucessfully")
	     		self.tabWidget.setCurrentIndex(1) # back to home page after deleting
	     	except con.Error as e:
	          	self.l21.setText("Error in delete student form " + e)


      ###### mark details ########

     def show_mark_tab(self):
     	self.tabWidget.setCurrentIndex(4)
     	self.fill_registration_number_in_combobox_in_mark_tab()


     def fill_registration_number_in_combobox_in_mark_tab(self):  # automatically fill the next reg number
     	try:
     		self.cb31.clear()
     		self.cb32.clear()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from student")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				self.cb31.addItem(str(stud[1]))
     				self.cb32.addItem(str(stud[1]))
     	except con.Error as e:
        		print("Error occured in fill reg number in combobox"+ e)       


           ##### save mark details ######

     def save_mark_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.cb31.currentText()
     		exam_name = self.tb31.text()
     		langauge = self.tb32.text()  	
     		english = self.tb33.text()
     		maths = self.tb34.text()
     		science = self.tb35.text()
     		social_studies = self.tb36.text()
     		hindi = self.tb37.text()

     		qry = "insert into mark(registration_number,exam_name,language,english,maths,science,social_studies,hindi) values(%s,%s,%s,%s,%s,%s,%s,%s)" #writing query to stor the information to dbms
     		value = (registration_number,exam_name,langauge,english,maths,science,social_studies,hindi)
     		cursor.execute(qry,value)
     		mydb.commit()

     		self.l31.setText("mark details saved sucessfully")
     		QMessageBox.information(self, "School management system","mark details added sucessfully")

     		self.tb31.setText("")
     		self.tb32.setText("")
     		self.tb33.setText("")
     		self.tb34.setText("")
     		self.tb35.setText("")
     		self.tb36.setText("")
     		self.tb37.setText("")
     		self.tabWidget.setCurrentIndex(1)
     	except con.Error as e:
          	self.l31.setText("Error in mark student form " + e)



     def fill_exam_names_in_combobox_for_registration_number_selected(self):  # automatically fill the next reg number
     	try:
     		self.cb33.clear()
     		registration_number = self.cb32.currentText()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from mark where registration_number='"+ registration_number +"'")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				self.cb33.addItem(str(stud[2]))
     	except con.Error as e:
        		print("Error occured in fill exam name in combobox"+ e)       


     def fill_exam_details_in_textbox_for_examname_selected(self):  # automatically fill the mark for editing
     	try:
     		registration_number = self.cb32.currentText()
     		exam_name = self.cb33.currentText()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from mark where registration_number='"+ registration_number +"' and exam_name = '"+ exam_name +"'")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				self.tb38.setText(str(stud[3]))
     				self.tb39.setText(str(stud[4]))
     				self.tb310.setText(str(stud[5]))
     				self.tb311.setText(str(stud[6]))
     				self.tb312.setText(str(stud[7]))
     				self.tb313.setText(str(stud[8]))
     	except con.Error as e:
        		print("Error occured in fill mark details in combobox"+ e)       

        		
     def update_mark_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.cb32.currentText()
     		exam_name = self.cb33.currentText()
     		language = self.tb38.text()
     		english = self.tb39.text()
     		maths = self.tb310.text()
     		science = self.tb311.text()
     		social_studies = self.tb312.text()
     		hindi = self.tb313.text()
     		
     		qry = "update mark set language = '"+ language +"',english = '"+ english +"',maths = '"+ maths +"',science = '"+ science +"',social_studies = '"+ social_studies +"',hindi = '"+ hindi +"' where registration_number = '"+ registration_number +"' and exam_name = '"+ exam_name +"'" #updating 
     		cursor.execute(qry)
     		mydb.commit()

     		self.l32.setText("mark details modified sucessfully")
     		QMessageBox.information(self, "School management system","mark details modified sucessfully")

     		self.tb38.setText("")
     		self.tb39.setText("")
     		self.tb310.setText("")
     		self.tb311.setText("")
     		self.tb312.setText("")
     		self.tb313.setText("")
     		self.tabWidget.setCurrentIndex(1)
     	except con.Error as e:
          	self.l32.setText("Error in edit mark form " + e)


     def delete_mark_details(self):
     	m = QMessageBox.question(self,"Delete", "Are you sure want to delete this mark details", QMessageBox.Yes|QMessageBox.No)
     	if m == QMessageBox.Yes:
	     	try:
	     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
	     		cursor = mydb.cursor()    
	     		registration_number = self.cb32.currentText()
	     		exam_name = self.cb33.currentText()
	
	     		qry = "delete from mark where registration_number = '"+ registration_number +"' and exam_name = '"+ exam_name +"'"#updating 
	     		cursor.execute(qry)
	     		mydb.commit()

	     		self.l32.setText("mark details deleted sucessfully")
	     		QMessageBox.information(self, "School management system","mark details deleted sucessfully")
	     		self.tb38.setText("")
	     		self.tb39.setText("")
	     		self.tb310.setText("")
	     		self.tb311.setText("")
	     		self.tb312.setText("")
	     		self.tb313.setText("")

	     		self.tabWidget.setCurrentIndex(1) # back to home page after deleting
	     	except con.Error as e:
	          	self.l32.setText("Error in delete mark form " + e)


            ###### ATTENDANCE CODING ##########
     def show_attendance_tab(self):
     	self.tabWidget.setCurrentIndex(5)
     	self.fill_registration_number_in_combobox_for_attendance_tab()
     	self.tb41.setText(str(date.today()))   # print today date

     def fill_registration_number_in_combobox_for_attendance_tab(self):  # automatically fill the next reg number
     	try:
     		self.cb41.clear()
     		self.cb42.clear()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from student")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				self.cb41.addItem(str(stud[1]))
     				self.cb42.addItem(str(stud[1]))
     	except con.Error as e:
        		print("Error occured in fill reg number in combobox"+ e)       


     def save_attendance_details(self): #saving the attendance details
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.cb41.currentText()
     		attendance_date = self.tb41.text()
     		morning = self.tb42.text()
     		evening = self.tb43.text()  	
     		
     		qry = "insert into attendance(registration_number,attendance_date,morning,evening) values(%s,%s,%s,%s)" #dbms story
     		value = (registration_number,attendance_date,morning,evening)
     		cursor.execute(qry,value)
     		mydb.commit()

     		self.l41.setText("attendance details saved sucessfully")
     		QMessageBox.information(self, "School management system","Attendance details added sucessfully")
     		self.tb42.setText("")
     		self.tb43.setText("")

     	except con.Error as e:
          	self.l41.setText("Error in save attendance form " + e)



     def fill_date_in_combobox_for_reg_no_selected(self):  # automatically fill the next reg number and date
     	try:
     		self.cb43.clear()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from attendance where registration_number = '"+ self.cb42.currentText() +"'")
     		result = cursor.fetchall()
     		if result:
     			for att in result:
     				self.cb43.addItem(str(att[2]))
     	except con.Error as e:
        		print("Error occured in fill date in combobox"+ e)       


     def fill_attendance_status(self):  # after clicking the button shows the attendance data
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from attendance where registration_number = '"+ self.cb42.currentText() +"' and attendance_date = '"+ self.cb43.currentText() +"'")
     		result = cursor.fetchall()
     		if result:
     			for att in result:
     				self.tb44.setText(str(att[3]))
     				self.tb45.setText(str(att[4]))

     	except con.Error as e:
        		print("Error occured in fill attendance status in combobox"+ e)       



        		
     def update_attendance_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.cb42.currentText()
     		attendance_date = self.cb43.currentText()
     		morning = self.tb44.text()
     		evening = self.tb45.text()
     		
     		qry = "update attendance set morning = '"+ morning +"',evening = '"+ evening +"' where registration_number = '"+ registration_number +"' and attendance_date = '"+ attendance_date +"'" #updating 
     		cursor.execute(qry)
     		mydb.commit()

     		self.tb44.setText("")
     		self.tb45.setText("")

     		self.l42.setText("attendance details modified sucessfully")
     		QMessageBox.information(self, "School management system","Attendance details modified sucessfully")
     	except con.Error as e:
          	self.l42.setText("Error in edit attendance form " + e)



        		
     def delete_attendance_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.cb42.currentText()
     		attendance_date = self.cb43.currentText()

     		
     		qry = "delete from attendance where registration_number = '"+ registration_number +"' and attendance_date = '"+ attendance_date +"'" #updating 
     		cursor.execute(qry)
     		mydb.commit()

     		self.tb44.setText("")
     		self.tb45.setText("")

     		self.l42.setText("attendance details deleted sucessfully")
     		QMessageBox.information(self, "School management system","Attendance details deleted sucessfully")
     		self.tabWidget.setCurrentIndex(1)
     	except con.Error as e:
          	self.l42.setText("Error in delete attendance form " + e)


            ###### FEES CODING ##########
     def show_fees_tab(self):
     	self.tabWidget.setCurrentIndex(6)
     	self.fill_registration_number_in_combobox_for_fees_tab()
     	self.tb54.setText(str(date.today()))   # print today date
     	self.fill_next_receipt_number()
     	self.fill_receipt_number_in_combobox_for_edit_fees_tab()


     def fill_registration_number_in_combobox_for_fees_tab(self):  # automatically fill the next reg number
     	try:
     		self.cb51.clear()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from student")
     		result = cursor.fetchall()
     		if result:
     			for stud in result:
     				self.cb51.addItem(str(stud[1]))
     	except con.Error as e:
        		print("Error occured in fill reg number in combobox"+ e)       


     def fill_next_receipt_number(self):  # automatically fill the next receipt number
     	try:
     		rn = 0
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from fees")
     		result = cursor.fetchall()
     		if result:
     			for rec in result:
     				rn +=1
     		self.tb51.setText(str(rn+1))
     	except con.Error as e:
        		print("Error occured in fill reg number in combobox"+ e)       


     def save_fees_details(self): #saving fees details
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		registration_number = self.cb51.currentText()
     		receipt_number = self.tb51.text()
     		reason = self.tb52.text()
     		amount = self.tb53.text()
     		fees_date = self.tb54.text()  	
     		
     		qry = "insert into fees(receipt_number,registration_number,reason,amount,fees_date) values(%s,%s,%s,%s,%s)" #writing query to stor the information to dbms
     		value = (receipt_number,registration_number,reason,amount,fees_date)
     		cursor.execute(qry,value)
     		mydb.commit()

     		self.l51.setText("fees details saved sucessfully")
     		QMessageBox.information(self, "School management system","fees details added sucessfully")
     		self.fill_receipt_number_in_combobox_for_edit_fees_tab()

     		    ###PRINT RECEIPT####
     		self.l81.setText(self.tb51.text())
     		self.l82.setText(self.tb54.text())
     		self.l86.setText(self.tb54.text())
     		self.l84.setText(self.tb53.text())
     		self.l85.setText(self.tb52.text())
     		cursor.execute("select * from student where registration_number = '"+ registration_number +"'")
     		result = cursor.fetchone()
     		if result:
     			self.l83.setText(str(result[2]))
     		self.tabWidget.setCurrentIndex(8)

     		self.tb52.setText("")
     		self.tb53.setText("")
     		self.fill_next_receipt_number()

     	except con.Error as e:
          	self.l51.setText("Error in save fees form " + e)


     def fill_receipt_number_in_combobox_for_edit_fees_tab(self):  # automatically fill the next reg number
     	try:
     		self.cb52.clear()
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from fees")
     		result = cursor.fetchall()
     		if result:
     			for rec in result:
     				self.cb52.addItem(str(rec[1]))
     	except con.Error as e:
        		print("Error occured in fill receipt number in combobox"+ e)       



     def fill_receipt_details_in_textboxes_for_receipt_combo_selected(self):  # automatically fill the next reg number
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()  #holds the value
     		cursor.execute("select * from fees where receipt_number = '"+ self.cb52.currentText() +"'")
     		result = cursor.fetchall()
     		if result:
     			for rec in result:
     				self.tb55.setText(str(rec[2]))
     				self.tb56.setText(str(rec[3]))
     				self.tb57.setText(str(rec[4]))
     				self.tb58.setText(str(rec[5]))
     	except con.Error as e:
        		print("Error occured in fill receipt details in textboxes"+ e)       


        		
     def update_fees_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		receipt_number = self.cb52.currentText()
     		registration_number = self.tb55.text()
     		reason = self.tb56.text()
     		amount = self.tb57.text()
     		fees_date = self.tb58.text()
     		
     		qry = "update fees set registration_number = '"+ registration_number +"',reason = '"+ reason +"',amount = '"+ amount +"',fees_date = '"+ fees_date +"' where receipt_number = '"+ receipt_number +"'" # updating  
     		cursor.execute(qry)
     		mydb.commit()

     		self.l52.setText("fees details modified sucessfully")
     		QMessageBox.information(self, "School management system","fees details modified sucessfully")
      		    ###PRINT RECEIPT####
     		self.l81.setText(self.cb52.currentText())
     		self.l82.setText(self.tb58.text())
     		self.l86.setText(self.tb58.text())
     		self.l84.setText(self.tb57.text())
     		self.l85.setText(self.tb56.text())
     		cursor.execute("select * from student where registration_number = '"+ registration_number +"'")
     		result = cursor.fetchone()
     		if result:
     			self.l83.setText(str(result[2]))
     		self.tabWidget.setCurrentIndex(8)

     		self.tb55.setText("")
     		self.tb56.setText("")
     		self.tb57.setText("")
     		self.tb58.setText("")

   	
     	except con.Error as e:
          	self.l52.setText("Error in edit fees form " + e)


        		
     def delete_fees_details(self):
     	try:
     		mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     		cursor = mydb.cursor()    
     		receipt_number = self.cb52.currentText()
	
     		qry = "delete from fees where receipt_number = '"+ receipt_number +"'" # delete the row  
     		cursor.execute(qry)
     		mydb.commit()

     		self.l52.setText("fees details deleted sucessfully")
     		QMessageBox.information(self, "School management system","fees details deleted sucessfully")
     		self.tb55.setText("")
     		self.tb56.setText("")
     		self.tb57.setText("")
     		self.tb58.setText("")
     		self.tabWidget.setCurrentIndex(1)

     	except con.Error as e:
          	self.l52.setText("Error in delete fees form " + e)


             ###### REPORT FORM ######

     def show_report(self):
     	table_name = self.sender()
     	self.l61.setText(table_name.text())
     	self.tabWidget.setCurrentIndex(7)
     	try:
     		self.tableReport.setRowCount(0)
     		if(table_name.text() == "Student Reports"):
     			mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     			cursor = mydb.cursor()
     			qry = "select registration_number,full_name,gender,date_of_birth,age,address,phone,email,standard from student"
     			cursor.execute(qry)
     			result = cursor.fetchall()
     			r = 0
     			c = 0
     			for row_number, row_data in enumerate(result):
     				r += 1
     				c = 0
     				for row_number, data in enumerate(row_data):
     					c += 1
     			self.tableReport.clear()
     			self.tableReport.setColumnCount(c)
     			for row_number, row_data in enumerate(result):
     				self.tableReport.insertRow(row_number)
     				for column_number, data in enumerate(row_data):
     					self.tableReport.setItem(row_number,column_number,QTableWidgetItem(str(data)))
     			self.tableReport.setHorizontalHeaderLabels(['Register number','Name','Gender','Date of Birth','Age','Address','Phone','Email','Standard'])


     		if(table_name.text() == "Mark Reports"):
     			mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     			cursor = mydb.cursor()
     			qry = "select registration_number,exam_name,language,english,maths,science,social_studies,hindi from mark"
     			cursor.execute(qry)
     			result = cursor.fetchall()
     			r = 0
     			c = 0
     			for row_number, row_data in enumerate(result):
     				r += 1
     				c = 0
     				for row_number, data in enumerate(row_data):
     					c += 1
     			self.tableReport.clear()
     			self.tableReport.setColumnCount(c)
     			for row_number, row_data in enumerate(result):
     				self.tableReport.insertRow(row_number)
     				for column_number, data in enumerate(row_data):
     					self.tableReport.setItem(row_number,column_number,QTableWidgetItem(str(data)))
     			self.tableReport.setHorizontalHeaderLabels(['Register number','Exam Name','Language','English','Maths','Science','Social studies','Hindi'])


     		if(table_name.text() == "Attendance Reports"):
     			mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     			cursor = mydb.cursor()
     			qry = "select registration_number,attendance_date,morning,evening from attendance"
     			cursor.execute(qry)
     			result = cursor.fetchall()
     			r = 0
     			c = 0
     			for row_number, row_data in enumerate(result):
     				r += 1
     				c = 0
     				for row_number, data in enumerate(row_data):
     					c += 1
     			self.tableReport.clear()
     			self.tableReport.setColumnCount(c)
     			for row_number, row_data in enumerate(result):
     				self.tableReport.insertRow(row_number)
     				for column_number, data in enumerate(row_data):
     					self.tableReport.setItem(row_number,column_number,QTableWidgetItem(str(data)))
     			self.tableReport.setHorizontalHeaderLabels(['Register number','Attendance date','Morning','Evening'])


     		if(table_name.text() == "Fees Reports"):
     			mydb = con.connect(host="localhost",user="root",password="",db="school") # connecting through the dbms
     			cursor = mydb.cursor()
     			qry = "select receipt_number,registration_number,reason,amount,fees_date from fees"
     			cursor.execute(qry)
     			result = cursor.fetchall()
     			r = 0
     			c = 0
     			for row_number, row_data in enumerate(result):
     				r += 1
     				c = 0
     				for row_number, data in enumerate(row_data):
     					c += 1
     			self.tableReport.clear()
     			self.tableReport.setColumnCount(c)
     			for row_number, row_data in enumerate(result):
     				self.tableReport.insertRow(row_number)
     				for column_number, data in enumerate(row_data):
     					self.tableReport.setItem(row_number,column_number,QTableWidgetItem(str(data)))
     			self.tableReport.setHorizontalHeaderLabels(['Receipt Number','Register number','Reason','Amount','Fees Date'])

     	except con.Error as e:
          	print("Error in report from" + e)



             ###### PRINT RECEIPT FUNCTION ######
     def print_file(self):
     	printer = QPrinter(QPrinter.HighResolution)
     	dialog = QPrintDialog(printer,self)
     	if dialog.exec_() == QPrintDialog.Accepted:
     		self.tabWidget.print_(printer)

     def cancel_print(self):
     	self.tabWidget.setCurrentIndex(1)
  

             ###### LOGOUT FUNCTION ######
     def logout(self):
     	self.menubar.setVisible(False)
     	self.tb01.setText("")
     	self.tb02.setText("")
     	self.tabWidget.setCurrentIndex(0)
     	QMessageBox.information(self, "School management system","You are logged out sucessfully")     	


def main():
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()

