from sys import argv, exit
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget,\
    QTableWidgetItem
from PyQt5 import uic
import sqlite3


class Cofeetable(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI.ui', self)
        self.connection = sqlite3.connect('cofee.sqlite')
        self.cur = self.connection.cursor()
        self.data_from_table = \
            self.cur.execute('''SELECT * FROM data''').fetchall()
        self.initUI()

    def initUI(self):
        self.tableWidget.setColumnCount(len(self.data_from_table[0]))
        self.tableWidget.setRowCount(len(self.data_from_table))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Сорт',
                                                    'Степень обжарки',
                                                    'Молотый/в зернах',
                                                    'Вкус', 'Цена(руб.)',
                                                    'Масса(гр.)'])
        for row in range(len(self.data_from_table)):
                for col in range(len(self.data_from_table[0])):
                    it = QTableWidgetItem(str(self.data_from_table[row][col]))
                    self.tableWidget.setItem(row, col, it)


if __name__ == '__main__':
    app = QApplication(argv)
    widg = Cofeetable()
    widg.show()
    exit(app.exec())

