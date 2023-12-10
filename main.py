import contextlib
import sys
import sqlite3
import asyncio
from datetime import datetime
import json
from io import StringIO

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, qApp


# from dialogs import FirstMiss, InfoPEP8, Congratulation


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
        self.name_object = None
        self.first_miss = False
        self.count_heart = 5
        self.mistakes = 0
        self.xp = 0
        self.coins = 0
        self.cur_num_main_window = 0
        super().__init__()
        uic.loadUi('project.ui', self)
        self.initUI()

    def initUI(self):
        self.update_hp()
        self.update_data()
        self.createvar_btn.clicked.connect(self.choose_themes)
        self.continue_createvar_btn_1.clicked.connect(self.next_page_createvar)
        self.continue_createvar_btn_2.clicked.connect(self.next_page_createvar)
        self.continue_createvar_btn_3.clicked.connect(self.next_page_createvar)
        self.continue_createvar_btn_4.clicked.connect(self.check_answer_createvar_1)
        self.answer_edit_1.textChanged.connect(self.change_size)
        self.frame_console_1.hide()
        self.continue_createvar_btn_5.clicked.connect(self.check_answer_createvar_2)
        self.frame_console_2.hide()
        self.continue_createvar_btn_6.clicked.connect(self.check_answer_createvar_3)

        # self.res_createvar_2.textChanged.connect(self.change_size)
        # self.res_createvar_3.textChanged.connect(self.change_size)
        # self.res_createvar_4.textChanged.connect(self.change_size)
        # self.res_createvar_5.textChanged.connect(self.change_size)
        # self.res_createvar_6.textChanged.connect(self.change_size)
        # self.res_createvar_9.textChanged.connect(self.change_size)
        # self.res_createvar_11.textChanged.connect(self.change_size)
        # self.check_createvar_2.clicked.connect(self.check_answer_createvar_2)
        # self.check_createvar_3.clicked.connect(self.check_answer_createvar_3)
        # self.check_createvar_4.clicked.connect(self.check_answer_createvar_4)
        # self.check_createvar_5.clicked.connect(self.check_answer_createvar_5)
        # self.check_createvar_6.clicked.connect(self.check_answer_createvar_6)
        # self.check_createvar_7.clicked.connect(self.check_answer_createvar_7)
        # self.frame_19.setHidden(True)
        # self.frame_22.setHidden(True)
        # self.frame_28.setHidden(True)
        # self.info_pep8.clicked.connect(self.get_info_pep8)
        self.run_btn.clicked.connect(self.run_code)
        self.open_btn.clicked.connect(self.open_file)
        self.save_btn.clicked.connect(self.save_file)
        self.exit_btn.clicked.connect(self.exit_btn_pressed)

    def choose_themes(self):
        text = self.sender().text()
        if self.check_hp():
            if text == 'Создание переменных':
                self.main_menu.setCurrentIndex(1)
                self.themes.setCurrentIndex(0)
                self.tasks_createvar.setCurrentIndex(0)
                self.cur_num_main_window = 0
        else:
            pass
            # TODO: добавить окно которое говорит о том что надо подождать

    def next_page_createvar(self):
        self.tasks_createvar.setCurrentIndex(self.tasks_createvar.currentIndex() + 1)
        # self.progress_tasks.setValue(self.progress_createvar_1.value() + 12)

    def main_window(self):
        self.main_windows.setCurrentIndex(0)

    def change_size(self):
        res = self.sender()
        text_width = QFontMetrics(res.font()).width(res.text())
        new_width = text_width + 10
        res.setFixedWidth(new_width)

    def check_answer_createvar_1(self):
        if self.answer_edit_1.text() == 'car = "Porsche"' or self.answer_edit_1.text() == "car = 'Porsche'":
            self.continue_createvar_btn_4.setText('Продолжить')
            self.continue_createvar_btn_4.clicked.connect(self.next_page_createvar)
            self.name_object = self.progress_createvar_1
            self.start_progress_bar()
        else:
            self.check_first_miss()
            self.count_heart -= 1
            self.mistakes += 1
            self.update_data()
            if self.count_heart == 0:
                self.end_createvar(False)
            self.update_hp_timer()

    def check_answer_createvar_2(self):
        self.continue_createvar_btn_5.setText('Продолжить')
        self.continue_createvar_btn_5.clicked.connect(self.next_page_createvar)
        self.frame_console_1.show()
        self.name_object = self.progress_createvar_2
        self.start_progress_bar()

    def check_answer_createvar_3(self):
        if self.answer_edit_4.toPlainText() == 'name = "Hello, Qt!"\nprint(name)' \
                or self.answer_edit_4.toPlainText() == "name = 'Hello, Qt!'\nprint(name)":
            self.continue_createvar_btn_6.setText('Завершить')
            self.continue_createvar_btn_6.clicked.connect(self.open_num_btn)
            self.frame_console_2.show()
            self.progress_createvar_3.setValue(100)
        else:
            self.check_first_miss()
            self.count_heart -= 1
            self.mistakes += 1
            self.update_data()
            if self.count_heart == 0:
                self.end_createvar()
            self.update_hp_timer()

    def end_createvar(self):
        self.main_menu.setCurrentIndex(0)
        self.tasks_createvar.setCurrentIndex(0)
        self.continue_createvar_btn_6.disconnect()
        self.answer_edit_1.clear()
        self.answer_edit_1.resize(21, 31)
        self.answer_edit_4.clear()
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

    def open_num_btn(self):
        self.progress_createvar_3.setValue(0)
        self.num_btn.setEnabled(True)
        self.num_btn.setStyleSheet('''color: white;
        background: rgb(64,66,115);
        border-radius: 5px; font-weight:
        bold; font-size: 16px;
        ''')
        self.progress_basics_part1.setValue(25)
        self.end_createvar()

    def check_first_miss(self):
        #     if not self.first_miss:
        #         self.first_miss = True
        #         self.dialog = FirstMiss(self)
        #         self.dialog.exec_()
        #
        # def get_info_pep8(self):
        #     self.dialog = InfoPEP8(self)
        #     self.dialog.exec_()
        pass

    def run_code(self):
        code = self.text_edit.toPlainText()
        result = PythonExecutor.execute(code)
        self.output_edit.setPlainText(result)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Python Files (*.py);;All Files (*)")

        if file_name:
            # Читаем содержимое файла и устанавливаем его в QPlainTextEdit
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_edit.setPlainText(content)

    def save_file(self):
        # Диалоговое окно для выбора места сохранения файла
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "",
                                                   "Python Files (*.py);;Text Files (*.txt);;All Files (*)")

        if file_name:
            # Сохраняем содержимое QPlainTextEdit в выбранный файл
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())

    def exit_btn_pressed(self):
        reply = QMessageBox.information(self, 'Подтверждение', 'Вы уверены, что хотите выйти?',
                                        QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.end_createvar()

    # def exit(self):
    #     congratulation = Congratulation()
    #     congratulation.exec_()
    #     self.main_window()
    #     self.xp += 100
    #     self.coins += 10
    #     self.update_data()

    def update_data(self):
        self.hp_btn.setText(f'💖 {self.count_heart}')
        self.hp_text.setText(' 💖' * self.count_heart)
        self.hp_text.adjustSize()

    def check_hp(self):
        return bool(self.count_heart)

    def update_hp(self):
        last_time_str = None
        try:
            with open('last_update_time.json', 'r') as file:
                last_time_str = json.load(file)['last_update_time']
        except FileNotFoundError:
            self.update_time()
        if last_time_str is not None:
            if isinstance(last_time_str, (float, int)):
                last_time = datetime.fromtimestamp(last_time_str)
            else:
                last_time = datetime.strptime(last_time_str, '%Y-%m-%d %H:%M:%S.%f')

            time_difference = datetime.now() - last_time
            elapsed_minutes = time_difference.total_seconds() / 60

            if elapsed_minutes + self.count_heart > 5:
                self.count_heart = 5
            else:
                self.count_heart += elapsed_minutes
            self.update_time()

            # Update the last update time
            new_time = datetime.now()
            data = {'last_update_time': new_time.timestamp()}
            with open('last_update_time.json', 'w') as file:
                json.dump(data, file, indent=2)

    def update_time(self):
        data = {'last_update_time': datetime.now().timestamp()}
        with open('last_update_time.json', 'w') as file:
            json.dump(data, file, indent=2)

    def start_progress_bar(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.increase_progress_bar)
        self.timer.start(10)

    def increase_progress_bar(self):
        value = self.name_object.value()
        if value <= 100:
            self.name_object.setValue(value + 5)
        else:
            self.timer.stop()
            self.timer.deleteLater()

    def update_hp_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_count_hp)
        self.timer.start(600000)

    def update_count_hp(self):
        self.count_heart += 1
        if self.count_heart != 5:
            self.update_hp_timer()
        else:
            self.timer.deleteLater()
        self.update_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())

# car = "Porsche"
name = "Hello, Qt!"
print(name)
