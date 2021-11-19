import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5 import uic


class Edit_add_window(QWidget):
    def __init__(self, status):
        super().__init__()
        self.status = status
        self.initUI()

    def initUI(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        if self.status == 'open':
            self.corr_id = window.db[0]
            self.id.setText(f'ID – {str(self.corr_id)}')
            self.name.setText(window.db[1])
            self.roasting.setText(window.db[2])
            self.type.setText(window.db[3])
            self.taste.setText(window.db[4])
            self.price.setText(str(window.db[5]))
            self.volume.setText(str(window.db[6]))
        else:
            self.corr_id = None
        self.btn_save.clicked.connect(self.save)

    def save(self):
        try:
            rec = self.corr_id, self.name.text(), self.roasting.text(), self.type.text(), self.taste.text(),\
                  self.price.text(), self.volume.text()
            if self.status == 'open':
                window.cur.execute(f"UPDATE coffees SET name = '{rec[1]}', roast = '{rec[2]}', type = '{rec[3]}',"
                                   f"taste = '{rec[4]}', price = {rec[5]}, volume = {rec[6]} WHERE ID = {rec[0]}")
            else:
                window.cur.execute(f"INSERT INTO coffees VALUES (?, ?, ?, ?, ?, ?, ?)", (rec[0], rec[1], rec[2], rec[3],
                                                                                         rec[4], rec[5], rec[6]))
            window.cur.commit()
            QMessageBox.information(window, 'Успешно', f'Запись успешно созданна', QMessageBox.Ok)
            self.close()
        except Exception as error:
            print(error)
            QMessageBox.critical(self, 'Внимание', 'Неверный формат данных', QMessageBox.Ok)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('main.ui', self)
        self.cur = sqlite3.connect('coffee.sqlite')
        self.cur.cursor()
        self.setWindowTitle('Coffee Database')
        self.btn.clicked.connect(self.load_coffee)
        self.open.clicked.connect(self.edit_coffee)
        self.create.clicked.connect(self.edit_coffee)

    def load_coffee(self):
        if all(i in '0123456789' for i in self.search.text()) and self.search.text() != '':
            try:
                self.db = self.cur.execute(f"SELECT * FROM coffees WHERE ID = {int(self.search.text())}").fetchone()
                self.id.setText(f'ID: {str(self.db[0])}')
                self.name.setText(f'Название сорта: {self.db[1]}')
                self.roasting.setText(f'Степень обжарки: {self.db[2]}')
                self.type.setText(f'Молотый/в зернах: {self.db[3]}')
                self.taste.setText(f'Вкус: {self.db[4]}')
                self.price.setText(f'Цена: {str(self.db[5])}')
                self.volume.setText(f'Объём упаковки: {str(self.db[6])}')
                self.status.setText('')
            except Exception:
                self.status.setText(f'Запись с ID - {self.search.text()} не найденна')
        else:
            self.status.setText('Неккоректный ID')

    def edit_coffee(self):
        try:
            if self.sender() == self.open:
                if all(i in '0123456789' for i in self.search.text()) and self.search.text() != '':
                    try:
                        self.db = self.cur.execute(f"SELECT * FROM coffees WHERE ID ="
                                                   f"{int(self.search.text())}").fetchone()
                    except Exception:
                        self.status.setText(f'Запись с ID - {self.search.text()} не найденна')
                else:
                    self.status.setText('Неккоректный ID')
                self.edit_window = Edit_add_window('open')
                self.edit_window.show()
                self.status.setText('')
            else:
                self.edit_window = Edit_add_window('create')
                self.edit_window.show()
                self.status.setText('')
        except Exception as error:
            print(error)
            self.status.setText('Выберите кофе который хотите изменить')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
