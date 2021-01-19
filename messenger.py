from datetime import datetime
import requests
from PyQt5 import QtWidgets, QtCore
import clientui
import os
import PySide2

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class Messenger(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        # to run on button click:
        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        # to run by timer:
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def get_messages(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.after}
            )
        except:
            return

        messages = response.json()['messages']

        for message in messages:
            self.print_message(message)
            self.after = message['time']

    def print_message(self, message):
        message_time = datetime.fromtimestamp(message['time'])
        message_time = message_time.strftime('%Y/%m/%d %H:%M:%S')
        self.textBrowser.append(message_time + ' ' + message['name'])
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(
                'http://127.0.0.1:5000//send',
                json={'name': name, 'text': text}
            )
        except:
            self.textBrowser.append('Сервер недоступен. Попробуйте позднее')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('При отправке произошла ошибка')
            self.textBrowser.append('Проверьте имя и текст сообщения')
            self.textBrowser.append('')
            return

        self.textEdit.setText('')


app = QtWidgets.QApplication([])
window = Messenger()
window.show()
app.exec()
