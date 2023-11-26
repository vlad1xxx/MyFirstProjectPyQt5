import contextlib
import sys
import sqlite3
import asyncio
from datetime import datetime
import json
from io import StringIO

from PyQt5 import uic
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
        self.createvar_btn.clicked.connect(self.choose_theme)
        # self.continue_createvar.clicked.connect(self.next_page_createvar)
        # self.continue_createvar_2.clicked.connect(self.next_page_createvar)
        # self.check_createvar_1.clicked.connect(self.check_answer_createvar_1)
        # self.res_createvar_1.textChanged.connect(self.change_size)
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
        # self.exit_btn.clicked.connect(self.exit_btn_pressed)

    # def choose_theme(self):
    #     text = self.sender().text()
    #     if self.check_hp():
    #         if text == 'Создание переменных':
    #             self.main_windows.setCurrentIndex(1)
    #             self.page_task.setCurrentIndex(0)
    #             self.cur_num_main_window = 0
    #     else:
    #         pass
    #         # TODO: добавить окно которое говорит о том что надо подождать
    #
    # def next_page_createvar(self):
    #     self.page_task.setCurrentIndex(self.page_task.currentIndex() + 1)
    #     # self.progress_tasks.setValue(self.progress_createvar_1.value() + 12)
    #
    # def main_window(self):
    #     self.main_windows.setCurrentIndex(0)
    #
    # def change_size(self):
    #     res = self.sender()
    #     text_width = QFontMetrics(res.font()).width(res.text())
    #     new_width = text_width + 10
    #     res.setFixedWidth(new_width)
    #
    # def check_answer_createvar_1(self):
    #     if self.res_createvar_1.text() == 'city':
    #         self.check_createvar_1.setText('Продолжить')
    #         self.check_createvar_1.clicked.connect(self.next_page_createvar)
    #     else:
    #         self.check_first_miss()
    #         self.count_heart -= 1
    #         self.mistakes += 1
    #         self.update_data()
    #
    # def check_answer_createvar_2(self):
    #     if self.res_createvar_2.text() == '"Porsche"':
    #         self.check_createvar_2.setText('Продолжить')
    #         self.check_createvar_2.clicked.connect(self.next_page_createvar)
    #     else:
    #         self.check_first_miss()
    #         self.count_heart -= 1
    #         self.mistakes += 1
    #         self.update_data()
    #
    # def check_answer_createvar_3(self):
    #     if self.res_createvar_3.text() == '=':
    #         self.check_createvar_3.setText('Продолжить')
    #         self.check_createvar_3.clicked.connect(self.next_page_createvar)
    #     else:
    #         self.check_first_miss()
    #         self.count_heart -= 1
    #         self.mistakes += 1
    #         self.update_data()
    #
    # def check_answer_createvar_4(self):
    #     if (self.res_createvar_4.text() == 'step_1 = "step"' and self.res_createvar_5.text() == 'step_2 = "by"'
    #             and self.res_createvar_6.text() == 'step_3 = "step"'):
    #         self.check_createvar_4.setText('Продолжить')
    #         self.check_createvar_4.clicked.connect(self.next_page_createvar)
    #     else:
    #         self.check_first_miss()
    #         self.count_heart -= 1
    #         self.mistakes += 1
    #         self.update_data()
    #
    # def check_answer_createvar_5(self):
    #     self.check_createvar_5.setText('Продолжить')
    #     self.check_createvar_5.clicked.connect(self.next_page_createvar)
    #     self.frame_19.setHidden(False)
    #     self.correct_answer()
    #
    # def check_answer_createvar_6(self):
    #     if self.res_createvar_9.text() == 'print("GO!")':
    #         self.check_createvar_6.setText('Продолжить')
    #         self.check_createvar_6.clicked.connect(self.next_page_createvar)
    #         self.frame_22.setHidden(False)
    #     else:
    #         self.check_first_miss()
    #         self.count_heart -= 1
    #         self.mistakes += 1
    #         self.update_data()
    #
    # def check_answer_createvar_7(self):
    #     if self.res_createvar_11.text() == 'print(greeting)':
    #         self.check_createvar_7.setText('Завершить')
    #         self.check_createvar_7.clicked.connect(self.exit)
    #         self.xp += 100
    #     else:
    #         self.check_first_miss()
    #         self.count_heart -= 1
    #         self.mistakes += 1
    #         self.update_data()

    # def check_first_miss(self):
    #     if not self.first_miss:
    #         self.first_miss = True
    #         self.dialog = FirstMiss(self)
    #         self.dialog.exec_()
    #
    # def get_info_pep8(self):
    #     self.dialog = InfoPEP8(self)
    #     self.dialog.exec_()

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
        qApp.setStyleSheet("QMessageBox QPushButton{color: white;}")
        reply = QMessageBox.information(self, 'Подтверждение', '<p style="color: white;"> Вы уверены, что хотит '
                                                               'выйти?</p>', QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.main_window()

    # def exit(self):
    #     congratulation = Congratulation()
    #     congratulation.exec_()
    #     self.main_window()
    #     self.xp += 100
    #     self.coins += 10
    #     self.update_data()
    #
    # def update_data(self):
    #     self.hp_btn.setText(f'💖 {self.count_heart}')
    #     self.hp_text.setText(' 💖' * self.count_heart)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())