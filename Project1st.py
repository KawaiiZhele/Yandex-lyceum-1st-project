import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QLabel, QLineEdit, \
    QCheckBox

letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
letters_eng = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'
special = '@.'
special_name = '"'


def name_check(chname):
    text, flag = ['Форма заполнена некорректно. Попробуйте снова.',
                  'Пример заполнения: Иванов Иван Иванович или Петров Петр (Нет отчества)'], True
    flag_len = 0
    if ' ' in chname:
        chname = len(chname.split())
    else:
        flag = False

    for i in chname:
        if i not in letters and i != ' ':
            flag = False
            text[0] = 'В указанном имени присутствуют неизвестные символы.'
            break

    if ' ' not in chname and flag_len != 3:
        flag = False

    if flag and flag_len == 3:
        return True

    Question(text)
    return False


def telephone_number_check(chnumber):
    text, flag = ['Номер телефона введен некорректно. Введите, пожалуйста, заново.',
                  'Пример заполнения: +78005553535 или 78005553535'], True

    if len(chnumber) == 0:
        Question(text)
        return False

    if chnumber[0] == '+':
        chnumber = chnumber[1:]

    if len(chnumber) != 11:
        flag = False

    for i in chnumber:
        if i not in numbers:
            flag = False
            text[0] = 'В указанном номере присутствуют неизвестные символы.'
            break

    if flag:
        return True

    Question(text)
    return False


def email_check(chemail):
    text, flag = ['Электронная почта введена некорректно. Попробуйте снова.',
                  'Пример заполнения: example@gmail.com'], True
    flag_sobaka = 0
    for i in chemail:
        if i not in letters_eng and i not in special:
            flag = False
            text[0] = 'В указанном имени присутствуют неизвестные символы.'
            break
        elif i == '@':
            flag_sobaka += 1
    if flag_sobaka == 1 and flag:
        return True
    flag = False

    Question(text)
    return False


def birth_check(chbirth):
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
        self.user_name.setText('')
        self.tele_user.setText('')
        # self.age_user.setText()
        self.hide()

    def save_ank(self):
        check = [self.user_name, self.job_user, self.tele_user, self.email_user, self.net_user,
                 self.birth_user, self.placelive_user, self.salary_user, self.citizenship_user,
                 self.lenguage_user, self.education_user, self.about_you_user]
        flag = True
        # ВСТАВИТЬ СЮДА ИЗ 213
        if flag:
            if name_check(self.user_name.text()) and \
                    telephone_number_check(self.tele_user.text()) and \
                    email_check(self.email_user.text()):
                self.exit_ank()


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

        QMessageBox.question(self, 'Сообщение об ошибке', f'{text[0]}\n{text[1]}',
                             QMessageBox.Ok)
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWidget()
    ex.show()
    sys.exit(app.exec_())
