import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QGridLayout, QWidget, qApp, QAction, QRadioButton, \
    QGroupBox, QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setMinimumSize(QSize(480, 320))  # Устанавливаем размеры
        self.setWindowTitle("Mutagenesis primer designer")  # Устанавливаем заголовок окна
        self.setWindowIcon(QIcon('main.png'))
        self.statusBar().showMessage('Ready to start work')
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout(self)  # Создаём QGridLayout
        grid_layout.setSpacing(10)
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        self.init_menu()

        enzymes_label = QLabel("Эндонуклеазы рестрикции", self)  # Создаём лейбл
        enzymes_label.setAlignment(QtCore.Qt.AlignCenter)  # Устанавливаем позиционирование текста
        grid_layout.addWidget(enzymes_label, 0, 0)  # и добавляем его в размещение

        enzymes_type_group_box = QGroupBox("Select Enzymes Type:")
        enzymes_button_layout = QHBoxLayout()
        radio_button = QRadioButton("Sib Enzymes")
        radio_button.setChecked(True)
        radio_button.e_type = "1"
        radio_button.toggled.connect(self.on_radio_button_toggled)
        enzymes_button_layout.addWidget(radio_button)
        radio_button = QRadioButton("Other Enzymes")
        radio_button.e_type = "2"
        radio_button.toggled.connect(self.on_radio_button_toggled)
        enzymes_button_layout.addWidget(radio_button)
        enzymes_type_group_box.setLayout(enzymes_button_layout)
        grid_layout.addWidget(enzymes_type_group_box, 1, 0)

        self.create_enzymes_list(grid_layout)

        sequence_label = QLabel("Nucleotide Sequence", self)  # Создаём лейбл
        sequence_label.setAlignment(QtCore.Qt.AlignCenter)  # Устанавливаем позиционирование текста
        grid_layout.addWidget(sequence_label, 0, 1)  # и добавляем его в размещение

        s_input_layout = QHBoxLayout()
        s_line_edit = QLineEdit()
        s_input_layout.addWidget(s_line_edit)
        s_input_button = QPushButton("Search")
        s_input_layout.addWidget(s_input_button)
        seq_input = QWidget()
        seq_input.setLayout(s_input_layout)
        grid_layout.addWidget(seq_input, 1, 1)

        primer_layout = QHBoxLayout()
        primer_label = QLabel("New Primer")
        primer_label.setAlignment(QtCore.Qt.AlignLeft)
        primer_layout.addWidget(primer_label)
        primer_seq_label = QLabel("Test")
        primer_seq_label.setAlignment(QtCore.Qt.AlignCenter)
        #primer_layout.addWidget(primer_seq_label)
        primer_button = QPushButton("Build Primer")
        primer_layout.addWidget(primer_button)
        #primer_widget = QWidget()
        #primer_widget.setLayout(primer_layout)
        #grid_layout.addWidget(primer_widget, 2, 1)
        grid_layout.addItem(primer_layout, 2, 1)

        # Search Results
        sr_layout = QVBoxLayout()
        sr_label = QLabel("Search Results", self)
        sr_label.setAlignment(QtCore.Qt.AlignCenter)
        grid_layout.addWidget(sr_label, 3, 1)


    def init_menu(self):
        # Создаём Action с помощью которого будем выходить из приложения
        exit_action = QAction(QIcon('exit.png'), "&Exit", self)
        exit_action.setShortcut('Ctrl+Q')  # Задаём для него хоткей
        exit_action.setStatusTip('Exit application')
        # Подключаем сигнал triggered к слоту quit у qApp.
        # синтаксис сигналов и слотов в PyQt5 заметно отличается от того,
        # который используется Qt5 C++
        exit_action.triggered.connect(qApp.quit)
        self.statusBar()
        # Устанавливаем в панель меню данный Action.
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)
        tools_menu = menu_bar.addMenu('&Tools')
        refresh_sibenzym_action = QAction(QIcon('refresh_se.png'), "&Refresh SibEnzym", self)
        tools_menu.addAction(refresh_sibenzym_action)
        help_menu = menu_bar.addMenu('&Help')
        about_action = QAction("&About", self)
        help_menu.addAction(about_action)

    def create_enzymes_list(self, grid_layout):
        # TODO: get data from enzymes_reader.py, in depends on selected enzyme's type
        data = [
            "GACGT↑C",
            "CC↑TCGAGG",
            "TGC↑GCA",
            "ACCTGC(N)4↑",
            "G↑GTACC",
            "G↑GYRCC",
            "CCANNNN↑NTGG",
            "GAG↑CGG",
            "AA↑CGTT",
            "GGATC(N)4↑",
            "Y↑GGCCR",
            "R↑AATTY",
            "CTGAAG(N)16↑",
            "AGC↑GCT",
            "TTS↑AA",
            "A↑CTAGT",
            "↑CCWGG",
            "AG↑CT",
            "AG↑CT",
            "C↑YCGRG"
        ]
        enzyms_list = QListWidget()
        enzyms_list.addItems(data)
        grid_layout.addWidget(enzyms_list, 2, 0, 2, 1)

    def create_sr_table(self, grid_layout):
        return

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def on_radio_button_toggled(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            # TODO:
            # self.statusBar().showMessage('Selected enzymes type is %s') % radiobutton.e_type
            print("test %s" % radiobutton.e_type)


if __name__ == "__main__":
    import sys

app = QtWidgets.QApplication(sys.argv)
mw = MainWindow()
mw.show()
sys.exit(app.exec())
