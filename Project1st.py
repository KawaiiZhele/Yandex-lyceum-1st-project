import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QLabel, QLineEdit, \
    QCheckBox

letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
numbers = '0123456789'


def name_check(chname):
    global true_name_user
    text, flag = '', True
    for i in chname:
        if i not in letters and i != ' ':
            flag = False
            text = 'В указанном имени присутствуют неизвестные символы'
            break
    if ' ' not in chname and flag:
        flag = False
        text = 'Неправильная форма заполнения.'
    if flag:
        return True
    Question(text)
    return False


def telephone_number_check(chnumber):
    pass


def email_check(chemail):
    pass


def set_text():
    with open('проба.txt', encoding='utf8') as file:
        return file.read()


class FirstWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project1.ui', self)  # Загружаем дизайн

        self.entry_to_user_list.hide()
        self.user_entry.setChecked(True)
        self.user_entry.clicked.connect(self.open)

        self.entry_to_admin_list.hide()
        self.admin_entry.setChecked(True)
        self.admin_entry.clicked.connect(self.open)

        self.d = {self.user_entry: self.entry_to_user_list,
                  self.admin_entry: self.entry_to_admin_list}

        self.dialog_user = UserWidget()
        self.dialog_admin = AdminWidget()
        self.entry_to_user_list.clicked.connect(self.user_run)
        self.entry_to_admin_list.clicked.connect(self.admin_run)

    def user_run(self):
        self.dialog_user.show()

    def admin_run(self):
        self.dialog_admin.show()

    def open(self):
        checkbox = self.sender()
        line = self.d[checkbox]
        if checkbox.isChecked():
            line.hide()
        else:
            line.show()


class UserWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('user.ui', self)

        self.dialog_user_anketa = AnketaWidget()
        self.entry.clicked.connect(self.run)

        self.exit_user.clicked.connect(self.exituser)

    def run(self):
        self.dialog_user_anketa.show()

    def exituser(self):
        self.hide()


class AnketaWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('anketa.ui', self)

        self.exit_ankuser.clicked.connect(self.exit_ank)
        self.save_ankuser.clicked.connect(self.save_ank)  # (ДОРАБОТАТЬ!!!!!!!)

    def exit_ank(self):
        self.hide()

    def save_ank(self):
        if name_check(self.user_name.text()):
            self.user_name.setText('')
            self.hide()


class AdminWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin.ui', self)

        self.dialog_admin_anketa = Anketa2Widget()
        self.entry.clicked.connect(self.run)
        self.exit_admin.clicked.connect(self.exitadmin)

        self.check_text.setText(set_text())

    def run(self):
        self.dialog_admin_anketa.show()

    def exitadmin(self):
        self.hide()


class Anketa2Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('anketa_organisation.ui', self)

        self.exit_ankuser.clicked.connect(self.exit_ank_admin)

    def exit_ank_admin(self):
        self.hide()


class Question(QMessageBox):
    def __init__(self, text):
        super().__init__()
        # uic.loadUi('oshibka.ui', self)

        QMessageBox.question(self, 'Сообщение об ошибке', text,
                             QMessageBox.Ok)
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWidget()
    ex.show()
    sys.exit(app.exec_())
