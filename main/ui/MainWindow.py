import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QGridLayout, QWidget, qApp, QAction, QGroupBox, \
    QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, \
    QTextEdit

from main.aho_korasick.search import AhoKorasickSearch
from main.aho_korasick_wildcard.wildcard_search import AhoKorasickWildcard
from main.bitap_search.pattern import Pattern
from main.utils.enzymes_reader import EnzymesReader


# Наследуемся от QMainWindow
from main.utils.search_results_helper import TransformationHelper


class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    IMAGES_PATH = 'resources/static/images/'

    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        super().__init__()
        self.tabs = QTabWidget()
        self.seq_line_edit = QTextEdit()
        self.table_widget = QTableWidget()
        self.enzymes_reader = EnzymesReader()
        self.search_engine = AhoKorasickSearch(self.enzymes_reader.get_sib_simple_patterns(),
                                               self.enzymes_reader.get_neb_simple_pattens())
        self.search_engine_wildcard = AhoKorasickWildcard(self.enzymes_reader.get_syb_wildcard_patterns(),
                                                          self.enzymes_reader.get_neb_wildcard_patterns())
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(QSize(480, 320))  # Устанавливаем размеры
        self.setWindowTitle("Mutagenesis primer designer")  # Устанавливаем заголовок окна
        self.setWindowIcon(QIcon(self.IMAGES_PATH + 'main.png'))
        self.statusBar().showMessage('Ready to start work')
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        self.init_menu()
        self.create_tool_bar()

        main_layout = QHBoxLayout(self)
        central_widget.setLayout(main_layout)

        # self.tabs = QTabWidget()
        tab_neb = QWidget()
        tab_sib = QWidget()
        # Add tabs
        self.tabs.addTab(tab_neb, "NEB")
        self.tabs.addTab(tab_sib, "SibEnzymes")

        # Create first, second tab
        # TODO: use getters
        self.create_enzymes_list(tab_neb, self.enzymes_reader.get_sib_enzymes_data())
        self.create_enzymes_list(tab_sib, self.enzymes_reader.get_neb_enzymes_data())
        # Add tabs to widget
        main_layout.addWidget(self.tabs, 1)

        # Create font
        font_9_pt = QtGui.QFont()
        font_9_pt.setPointSizeF(9)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        seq_group_box = QGroupBox("Enter a sequence:")
        seq_group_box.setFont(font_9_pt)
        seq_layout = QHBoxLayout()
        #self.seq_line_edit = QTextEdit()
        seq_layout.addWidget(self.seq_line_edit)
        # seq_grid_layout = QGridLayout()
        # seq_grid_layout.setSpacing(10)
        # seq_label = QLabel("Enter a sequence:")
        # #seq_line_edit = QLineEdit()
        # seq_line_edit = QTextEdit()
        # seq_search_button = QPushButton("Search")
        # primer_label = QLabel("Primer:")
        # # primer_label.setFont(font_11_pt)
        # primer_label_1 = QLabel("")
        # build_primer_button = QPushButton("Build Primer")
        # seq_grid_layout.addWidget(seq_label, 0, 0)
        # seq_grid_layout.addWidget(seq_line_edit, 0, 1, 2, 1)
        # seq_grid_layout.addWidget(seq_search_button, 0, 2)
        # seq_grid_layout.addWidget(primer_label, 2, 0)
        # seq_grid_layout.addWidget(primer_label_1, 1, 1)
        # seq_grid_layout.addWidget(build_primer_button, 1, 2)
        # seq_group_box.setLayout(seq_grid_layout)

        seq_group_box.setLayout(seq_layout)
        right_layout.addWidget(seq_group_box, 1)

        # Create table
        # self.table_widget = QTableWidget()
        # self.table_widget.setRowCount(4)
        # self.table_widget.setColumnCount(2)
        # self.table_widget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        # self.table_widget.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
        # self.table_widget.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
        # self.table_widget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
        # self.table_widget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
        # self.table_widget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
        # self.table_widget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
        # self.table_widget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))

        right_layout.addWidget(self.table_widget, 4)

        right_widget.setLayout(right_layout)

        main_layout.addWidget(right_widget, 3)

    def init_menu(self):
        # Создаём Action с помощью которого будем выходить из приложения
        exit_action = QAction(QIcon(self.IMAGES_PATH + 'exit.png'), "&Exit", self)
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
        refresh_sibenzym_action = QAction(QIcon(self.IMAGES_PATH + 'refresh_se.png'), "&Refresh SibEnzym", self)
        tools_menu.addAction(refresh_sibenzym_action)
        help_menu = menu_bar.addMenu('&Help')
        about_action = QAction("&About", self)
        help_menu.addAction(about_action)

    def create_tool_bar(self):
        toolbar = self.addToolBar('ToolBar')
        search_action = QAction(QIcon(self.IMAGES_PATH + 'search.png'), "&Search for enzymes", self)
        search_action.triggered.connect(self.on_search_btn_clicked)
        build_primers_action = QAction(QIcon(self.IMAGES_PATH + 'build.png'), "&Build Primers", self)
        build_primers_action.triggered.connect(self.on_build_primers_btn_clicked)
        toolbar.addAction(search_action)
        toolbar.addAction(build_primers_action)

    def create_enzymes_list(self, tab, enzymes_data):
        # enzymes_list = QListWidget()
        # enzymes_list.addItems(enzymes_data)
        # tab.layout = QVBoxLayout()
        # tab.layout.addWidget(enzymes_list)
        # tab.setLayout(tab.layout)
        header_labels = ['Name', 'Top site', 'Bottom site']
        enzymes_table = QTableWidget(len(enzymes_data), 3)
        enzymes_table.setHorizontalHeaderLabels(header_labels)
        horizontal_header = enzymes_table.horizontalHeader()
        horizontal_header.setStretchLastSection(True)
        for enzyme_row in enzymes_data:
            index = enzymes_data.index(enzyme_row)
            enzymes_table.setItem(index, 0, QTableWidgetItem(enzyme_row.e_name))
            enzymes_table.setItem(index, 1, QTableWidgetItem(enzyme_row.top_site))
            enzymes_table.setItem(index, 2, QTableWidgetItem(enzyme_row.bottom_site))
        tab.layout = QVBoxLayout()
        tab.layout.addWidget(enzymes_table)
        tab.setLayout(tab.layout)

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

    def on_search_btn_clicked(self):
        # search_btn = self.sender()
        self.statusBar().showMessage("Search for enzymes")
        sequence_text = self.seq_line_edit.toPlainText().replace(" ", "").replace('\n', '')
        current_tab = self.tabs.currentIndex()
        # TODO: create the same for NEB tab
        # TODO: parallel processing for usual patterns and wildcard ones
        if current_tab == 1:  # SibTab
            search_results = self.search_engine.sib_traverse(sequence_text)
            search_results_wildcard = self.search_engine_wildcard.do_sib_search(sequence_text)
        if current_tab == 0:  # NebTab
            search_results = self.search_engine.neb_traverse(sequence_text)
            search_results_wildcard = self.search_engine_wildcard.do_neb_search(sequence_text)
        results_for_table = TransformationHelper.transform_results(search_results, search_results_wildcard)
        self.show_search_results_table(results_for_table)

    def on_build_primers_btn_clicked(self):
        self.statusBar().showMessage("Build primers")
        sequence_text = self.seq_line_edit.toPlainText().replace(" ", "").replace('\n', '')
        current_tab = self.tabs.currentIndex()
        if current_tab == 1:  # SibTab
            pass

    def show_search_results_table(self, search_results):
        header_labels = ['Name', 'Sequence', 'Site Length', 'Frequency', 'Cut Positions']
        self.table_widget.setRowCount(len(search_results))
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(header_labels)
        horizontal_header = self.table_widget.horizontalHeader()
        horizontal_header.setStretchLastSection(True)
        for site_item in search_results:
            index = search_results.index(site_item)
            self.table_widget.setItem(index, 0, QTableWidgetItem(str(site_item.get_site_names())))
            self.table_widget.setItem(index, 1, QTableWidgetItem(site_item.get_site_sequence()))
            self.table_widget.setItem(index, 2, QTableWidgetItem(str(site_item.get_site_length())))
            self.table_widget.setItem(index, 3, QTableWidgetItem(str(site_item.get_frequency())))
            self.table_widget.setItem(index, 4, QTableWidgetItem(str(site_item.get_cut_positions())))

if __name__ == "__main__":
    import sys

app = QtWidgets.QApplication(sys.argv)
mw = MainWindow()
mw.showMaximized()  # show()
sys.exit(app.exec())
