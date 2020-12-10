from sys import argv, exit
from PyQt5.QtWidgets import QApplication, QMainWindow,\
    QTableWidgetItem, QMenu, QAction, QMessageBox
from UI import Ui_MainWindow
from addEditCoffeeForm import Ui_MainWindow_2
import sqlite3


class Coffeetable(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect('cofee.sqlite')
        self.cur = self.connection.cursor()
        self.initUI()

    def initUI(self):
        self.show_table()

        self.bar = self.menuBar()

        self.action = QAction('Добавить запись', self)
        self.action.triggered.connect(self.open_add_menu)

        self.menu = QMenu()
        self.menu.setTitle('Инструменты')
        self.menu.addAction(self.action)
        self.bar.addMenu(self.menu)

    def show_table(self):
        self.data_from_table = \
            self.cur.execute('''SELECT * FROM data''').fetchall()

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

    def open_add_menu(self):
        self.add_widg = AddCoffee(self)
        self.add_widg.show()


class AddCoffee(QMainWindow, Ui_MainWindow_2):
    def __init__(self, obj):
        super().__init__()
        self.main = obj
        self.setupUi(self)
        self.connection = sqlite3.connect('cofee.sqlite')
        self.cur = self.connection.cursor()
        self.table_row = ''
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.ok_btn)

        self.pushButton_2.clicked.connect(self.close)

        self.comboBox.addItems([str(elem[0]) for elem
                                in self.main.data_from_table])
        self.comboBox.setCurrentText('')
        self.comboBox.currentIndexChanged.connect(self.add_data_from_db)

    def ok_btn(self):
        try:
            data_list = [int(self.comboBox.currentText()), self.lineEdit.text(),
                         self.lineEdit_2.text(), self.lineEdit_3.text(),
                         self.lineEdit_4.text(), int(self.lineEdit_5.text()),
                         int(self.lineEdit_6.text())]
            self.table_row = data_list
            if data_list[0] not in [i[0] for i in self.main.data_from_table]:
                self.cur.execute(f'''INSERT INTO data
                            VALUES({data_list[0]}, '{data_list[1]}',
                                    '{data_list[2]}', '{data_list[3]}',
                                '{data_list[4]}', {data_list[5]},
                                                    {data_list[6]})''')
                self.main.tableWidget.setRowCount(
                    self.main.tableWidget.rowCount()
                    + 1)
                for i in range(7):
                    self.main.tableWidget.setItem(
                        self.main.tableWidget.rowCount()
                        - 1, i,
                        QTableWidgetItem
                        (str(self.table_row[i])))
                self.connection.commit()
            else:
                self.cur.execute(f'''UPDATE data  SET Сорт = '{data_list[1]}',
                        Степень_обжарки = '{data_list[2]}',
                            Молотый_или_в_зёрнах = '{data_list[3]}',
                                Вкус = '{data_list[4]}',
                                    Цена = {data_list[5]},
                                        Масса_упаковки = {data_list[6]}
                                                WHERE ID = {data_list[0]}''')
                self.connection.commit()
                self.main.show_table()

        except ValueError:
            msg = QMessageBox(self)
            msg.setWindowTitle('Ошибка')
            msg.setText('Некорректный ввод')
            msg.show()
            if msg.exec() == QMessageBox.Ok:
                self.main.open_add_menu()

        self.close()

    def add_data_from_db(self):
        elems = [i for i in self.main.data_from_table
                 if str(i[0]) == self.sender().currentText()]

        self.lineEdit.setText(elems[0][1])
        self.lineEdit_2.setText(elems[0][2])
        self.lineEdit_3.setText(elems[0][3])
        self.lineEdit_4.setText(elems[0][4])
        self.lineEdit_5.setText(str(elems[0][5]))
        self.lineEdit_6.setText(str(elems[0][6]))


if __name__ == '__main__':
    app = QApplication(argv)
    widg = Coffeetable()
    widg.show()
    exit(app.exec())
