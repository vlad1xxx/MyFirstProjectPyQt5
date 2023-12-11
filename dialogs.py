import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QDialog


class RegistrationForm(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('reg_form.ui', self)
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.start_reg.clicked.connect(self.add_account)

    def add_account(self):
        if self.input_name.text() == '':
            self.error_text.setText('Поле "Имя" не должно быть пустым')
        elif self.input_surname.text() == '':
            self.error_text.setText('Поле "Фамилия" не должно быть пустым')
        elif self.input_login.text() == '':
            self.error_text.setText('Поле "Логин" не должно быть пустым')
        elif self.input_password.text() == '':
            self.error_text.setText('Поле "Пароль" не должно быть пустым')
        elif len(self.input_password.text()) < 8:
            self.error_text.setText('Пароль должен содержать больше 7 символов')
        else:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    "first_name"	TEXT,
                    "last_name"	TEXT,
                    "username"	TEXT,
                    "password"	TEXT DEFAULT 0,
                    "heart" INTEGER DEFAULT 5,
                    "coins" INTEGER DEFAULT 0,
                    "xp"    INTEGER DEFAULT 0,
                    "errors"    INTEGER DEFAULT 0,
                    "num_btn"	INTEGER DEFAULT 0,
                    "cond_btn"	INTEGER DEFAULT 0,
                    "loop_btn"	INTEGER DEFAULT 0,
                    "str_btn"	INTEGER DEFAULT 0,
                    "set_btn"	INTEGER DEFAULT 0,
                    "list_btn"	INTEGER DEFAULT 0,
                    "dict_and_tuple_btn"	INTEGER DEFAULT 0,
                    "func_btn"	INTEGER DEFAULT 0,
                    "start_oop_btn"	INTEGER DEFAULT 0,
                    "oop_part2_btn"	INTEGER DEFAULT 0,
                    "oop_part3_btn"	INTEGER DEFAULT 0
                )
            ''')

            data = [self.input_name.text(), self.input_surname.text(),
                    self.input_login.text(), self.input_password.text()]
            cursor.execute('''
            INSERT INTO users (first_name, last_name, username, password) VALUES (?, ?, ?, ?)
            ''', data)
            conn.commit()
            num_id = cursor.execute('''
                SELECT id FROM users WHERE username = ? AND password = ?
            ''', [self.input_login.text(), self.input_password.text()]).fetchall()[0][0]

            cursor.execute('''
                UPDATE last_enter SET id = ?
            ''', [num_id])
            conn.commit()
            conn.close()

            self.parent.name_surname.setText(self.input_name.text() + ' ' + self.input_surname.text())
            self.parent.profile_menu.setCurrentIndex(1)
            self.close()


class EnterForm(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('enter_form.ui', self)
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.start_enter.clicked.connect(self.enter_account)

    def enter_account(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        res = cursor.execute('''
            SELECT * FROM users WHERE username = ? AND password = ?
        ''', [self.input_login.text(), self.input_password.text()]).fetchall()
        conn.commit()
        conn.close()
        if res:
            self.parent.id = res[0][0]
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute('''
                            UPDATE last_enter SET id = ?
                        ''', [self.parent.id])
            conn.commit()
            conn.close()
            self.parent.name.setText(res[0][1])
            self.parent.surname.setText(res[0][2])
            self.parent.xp_count.setText(str(res[0][7]) + 'xp')
            self.parent.errors_count.setText(str(res[0][8]))
            self.parent.count_heart = res[0][5]
            self.parent.coins = res[0][6]
            if bool(res[0][9]):
                self.parent.open_num_btn()
            self.parent.cond_btn.setEnabled(bool(res[0][10]))
            self.parent.profile_menu.setCurrentIndex(1)
            self.close()
        else:
            self.error_text.setText('Неверный логин или пароль')



