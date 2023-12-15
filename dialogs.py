import sqlite3
from datetime import datetime

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
                    "password"	TEXT,
                    "heart" INTEGER DEFAULT 5,
                    "coins" INTEGER DEFAULT 0,
                    "xp"    INTEGER DEFAULT 0,
                    "errors"    INTEGER DEFAULT 0,
                    "num_btn"	INTEGER DEFAULT 1,
                    "cond_btn"	INTEGER DEFAULT 1,
                    "loop_btn"	INTEGER DEFAULT 1,
                    "str_btn"	INTEGER DEFAULT 1,
                    "set_btn"	INTEGER DEFAULT 1,
                    "list_btn"	INTEGER DEFAULT 1,
                    "dict_and_tuple_btn"	INTEGER DEFAULT 1,
                    "func_btn"	INTEGER DEFAULT 1,
                    "start_oop_btn"	INTEGER DEFAULT 1,
                    "oop_part2_btn"	INTEGER DEFAULT 1,
                    "oop_part3_btn"	INTEGER DEFAULT 1,
                    "last_enter_time" INTEGER
                )
            ''')
            cursor.execute("""
                UPDATE users SET last_enter_time = ?
            """, [datetime.now().timestamp()])
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

            self.parent.name.setText(self.input_name.text())
            self.parent.surname.setText(self.input_surname.text())
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
            cursor.execute('''
                UPDATE users SET last_enter_time = ? WHERE id = ?
            ''', [datetime.now().timestamp(), self.parent.id])
            conn.commit()
            conn.close()
            self.parent.name.setText(res[0][1])
            self.parent.surname.setText(res[0][2])
            self.parent.xp = res[0][7]
            self.parent.errors = res[0][8]
            self.parent.count_heart = res[0][5]
            self.parent.coins = res[0][6]
            if bool(res[0][9]):
                self.parent.open_num_btn()
            if bool(res[0][10]):
                self.parent.open_cond_btn()
            if bool(res[0][11]):
                self.parent.open_loop_btn()
            if bool(res[0][12]):
                self.parent.open_str_btn()
            self.parent.cond_btn.setEnabled(bool(res[0][10]))
            self.parent.update_data()
            self.parent.profile_menu.setCurrentIndex(1)
            if self.parent.count_heart < 5:
                self.parent.update_hp_timer()
            self.close()
        else:
            self.error_text.setText('Неверный логин или пароль')


class ChooseThemeForm(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi('choose_theme_form.ui', self)
        self.initUi()
        self.parent = parent

    def initUi(self):
        self.py_part_1_btn.clicked.connect(self.choose_py_theme)
        self.py_part_2_btn.clicked.connect(self.choose_py_theme)

    def choose_py_theme(self):
        btn_text = self.sender().text()
        if btn_text == 'Основы Python часть 1':
            self.parent.stacked_themes.setCurrentIndex(0)
        elif btn_text == 'Основы Python часть 2':
            self.parent.stacked_themes.setCurrentIndex(1)
        self.close()


