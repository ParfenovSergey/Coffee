import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.load_data()
        self.add_button.clicked.connect(self.add_window)
        self.save_db_button.clicked.connect(self.save_data)
        self.aw = None

    def add_window(self):
        if self.aw is None:
            self.aw = AdditionalWindow()
            self.aw.show()
        else:
            self.aw.close()
            self.aw = None

    def save_data(self):
        cur = self.con.cursor()
        cur.execute("DROP TABLE IF EXISTS coffee")
        cur.execute("""CREATE TABLE coffee (
    idr      INTEGER PRIMARY KEY
                     UNIQUE,
    sort     TEXT,
    roasting TEXT,
    type,
    flavour,
    price,
    volume
);
""")
        for i in range(self.table.rowCount()):
            tmp = []
            for j in range(self.table.columnCount()):
                tmp.append(self.table.item(i, j).text())
            cur.execute("""INSERT INTO coffee (idr, sort, roasting, type, flavour, price, volume)
                        VALUES ('%i', '%s', '%s', '%s', '%s', '%s', '%s');""" % (int(tmp[0]),
                                                                                 tmp[1], tmp[2], tmp[3],
                                                                                 tmp[4], tmp[5], tmp[6]))
        self.con.commit()

    def load_data(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()

        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/зерновой', 'Описание вкуса',
             'Цена', 'Объём упаковки'])

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))


class AdditionalWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.save_button.clicked.connect(self.save)

    def save(self):
        if all((self.lineEdit.text(),
                self.lineEdit_2.text(),
                self.lineEdit_3.text(),
                self.lineEdit_4.text(),
                self.lineEdit_5.text(),
                self.lineEdit_6.text())):
            ex.table.insertRow(ex.table.rowCount())
            ex.table.setItem(ex.table.rowCount() - 1, 0, QTableWidgetItem(str(ex.table.rowCount())))
            ex.table.setItem(ex.table.rowCount() - 1, 1, QTableWidgetItem(self.lineEdit.text()))
            ex.table.setItem(ex.table.rowCount() - 1, 2, QTableWidgetItem(self.lineEdit_2.text()))
            ex.table.setItem(ex.table.rowCount() - 1, 3, QTableWidgetItem(self.lineEdit_3.text()))
            ex.table.setItem(ex.table.rowCount() - 1, 4, QTableWidgetItem(self.lineEdit_4.text()))
            ex.table.setItem(ex.table.rowCount() - 1, 5, QTableWidgetItem(self.lineEdit_5.text()))
            ex.table.setItem(ex.table.rowCount() - 1, 6, QTableWidgetItem(self.lineEdit_6.text()))
            self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
    ex.con.close()
