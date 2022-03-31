import sys
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow,QMenu,QSystemTrayIcon,QApplication
from python_graphql_client import GraphqlClient




class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        uic.loadUi('ui/home_screen.ui', self)
        self.setFixedHeight(850)
        self.setFixedWidth(1120)
        self.setWindowTitle('BUS BOOKING APP')
        
        self.title = self.findChild(QtWidgets.QLabel, 'title')
        self.title.setText("BUS BOOKING SYSTEM")
        
        
        #getting data from hasura graphql api
        def getData():
            client = GraphqlClient(endpoint="http://127.0.0.1:8080/v1/graphql")
            query = """
             query{
            bokings{
                id
                name
                email
                phone_number
                gender
                departure_city
                destination_city
                ticket_number
                seat_pos
                }
                }
                """
            data = client.execute(query=query)
            return data
        data = getData()["data"]
        bookings= data["bokings"] #lol bokings is a typo on hasura table
        print(bookings)
        
        
        row=0
        self.tableWidget.setRowCount(len(bookings))
        for booking in bookings:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(booking[str("id")])) #str to change int id to string
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(booking["name"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(booking["email"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(booking["phone_number"]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(booking["gender"]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(booking["departure_city"]))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(booking["destination_city"]))
            self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(booking["ticket_number"]))
            self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(booking["seat_pos"]))
            row=row+1
            
        
        def search(self,s):
            self.tableWidget.setCurrentItem(None)
            
            if not s:
                return
            matching_items =self.tableWidget.findItems(s, Qt.MatchContains)
            if matching_items:
                item =matching_items[0]
                self.tableWidget.setCurrentItem(item)
        
        self.searchbar.textChanged.connect(search)    
            
        self.show()
        
# create pyqt5 app
App = QApplication(sys.argv)
trayIco = QSystemTrayIcon(QIcon('64.png') , parent=App)
trayIco.show()
menu = QMenu()
aboutUs = menu.addAction('About App')
quitApp = menu.addAction('Exit or close App')
quitApp.triggered.connect(App.quit)
trayIco.setContextMenu(menu)

window = Window()

sys.exit(App.exec())

    
