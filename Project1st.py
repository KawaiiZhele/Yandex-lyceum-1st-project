import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QLabel, QLineEdit, \
    QCheckBox


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

        self.dialog = UserWidget()
        self.dialog3 = AdminWidget()
        self.entry_to_user_list.clicked.connect(self.user_run)
        self.entry_to_admin_list.clicked.connect(self.admin_run)

    def user_run(self):
        self.dialog.show()

    def admin_run(self):
        self.dialog3.show()

    def open(self):
        checkbox = self.sender()
        line = self.d[checkbox]
        if checkbox.isChecked():
            line.hide()
        else:
            line.show()


class UserWidget(QMainWindow):  # соискатель
    def __init__(self):
        super().__init__()
        uic.loadUi('user.ui', self)

        self.dialog1 = AnketaWidget()
        self.entry.clicked.connect(self.run)

        self.exit_user.clicked.connect(self.exituser)

    def run(self):
        self.dialog1.show()

    def exituser(self):
        self.dialog.hide()
        # self.dialog1.hide()


class AnketaWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('anketa.ui', self)

        self.exit_ankuser.clicked.connect(self.exit_ank)

    def exit_ank(self):
        self.dialog1.hide()




class AdminWidget(QMainWindow):  # работодатель
    def __init__(self):
        super().__init__()
        uic.loadUi('admin.ui', self)

        self.dialog2 = AnketaWidget()
        # self.entry.clicked.connect(self.run)

    def run(self):
        self.dialog2.show()


class Anketa2Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('anketa.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstWidget()
    ex.show()
    sys.exit(app.exec_())
