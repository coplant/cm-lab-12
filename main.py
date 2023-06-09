from enum import Enum
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from ui_mainwindow import Ui_MainWindow


class Application(QMainWindow):
    class Action(Enum):
        ENCRYPT = -1
        DECRYPT = 1

    class Language(Enum):
        RUSSIAN = 0
        ENGLISH = 1

    def __init__(self):
        super(Application, self).__init__()
        self.data = None
        self.key = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.btn_enc.setChecked(True)
        self.abc = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        # self.abc = "abcdefghijklmnopqrstuvwxyz"

        self.ui.proc_button.clicked.connect(self.process_data)
        self.ui.open_file.triggered.connect(self.open)
        self.ui.save_file.triggered.connect(self.save)

    def process_data(self):
        self.data = self.ui.plain_text.toPlainText()
        self.key = self.ui.line_key.text()
        if len(self.data) != len(self.key):
            return QMessageBox.information(self, "Ошибка", "Длина ключа должна совпадать с длиной сообщения",
                                           QMessageBox.Ok)
        try:
            if self.ui.btn_enc.isChecked():
                self.data = self.crypt_text(self.Action.ENCRYPT.value)
            elif self.ui.btn_dec.isChecked():
                self.data = self.crypt_text(self.Action.DECRYPT.value)

        except ValueError as e:
            ...
        self.ui.cipher_text.setText(str(self.data))

    def crypt_text(self, choice):
        text = ""
        result = []
        for i in range(len(self.data)):
            text_letter = self.abc.find(self.data[i].lower())
            key_letter = self.abc.find(self.key[i].lower())
            result.append(((text_letter - choice * key_letter) + len(self.abc)) % len(self.abc))
        for i in range(len(self.data)):
            if self.data[i].lower() in self.abc:
                text += self.abc[result[i]]
            else:
                text += self.data[i]
        return text

        # todo method 2 - xor посимвольно
        # text = bytearray(self.data)
        # key = bytearray(self.key)
        # result = bytearray()
        # for i in range(len(text)):
        #     result.append(text[i] ^ key[i])
        # return result.decode("ansi")

    def open(self):
        file_name = QFileDialog.getOpenFileName(self, "Открыть файл", ".", "All Files (*)")
        if file_name[0]:
            with open(file_name[0], "r") as file:
                self.data = file.read()
                self.ui.plain_text.setText(self.data)
        else:
            QMessageBox.information(self, "Ошибка", "Файл не выбран", QMessageBox.Ok)

    def save(self):
        file_name = QFileDialog.getSaveFileName(self, "Сохранить файл", ".", "All Files (*)")
        if file_name[0]:
            with open(file_name[0], "w") as file:
                file.write(self.ui.cipher_text.toPlainText())
        else:
            QMessageBox.information(self, "Ошибка", "Файл не выбран", QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication()
    window = Application()
    app.exec()
