import sys
import sqlite3
import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QLabel, QLineEdit, \
    QCheckBox
from PyQt5 import QtCore, QtWidgets

letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
letters_eng = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'


def get_result_user(idname, user, user1, user2):
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    users = (idname + 1, user[0].text(), user1[0].text(), user[1].text(), user[2].text(),
             user[3].text(), user2[0].toPlainText(), user[4].text(),
             int(user[5].text()), user[6].text(), user2[1].toPlainText(), user2[2].toPlainText(),
             int(user1[1].text()), user2[3].toPlainText())
    cur.execute("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", users)
    con.commit()
    con.close()


def get_reslt_admin(idname, user, user1, user2):
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    users = (idname + 1, user[0].text(), user[1].text(), user[2].text(), int(user[3].text()),
             user1[0].text(), user2[0].toPlainText(), user2[1].toPlainText(),
             user2[2].toPlainText(), user2[3].toPlainText())
    cur.execute("INSERT INTO admin VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", users)
    con.commit()
    con.close()


def get_id_name_user():
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    id_name = cur.execute("""
                            SELECT id_counter_user
                            FROM last_id
                            """).fetchall()
    con.close()
    for item in id_name:
        return item[0]


def get_id_name_admin():
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    id_name = cur.execute("""
                            SELECT id_counter_admin
                            FROM last_id
                            """).fetchall()
    con.close()
    for item in id_name:
        return item[0]


def upload_id_name_user():
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    cur.execute("""
                    UPDATE last_id
                    SET id_counter_user = id_counter_user + 1
                    """).fetchall()
    con.commit()
    con.close()


def upload_id_name_admin():
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    cur.execute("""
                    UPDATE last_id
                    SET id_counter_admin = id_counter_admin + 1
                    """).fetchall()
    con.commit()
    con.close()


def name_check(chname):
    text, flag = ['Форма заполнена некорректно. Попробуйте снова.',
                  'Пример заполнения: Иванов Иван Иванович или Петров Петр (Нет отчества)'], True
    otch = []
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
        otch = chname.split()
        if len(otch[0]) >= 1 and len(otch[1]) >= 2 and len(otch[2]) >= 3:
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
    flag_dot = 0
    if chemail[0] in numbers:
        flag = False
    for i in chemail:
        if i not in letters_eng and i not in numbers and i != '@' and i != '.':
            flag = False
            text[0] = 'В указанном имени присутствуют неизвестные символы.'
            break
        elif i == '@':
            flag_sobaka += 1
    if '@.' in chemail or '.@' in chemail:
        flag = False
    if flag_sobaka == 1 and flag:
        chemail = chemail.split('@')
        for i in chemail[1]:
            if i in numbers:
                flag = False
                break
            if i == '.':
                flag_dot += 1
        if flag and flag_dot == 1:
            return True
    Question(text)
    return False


def birth_check(chbirth):
    text = ['Дата рождения введена некорректно. Попробуйте снова.',
            'Она должна соответствовать Вашему возрасту.']
    chbirth = list(map(lambda x: int(x), chbirth.split('.')))
    year_before = datetime.date(chbirth[2], chbirth[1], chbirth[0])
    year_now = datetime.date.today()

    if (year_now.year - year_before.year) >= 16:
        return True
    else:
        text = ['Вы слишком малы, извините. Приходите позже.', '']
        Question(text)
        return 'Мал'


def salary_check(chsalary):
    text, flag = ['Зарплатные ожидания введены некорректно. Введите, пожалуйста, заново.',
                  'Пример заполнения: 15000'], True

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


def job_check(chjob):
    text, flag = ['Должность введена некорректно. Введите, пожалуйста, заново.',
                  'Программист'], True

    for i in chjob:
        if i not in letters and i != ' ':
            flag = False
            text[0] = 'В указанном имени присутствуют неизвестные символы.'
            break

    if flag:
        return True

    Question(text)
    return False


def profile_check(chprofile):
    text, flag = ['Ссылка введена некорректно. Попробуйте снова.',
                  'https://vk.com/'], True
    if ' ' in chprofile:
        chprofile = chprofile.split()
    else:
        chprofile = [chprofile]

    for i in chprofile:
        if not i.startswith('https://'):
            flag = False
            break

    if flag:
        return True

    Question(text)
    return False


def id_count():
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    result = cur.execute("""
                        SELECT DISTINCT id
                        FROM user
                        """).fetchall()
    return result


def id_count_ad():
    con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
    cur = con.cursor()
    result = cur.execute("""
                            SELECT DISTINCT id
                            FROM admin
                            """).fetchall()
    return result


def set_text_user():
    user_text_user = ''
    for i in id_count():
        con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
        cur = con.cursor()
        rows = cur.execute("SELECT * FROM user WHERE id = ?", str(i[0])).fetchall()
        text = []
        for j in rows[0]:
            text.append(str(j))
        user_text_user += f'ФИО пользователя: {text[1]}\n' + \
                          f'Возраст: {text[2]}\n' + \
                          f'Должность: {text[3]}\n' + \
                          f'Мобильный телефон: {text[4]}\n' + \
                          f'Электронная почта: {text[5]}\n' + \
                          f'Профиль в соц.сетях: {text[6]}\n' + \
                          f'Место проживания: {text[7]}\n' + \
                          f'Зарплатные ожидания: {text[8]}\n' + \
                          f'Гражданство: {text[9]}\n' + \
                          f'Язык: {text[10]}\n' + \
                          f'Образование: {text[11]}\n' + \
                          f'Опыт работы: {text[12]}\n' + \
                          f'Информация о себе: {text[13]}\n' + \
                          '----------------------------------\n'
    return user_text_user


def set_text_admin():
    user_text_user = ''
    for i in id_count_ad():
        con = sqlite3.connect(r'C:\Users\Екатерина\PycharmProjects\pythonProject\user_anketa.sqlite')
        cur = con.cursor()
        rows = cur.execute("SELECT * FROM admin WHERE id = ?", str(i[0])).fetchall()
        text = []
        for j in rows[0]:
            text.append(str(j))
        user_text_user += f'Именование организации: {text[1]}\n' + \
                          f'Должность: {text[2]}\n' + \
                          f'Город: {text[3]}\n' + \
                          f'Уровень зарплаты: {text[4]}\n' + \
                          f'Требуемый опыт работы: {text[5]}\n' + \
                          f'Компания: {text[6]}\n' + \
                          f'Обязанности: {text[7]}\n' + \
                          f'Требования: {text[8]}\n' + \
                          f'Условия: {text[9]}\n' + \
                          '----------------------------------\n'
    return user_text_user


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
        self.upload.clicked.connect(self.uploadank)

        self.user_text_user.setText(set_text_user())
        self.admin_text_user.setText(set_text_admin())

    def run(self):
        self.dialog_user_anketa.show()

    def exituser(self):
        self.hide()

    def uploadank(self):
        self.user_text_user.setText(set_text_user())
        self.admin_text_user.setText(set_text_admin())


class AnketaWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('anketa.ui', self)

        self.exit_ankuser.clicked.connect(self.exit_ank)
        self.save_ankuser.clicked.connect(self.save_ank)

    def exit_ank(self):
        check = [[self.user_name, self.job_user, self.tele_user, self.email_user,
                  self.placelive_user, self.salary_user, self.citizenship_user],
                 [self.birth_user, self.job_age_user],
                 [self.net_user, self.lenguage_user, self.education_user, self.about_you_user]]
        for i in check[0]:
            i.setText('')
        for i in check[1]:
            i.clear()
        for i in check[2]:
            i.setText('')
        self.birth_user.setDate(QtCore.QDate(2020, 1, 1))
        self.birth_user.setDisplayFormat("dd.MM.yyyy")
        self.hide()

    def save_ank(self):
        flag = True
        text = ['Заполните пустые ячейки.', 'Не забудьте все проверить перед сохранением.']
        check_user = [[self.user_name, self.job_user, self.tele_user, self.email_user,
                       self.placelive_user, self.salary_user, self.citizenship_user],
                      [self.birth_user, self.job_age_user],
                      [self.net_user, self.lenguage_user, self.education_user, self.about_you_user]]

        for i in check_user[0]:
            if len(i.text().strip()) == 0:
                flag = False
                Question(text)
                break
        if flag:
            for i in check_user[2]:
                if len(i.toPlainText().strip()) == 0:
                    flag = False
                    Question(text)
                    break
        if flag:
            flag_age = birth_check(self.birth_user.text())
            if flag_age == 'Мал':
                self.exit_ank()
            else:
                if name_check(self.user_name.text()) and flag_age and \
                        telephone_number_check(self.tele_user.text()) and \
                        email_check(self.email_user.text()) and \
                        salary_check(self.salary_user.text()) and \
                        job_check(self.job_user.text()) and \
                        profile_check(self.net_user.toPlainText()):
                    get_result_user(get_id_name_user(), check_user[0], check_user[1], check_user[2])
                    upload_id_name_user()
                    self.exit_ank()


class AdminWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('admin.ui', self)

        self.dialog_admin_anketa = Anketa2Widget()
        self.entry.clicked.connect(self.run)
        self.exit_admin.clicked.connect(self.exitadmin)

        self.user_text_admin.setText(set_text_user())
        self.admin_text_admin.setText(set_text_admin())

        self.upload.clicked.connect(self.uploadank)

    def run(self):
        self.dialog_admin_anketa.show()

    def exitadmin(self):
        self.hide()

    def uploadank(self):
        self.user_text_admin.setText(set_text_user())
        self.admin_text_admin.setText(set_text_admin())


class Anketa2Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('anketa_organisation.ui', self)

        self.exit_ankuser.clicked.connect(self.exit_ank_admin)
        self.save_ankadmin.clicked.connect(self.save_ank_admin)

    def exit_ank_admin(self):
        check = [[self.name_admin, self.job_admin, self.town_admin, self.salary_admin],
                 [self.job_age_user], [self.company_admin, self.duties_user,
                                       self.requirements_admin, self.conditions_admin]]
        for i in check[0]:
            i.setText('')
        for i in check[1]:
            i.clear()
        for i in check[2]:
            i.setText('')
        self.hide()

    def save_ank_admin(self):
        check_admin = [[self.name_admin, self.job_admin, self.town_admin, self.salary_admin],
                       [self.job_age_user], [self.company_admin, self.duties_user,
                                             self.requirements_admin, self.conditions_admin]]
        text = ['Заполните пустые ячейки.', 'Не забудьте все проверить перед сохранением.']
        flag = True

        for i in check_admin[0]:
            if len(i.text().strip()) == 0:
                flag = False
                Question(text)
                break

        if flag:
            for i in check_admin[2]:
                if len(i.toPlainText().strip()) == 0:
                    flag = False
                    Question(text)
                    break

        if flag:
            if len(check_admin[1][0].text()) == 0:
                flag = False
                Question(text)

        if flag:
            if salary_check(self.salary_admin.text()) and job_check(self.job_admin.text()):
                get_reslt_admin(get_id_name_admin(), check_admin[0], check_admin[1], check_admin[2])
                upload_id_name_admin()
                self.exit_ank_admin()


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
