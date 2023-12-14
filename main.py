import contextlib
import sys
import sqlite3
from datetime import datetime
from io import StringIO
from dialogs import RegistrationForm, EnterForm

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox


class PythonExecutor:
    @staticmethod
    def execute(code):
        with StringIO() as output_buffer, contextlib.redirect_stdout(output_buffer):
            try:
                exec(code)
            except Exception as e:
                return f"Error: {e}"
            return output_buffer.getvalue()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('project.ui', self)
        self.id = None
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''
                    CREATE TABLE IF NOT EXISTS last_enter (
                    id INTEGER DEFAULT 0)
                    ''')
        res = cur.execute('''
            SELECT id FROM last_enter
        ''').fetchall()
        if not res:
            cur.execute('''
                        INSERT INTO last_enter (id) VALUES (0)
                    ''')
        else:
            self.id = res[0][0]
        conn.commit()
        conn.close()
        print(res)
        self.name_object = None
        self.first_miss = True
        self.is_low_five_hp = False
        self.count_heart = 5
        self.errors = 0
        self.xp = 0
        self.coins = 0
        if self.id != 0:
            self.set_data()
        self.initUI()

    def initUI(self):
        self.update_data()
        self.createvar_btn.clicked.connect(self.choose_themes)
        self.num_btn.clicked.connect(self.choose_themes)
        self.cond_btn.clicked.connect(self.choose_themes)
        self.loop_btn.clicked.connect(self.choose_themes)
        self.continue_createvar_btn_1.clicked.connect(self.next_page_createvar)
        self.continue_createvar_btn_2.clicked.connect(self.next_page_createvar)
        self.continue_createvar_btn_3.clicked.connect(self.next_page_createvar)
        self.continue_cond_btn_1.clicked.connect(self.next_page_cond)
        self.answer_edit_createvar_1.textChanged.connect(self.change_size)
        self.answer_edit_cond_2.textChanged.connect(self.change_size)
        self.answer_edit_num_6.textChanged.connect(self.change_size)
        self.answer_edit_cond_7.textChanged.connect(self.change_size)
        self.answer_edit_loop_2.textChanged.connect(self.change_size)
        self.answer_edit_loop_4.textChanged.connect(self.change_size)

        self.create_profile_btn.clicked.connect(self.registration)
        self.enter_btn.clicked.connect(self.enter)
        self.exit_from_account.clicked.connect(self.exit_account)
        self.run_btn.clicked.connect(self.run_code)
        self.open_btn.clicked.connect(self.open_file)
        self.save_btn.clicked.connect(self.save_file)
        self.exit_btn.clicked.connect(self.exit_btn_pressed)
        self.restart_createvar()
        self.restart_num()
        self.restart_cond()
        self.restart_loop()

    def choose_themes(self):
        text = self.sender().text()
        if self.check_hp():
            if text == 'Создание переменных':
                self.main_menu.setCurrentIndex(1)
                self.themes.setCurrentIndex(0)
                self.tasks_createvar.setCurrentIndex(0)
            elif text == 'Работа с числами':
                self.main_menu.setCurrentIndex(1)
                self.themes.setCurrentIndex(1)
                self.tasks_num.setCurrentIndex(0)
            elif text == 'Условные операторы':
                self.main_menu.setCurrentIndex(1)
                self.themes.setCurrentIndex(2)
                self.tasks_cond.setCurrentIndex(0)
            elif text == 'Циклы':
                self.main_menu.setCurrentIndex(1)
                self.themes.setCurrentIndex(3)
                self.tasks_loop.setCurrentIndex(0)

    def next_page_createvar(self):
        self.tasks_createvar.setCurrentIndex(self.tasks_createvar.currentIndex() + 1)

    def next_page_num(self):
        self.tasks_num.setCurrentIndex(self.tasks_num.currentIndex() + 1)

    def next_page_cond(self):
        self.tasks_cond.setCurrentIndex(self.tasks_cond.currentIndex() + 1)

    def next_page_loop(self):
        self.tasks_loop.setCurrentIndex(self.tasks_loop.currentIndex() + 1)

    def change_size(self):
        res = self.sender()
        text_width = QFontMetrics(res.font()).width(res.text())
        new_width = text_width + 10
        res.setFixedWidth(new_width)

    def check_answer_createvar_1(self):
        if (self.answer_edit_createvar_1.text() == 'car = "Porsche"'
                or self.answer_edit_createvar_1.text() == "car = 'Porsche'"):
            self.continue_createvar_btn_4.setText('Продолжить')
            self.continue_createvar_btn_4.clicked.connect(self.next_page_createvar)
            self.xp += 25
            self.update_data()
            self.name_object = self.progress_createvar_1
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_createvar()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_createvar_2(self):
        self.continue_createvar_btn_5.setText('Продолжить')
        self.continue_createvar_btn_5.clicked.connect(self.next_page_createvar)
        self.xp += 25
        self.update_data()
        self.frame_console_1.show()
        self.name_object = self.progress_createvar_2
        self.start_progress_bar()

    def check_answer_createvar_3(self):
        if self.answer_edit_createvar_4.toPlainText() == 'name = "Hello, Qt!"\nprint(name)' \
                or self.answer_edit_createvar_4.toPlainText() == "name = 'Hello, Qt!'\nprint(name)":
            self.continue_createvar_btn_6.setText('Завершить')
            self.continue_createvar_btn_6.clicked.connect(self.open_num_btn)
            self.xp += 25
            self.coins += 100
            self.update_data()
            self.frame_console_2.show()
            self.progress_createvar_3.setValue(100)
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_createvar()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def restart_createvar(self):
        self.main_menu.setCurrentIndex(0)
        self.continue_createvar_btn_6.disconnect()
        self.answer_edit_createvar_1.clear()
        self.answer_edit_createvar_1.resize(21, 31)
        self.answer_edit_createvar_4.clear()
        self.progress_createvar_1.setValue(0)
        self.progress_createvar_2.setValue(0)
        self.progress_createvar_3.setValue(0)
        self.frame_console_1.hide()
        self.frame_console_2.hide()
        self.continue_createvar_btn_4.setText('Проверить')
        self.continue_createvar_btn_4.disconnect()
        self.continue_createvar_btn_5.setText('Проверить')
        self.continue_createvar_btn_5.disconnect()
        self.continue_createvar_btn_6.setText('Проверить')
        self.continue_createvar_btn_4.clicked.connect(self.check_answer_createvar_1)
        self.continue_createvar_btn_5.clicked.connect(self.check_answer_createvar_2)
        self.continue_createvar_btn_6.clicked.connect(self.check_answer_createvar_3)

    def check_answer_num_1(self):
        if self.answer_edit_num_1.text() == '5':
            self.continue_num_btn_1.setText('Продолжить')
            self.continue_num_btn_1.clicked.connect(self.next_page_num)
            self.xp += 25
            self.update_data()
            self.name_object = self.progress_num_1
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_num()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_num_2(self):
        if self.answer_edit_num_2.text() == '+ 1':
            self.continue_num_btn_2.setText('Продолжить')
            self.continue_num_btn_2.clicked.connect(self.next_page_num)
            self.xp += 25
            self.update_data()
            self.frame_console_5.show()
            self.name_object = self.progress_num_2
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_num()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_num_3(self):
        if self.answer_edit_num_3.text() == '*':
            self.continue_num_btn_3.setText('Продолжить')
            self.continue_num_btn_3.clicked.connect(self.next_page_num)
            self.xp += 25
            self.update_data()
            self.frame_console_6.show()
            self.name_object = self.progress_num_3
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_num()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_num_4(self):
        if self.answer_edit_num_4.text() == '%':
            self.continue_num_btn_4.setText('Продолжить')
            self.continue_num_btn_4.clicked.connect(self.next_page_num)
            self.xp += 25
            self.update_data()
            self.frame_console_7.show()
            self.name_object = self.progress_num_4
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_num()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_num_5(self):
        if self.answer_edit_num_5.text() == '+ 1':
            self.continue_num_btn_5.setText('Продолжить')
            self.continue_num_btn_5.clicked.connect(self.next_page_num)
            self.xp += 25
            self.update_data()
            self.frame_console_8.show()
            self.name_object = self.progress_num_5
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_num()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_num_6(self):
        if self.answer_edit_num_6.text() == 'private + public' or self.answer_edit_num_6.text() == 'public + private':
            self.continue_num_btn_6.setText('Завершить')
            self.continue_num_btn_6.clicked.connect(self.open_cond_btn)
            self.xp += 25
            self.coins += 100
            self.update_data()
            self.frame_console_9.show()
            self.progress_num_6.setValue(100)

        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_num()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def restart_num(self):
        self.main_menu.setCurrentIndex(0)
        self.answer_edit_num_1.setText('')
        self.answer_edit_num_1.resize(31, 21)
        self.answer_edit_num_2.setText('')
        self.answer_edit_num_2.resize(31, 21)
        self.frame_console_5.hide()
        self.answer_edit_num_3.setText('')
        self.answer_edit_num_3.resize(21, 21)
        self.frame_console_6.hide()
        self.answer_edit_num_4.setText('')
        self.answer_edit_num_4.resize(21, 21)
        self.frame_console_7.hide()
        self.answer_edit_num_5.setText('')
        self.answer_edit_num_5.resize(31, 21)
        self.frame_console_8.hide()
        self.answer_edit_num_6.setText('')
        self.answer_edit_num_6.resize(21, 21)
        self.frame_console_9.hide()
        self.progress_num_1.setValue(0)
        self.progress_num_2.setValue(0)
        self.progress_num_3.setValue(0)
        self.progress_num_4.setValue(0)
        self.progress_num_5.setValue(0)
        self.progress_num_6.setValue(0)
        self.continue_num_btn_1.setText('Проверить')
        self.continue_num_btn_2.setText('Проверить')
        self.continue_num_btn_3.setText('Проверить')
        self.continue_num_btn_4.setText('Проверить')
        self.continue_num_btn_5.setText('Проверить')
        self.continue_num_btn_6.setText('Проверить')
        self.continue_num_btn_1.disconnect()
        self.continue_num_btn_1.clicked.connect(self.check_answer_num_1)
        self.continue_num_btn_2.disconnect()
        self.continue_num_btn_2.clicked.connect(self.check_answer_num_2)
        self.continue_num_btn_3.disconnect()
        self.continue_num_btn_3.clicked.connect(self.check_answer_num_3)
        self.continue_num_btn_4.disconnect()
        self.continue_num_btn_4.clicked.connect(self.check_answer_num_4)
        self.continue_num_btn_5.disconnect()
        self.continue_num_btn_5.clicked.connect(self.check_answer_num_5)
        self.continue_num_btn_6.disconnect()
        self.continue_num_btn_6.clicked.connect(self.check_answer_num_6)

    def check_answer_cond_1(self):
        self.continue_cond_btn_2.setText('Продолжить')
        self.continue_cond_btn_2.clicked.connect(self.next_page_cond)
        self.xp += 25
        self.update_data()
        self.frame_console_17.show()
        self.name_object = self.progress_cond_1
        self.start_progress_bar()

    def check_answer_cond_2(self):
        if self.answer_edit_cond_1.text() == 'if':
            self.continue_cond_btn_3.setText('Продолжить')
            self.continue_cond_btn_3.clicked.connect(self.next_page_cond)
            self.xp += 25
            self.update_data()
            self.frame_console_18.show()
            self.name_object = self.progress_cond_2
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_cond()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_cond_3(self):
        if self.answer_edit_cond_2.text() == 'else:':
            self.continue_cond_btn_4.setText('Продолжить')
            self.continue_cond_btn_4.clicked.connect(self.next_page_cond)
            self.xp += 25
            self.update_data()
            self.frame_console_11.show()
            self.name_object = self.progress_cond_3
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_cond()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_cond_4(self):
        if self.answer_edit_cond_6.text() == 'elif':
            self.continue_cond_btn_8.setText('Продолжить')
            self.continue_cond_btn_8.clicked.connect(self.next_page_cond)
            self.xp += 25
            self.update_data()
            self.frame_console_12.show()
            self.name_object = self.progress_cond_4
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_cond()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_cond_5(self):
        if self.answer_edit_cond_7.text() == 'and':
            self.continue_cond_btn_9.setText('Завершить')
            self.continue_cond_btn_9.clicked.connect(self.open_loop_btn)
            self.xp += 25
            self.coins += 100
            self.update_data()
            self.frame_console_12.show()
            self.progress_cond_5.setValue(100)
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_cond()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def restart_cond(self):
        self.main_menu.setCurrentIndex(0)
        self.continue_cond_btn_2.disconnect()
        self.continue_cond_btn_2.setText('Проверить')
        self.continue_cond_btn_2.clicked.connect(self.check_answer_cond_1)
        self.progress_cond_1.setValue(0)
        self.frame_console_17.hide()
        self.frame_console_18.hide()
        self.continue_cond_btn_3.disconnect()
        self.continue_cond_btn_3.setText('Проверить')
        self.continue_cond_btn_3.clicked.connect(self.check_answer_cond_2)
        self.progress_cond_2.setValue(0)
        self.answer_edit_cond_1.clear()
        self.frame_console_11.hide()
        self.answer_edit_cond_2.clear()
        self.continue_cond_btn_4.disconnect()
        self.continue_cond_btn_4.setText('Проверить')
        self.continue_cond_btn_4.clicked.connect(self.check_answer_cond_3)
        self.progress_cond_3.setValue(0)
        self.answer_edit_cond_2.resize(41, 21)
        self.frame_console_12.hide()
        self.answer_edit_cond_6.clear()
        self.continue_cond_btn_8.disconnect()
        self.continue_cond_btn_8.clicked.connect(self.check_answer_cond_4)
        self.continue_cond_btn_8.setText('Проверить')
        self.progress_cond_4.setValue(0)
        self.frame_console_13.hide()
        self.continue_cond_btn_9.disconnect()
        self.continue_cond_btn_9.clicked.connect(self.check_answer_cond_5)
        self.continue_cond_btn_9.setText('Проверить')
        self.progress_cond_5.setValue(0)
        self.answer_edit_cond_7.clear()

    def check_answer_loop_1(self):
        self.continue_loop_btn_1.setText('Продолжить')
        self.continue_loop_btn_1.clicked.connect(self.next_page_loop)
        self.frame_console_10.show()
        self.name_object = self.progress_loop_1
        self.start_progress_bar()

    def check_answer_loop_2(self):
        if (self.answer_edit_loop_2.text() == 'while num != 8:' or self.answer_edit_loop_2.text() == 'while num < 8:'
                or self.answer_edit_loop_2.text() == 'while num <= 7:'):
            self.continue_loop_btn_2.setText('Продолжить')
            self.continue_loop_btn_2.clicked.connect(self.next_page_loop)
            self.frame_console_20.show()
            self.name_object = self.progress_loop_2
            self.start_progress_bar()
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_loop()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def check_answer_loop_3(self):
        self.continue_loop_btn_3.setText('Продолжить')
        self.continue_loop_btn_3.clicked.connect(self.next_page_loop)
        self.frame_console_14.show()
        self.name_object = self.progress_loop_3
        self.start_progress_bar()

    def check_answer_loop_4(self):
        if self.answer_edit_loop_4.text() == 'for i in range(5):':
            self.continue_loop_btn_4.setText('Завершить')
            self.continue_loop_btn_4.clicked.connect(self.open_str_btn)
            self.frame_console_15.show()
            self.progress_loop_4.setValue(100)
        else:
            self.miss()
            if self.count_heart == 0:
                self.restart_loop()
            if not self.is_low_five_hp:
                self.is_low_five_hp = True
                self.update_hp_timer()

    def restart_loop(self):
        self.main_menu.setCurrentIndex(0)
        self.answer_edit_loop_4.clear()
        self.answer_edit_loop_4.resize(31, 21)
        self.answer_edit_loop_2.clear()
        self.answer_edit_loop_2.resize(31, 21)
        self.continue_loop_btn_1.disconnect()
        self.continue_loop_btn_2.disconnect()
        self.continue_loop_btn_3.disconnect()
        self.continue_loop_btn_4.disconnect()
        self.continue_loop_btn_1.setText('Проверить')
        self.continue_loop_btn_1.clicked.connect(self.check_answer_loop_1)
        self.frame_console_10.hide()
        self.frame_console_15.hide()
        self.frame_console_20.hide()
        self.continue_loop_btn_2.setText('Проверить')
        self.continue_loop_btn_2.clicked.connect(self.check_answer_loop_2)
        self.continue_loop_btn_3.setText('Проверить')
        self.continue_loop_btn_3.clicked.connect(self.check_answer_loop_3)
        self.continue_loop_btn_4.setText('Проверить')
        self.continue_loop_btn_4.clicked.connect(self.check_answer_loop_4)
        self.frame_console_14.hide()
        self.progress_loop_1.setValue(0)
        self.progress_loop_2.setValue(0)
        self.progress_loop_3.setValue(0)
        self.progress_loop_4.setValue(0)

    def open_cond_btn(self):
        self.progress_num_6.setValue(0)
        self.cond_btn.setEnabled(True)
        self.cond_btn.setStyleSheet('''color: white;
                background: rgb(64,66,115);
                border-radius: 5px; font-weight:
                bold; font-size: 16px;
                ''')
        if self.progress_basics_part1.value() < 50:
            self.progress_basics_part1.setValue(50)
        self.restart_num()
        self.enable_task('cond_btn')

    def open_num_btn(self):
        self.progress_createvar_3.setValue(0)
        self.num_btn.setEnabled(True)
        self.num_btn.setStyleSheet('''color: white;
        background: rgb(64,66,115);
        border-radius: 5px; font-weight:
        bold; font-size: 16px;
        ''')
        if self.progress_basics_part1.value() < 25:
            self.progress_basics_part1.setValue(25)
        self.restart_createvar()
        self.enable_task('num_btn')

    def open_loop_btn(self):
        self.progress_cond_5.setValue(0)
        self.loop_btn.setEnabled(True)
        self.loop_btn.setStyleSheet('''color: white;
        background: rgb(64,66,115);
        border-radius: 5px; font-weight:
        bold; font-size: 16px;
        ''')
        if self.progress_basics_part1.value() < 75:
            self.progress_basics_part1.setValue(75)
        self.restart_cond()
        self.enable_task('loop_btn')

    def open_str_btn(self):
        self.progress_loop_4.setValue(0)
        self.str_btn.setEnabled(True)
        self.str_btn.setStyleSheet('''color: white;
                background: rgb(64,66,115);
                border-radius: 5px; font-weight:
                bold; font-size: 16px;
                ''')
        if self.progress_basics_part1.value() < 100:
            self.progress_basics_part1.setValue(100)
        self.restart_loop()
        self.enable_task('cond_btn')

    def enable_task(self, task):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute(f'''
                            UPDATE users SET {task} = 1 WHERE id = ?
                        ''', [self.id])
        conn.commit()
        conn.close()

    def miss(self):
        self.count_heart -= 1
        self.errors += 1
        self.update_data()

    def run_code(self):
        code = self.text_edit.toPlainText()
        result = PythonExecutor.execute(code)
        self.output_edit.setPlainText(result)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Python Files (*.py);;All Files (*)")

        if file_name:
            # Читаем содержимое файла и устанавливаем его в text_edit
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setPlainText(content)

    def save_file(self):
        # Диалоговое окно для выбора места сохранения файла
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
                                                   "Python Files (*.py);;Text Files (*.txt);;All Files (*)")

        if file_name:
            # Сохраняем содержимое text_edit в выбранный файл
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def exit_btn_pressed(self):
        reply = QMessageBox.information(self, 'Подтверждение', 'Вы уверены, что хотите выйти?',
                                        QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.restart_createvar()
            self.restart_num()
            self.restart_cond()

    # Обновляем количество жизней, монет, ошибок, опыта
    def update_data(self, db_update=True):
        self.hp_btn.setText(f'💖 {self.count_heart}')
        self.hp_text.setText(' 💖' * self.count_heart)
        self.hp_text.adjustSize()
        self.coins_btn.setText(f'💰 {self.coins}')
        self.xp_count.setText(f'{self.xp} xp')
        self.errors_count.setText(f'{self.errors} miss')
        if db_update:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute(f'''
                                        UPDATE users SET heart = ?, coins = ?, xp = ?, errors = ? WHERE id = ?
                                    ''', [self.count_heart, self.coins, self.xp, self.errors, self.id])
            conn.commit()
            conn.close()

    # Проверяем не равно ли значение жизней нулю
    def check_hp(self):
        return bool(self.count_heart)

    # def update_hp(self):
    #     last_time_str = None
    #     try:
    #         with open('last_update_time.json', 'r') as file:
    #             last_time_str = json.load(file)['last_update_time']
    #     except FileNotFoundError:
    #         self.update_time()
    #     if last_time_str is not None:
    #         if isinstance(last_time_str, (float, int)):
    #             last_time = datetime.fromtimestamp(last_time_str)
    #         else:
    #             last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S.%f')
    #
    #         time_difference = datetime.now() - last_time
    #         elapsed_minutes = time_difference.total_seconds() / 60
    #
    #         if elapsed_minutes + self.count_heart > 5:
    #             self.count_heart = 5
    #         else:
    #             self.count_heart += elapsed_minutes
    #         self.update_time()
    #
    #         # Обновление времени
    #         new_time = datetime.now()
    #         data = {'last_update_time': new_time.timestamp()}
    #         with open('last_update_time.json', 'w') as file:
    #             json.dump(data, file, indent=2)

    # def update_time(self):
    #     data = {'last_update_time': datetime.now().timestamp()}
    #     with open('last_update_time.json', 'w') as file:
    #         json.dump(data, file, indent=2)

    def start_progress_bar(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.increase_progress_bar)
        self.timer.start(2)

    def increase_progress_bar(self):
        if self.name_object is not None:
            value = self.name_object.value()
            if value < 100:
                self.name_object.setValue(value + 5)
            else:
                self.name_object = None
                self.timer.stop()
        else:
            pass

    def update_hp_timer(self):
        self.timer_hp = QTimer(self)
        self.timer_hp.singleShot(1000, self.update_count_hp)

    def update_count_hp(self):
        if self.count_heart < 5:
            self.count_heart += 1
            self.update_data()
            self.update_hp_timer()

    def registration(self):
        form = RegistrationForm(self)
        form.exec_()

    def enter(self):
        form = EnterForm(self)
        form.exec_()

    def set_data(self):
        self.profile_menu.setCurrentIndex(1)
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        res = cur.execute('''
            SELECT * FROM users WHERE id = ?
        ''', [self.id]).fetchall()
        self.name.setText(res[0][1])
        self.surname.setText(res[0][2])
        self.xp_count.setText(str(res[0][7]) + 'xp')
        self.errors_count.setText(str(res[0][8]))
        self.count_heart = res[0][5]
        if self.count_heart < 5:
            self.update_hp_timer()
        self.coins = res[0][6]
        self.xp = res[0][7]
        self.errors = res[0][8]
        self.restart_createvar()
        if bool(res[0][9]):
            self.open_num_btn()
        if bool(res[0][10]):
            self.open_cond_btn()
        if bool(res[0][11]):
            self.open_loop_btn()

    def exit_account(self):
        conn = sqlite3.connect('data.db')
        cur = conn.cursor()
        cur.execute('''
                    UPDATE last_enter SET id = 0
                ''')
        conn.commit()
        conn.close()
        self.profile_menu.setCurrentIndex(0)
        self.num_btn.setEnabled(False)
        self.num_btn.setStyleSheet('''
                color: white;
                background: rgb(49, 51, 88);
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
        ''')
        self.cond_btn.setStyleSheet('''
                color: white;
                background: rgb(49, 51, 88);
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
                ''')
        self.loop_btn.setStyleSheet('''
                        color: white;
                        background: rgb(49, 51, 88);
                        border-radius: 5px;
                        font-weight: bold;
                        font-size: 16px;
                        ''')
        self.progress_basics_part1.setValue(0)
        self.progress_basics_part2.setValue(0)
        self.progress_basics_part3.setValue(0)
        self.count_heart = 5
        self.xp = 0
        self.coins = 0
        self.errors = 0
        self.update_data(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
