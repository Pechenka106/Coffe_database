import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic


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

    def load_coffee(self):
        if all(i in '0123456789' for i in self.search.text()) and self.search.text() != '':
            try:
                db = self.cur.execute(f"SELECT * FROM coffees WHERE ID = {int(self.search.text())}").fetchone()
                self.id.setText(f'ID: {str(db[0])}')
                self.name.setText(f'Название сорта: {db[1]}')
                self.roasting.setText(f'Степень обжарки: {db[2]}')
                self.type.setText(f'Молотый/в зернах: {db[3]}')
                self.taste.setText(f'Вкус: {db[4]}')
                self.price.setText(f'Цена: {str(db[5])}')
                self.volume.setText(f'Объём упаковки: {str(db[6])}')
            except Exception:
                self.status.setText(f'Запись с ID - {self.search.text()} не найденна')
        else:
            self.status.setText('Неккоректный ID')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
