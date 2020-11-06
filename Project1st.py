import sys
import sqlite3
import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QLabel, QLineEdit, \
    QCheckBox

letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
letters_eng = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'

id_name_user = 1


def get_result_user(idname, user, user1, user2):
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    print(5)
    users = (idname + 1, user[0].text(), int(user1[0].text()), user[1].text(), user[2].text(),
             user[3].text(), user2[0].toPlainText(), user1[1].text(), user[4].text(),
             int(user[5].text()), user[6].text(), user2[1].toPlainText(), user2[2].toPlainText(),
             user1[2].text(), user2[3].toPlainText())
    print(45)
    cur.execute("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", users)
    print(6)
    con.commit()
    con.close()


def get_id_name_user():
    global id_name_user
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    id_name = cur.execute("""
                            SELECT id_counter
                            FROM last_user_id
                            """).fetchall()
    con.close()
    for item in id_name:
        return item[0]


def upload_id_name_user():
    global id_name_user
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    id_name = cur.execute("""
                                UPDATE last_user_id
                                SET id_counter = id_counter + 1
                                """).fetchall()
    con.close()


def name_check(chname):
    text, flag = ['Форма заполнена некорректно. Попробуйте снова.',
                  'Пример заполнения: Иванов Иван Иванович или Петров Петр (Нет отчества)'], True
    flag_len = 0
    if ' ' in chname:
        flag_len = len(chname.split())
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

    if ' ' in chnumber:
        chnumber = ''.join(chnumber.split())

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
        if i not in letters_eng and i != '@' and i != '.':
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


def birth_check(age, chbirth):
    text = ['Дата рождения введена некорректно. Попробуйте снова.',
            'Она должна соответствовать Вашему возрасту.']
    chbirth = list(map(lambda x: int(x), chbirth.split('.')))
    year_before = datetime.date(chbirth[2], chbirth[1], chbirth[0])
    year_now = datetime.date.today()

    if (year_now.year - year_before.year) >= 16 and \
            (year_now.year - year_before.year) == age:
        return True
    Question(text)
    return False


def age_check(chage):
    text, flag = ['Вы забыли указать свой возраст.',
                  'Пример заполнения: 23'], True
    if chage == 0:
        Question(text)
        return 'Забыл'

    if chage >= 16:
        return True

    else:
        text = ['Вы слишком малы, извините. Приходите позже.', '']
        Question(text)
        return 'Мал'


def salary_check(chsalary):
    text, flag = ['Зарплатные ожидания введены некорректно. Введите, пожалуйста, заново.',
                  'Пример заполнения: 15000'], True

    if len(chsalary) == 0:
        Question(text)
        return False

    if ' ' in chsalary:
        chsalary = ''.join(chsalary.split())

    for i in chsalary:
        if i not in numbers:
            flag = False
            text[0] = 'В указанном номере присутствуют неизвестные символы.'
            break
    if flag:
        return True

    Question(text)
    return False


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
        self.save_ankuser.clicked.connect(self.save_ank)

    def exit_ank(self, check):
        for i in check[0]:
            i.setText('')
        # ДОДЕЛАТЬ УДАЛЕНИЕ ПРЕДЫДУЩЕЙ ДАТЫ С ЭКРАНА
        for i in check[1]:
            i.clear()
        for i in check[2]:
            i.setText('')

        self.hide()

    def save_ank(self):
        global id_name
        check_user = [[self.user_name, self.job_user, self.tele_user, self.email_user,
                       self.placelive_user, self.salary_user, self.citizenship_user],
                      [self.age_user, self.birth_user, self.job_age_user],
                      [self.net_user, self.lenguage_user, self.education_user, self.about_you_user]]
        flag = True

        for i in check_user[0]:
            if len(i.text()) == 0:
                flag = False
                Question(['Заполните пустые ячейки.',
                          'Не забудьте все проверить перед сохранением.'])
                break

        for i in check_user[2]:
            if len(i.toPlainText()) == 0:
                flag = False
                Question(['Заполните пустые ячейки.',
                          'Не забудьте все проверить перед сохранением.'])
                break

        if flag:
            flag_age = age_check(int(self.age_user.text()))
            if flag_age == 'Мал':
                self.exit_ank(check_user)
            elif flag_age == 'Забыл':
                pass
            else:
                if name_check(self.user_name.text()) and flag_age and \
                        telephone_number_check(self.tele_user.text()) and \
                        email_check(self.email_user.text()) and \
                        salary_check(self.salary_user.text()) and \
                        birth_check(int(self.age_user.text()), self.birth_user.text()):
                    print(2)
                    get_result_user(get_id_name_user(), check_user[0], check_user[1], check_user[2])
                    print(3)
                    upload_id_name_user()
                    self.exit_ank(check_user)


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
