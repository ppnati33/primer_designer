import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QLabel, QGridLayout, QWidget, qApp, QAction, QGroupBox, \
    QHBoxLayout, QVBoxLayout, QListWidget, QLineEdit, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, \
    QTextEdit
from PyQt5.QtWidgets import QSpinBox

from main.aho_korasick.search import AhoKorasickSearch
from main.aho_korasick_wildcard.wildcard_search import AhoKorasickWildcard
# from main.bitap_search.pattern import Pattern
from main.bitap_search.custom_bitap import CustomBitapSearch
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
        self.mutationPosition = QSpinBox(self)
        self.enzymes_reader = EnzymesReader()
        self.search_engine = AhoKorasickSearch(self.enzymes_reader.get_sib_simple_patterns(),
                                               self.enzymes_reader.get_neb_simple_pattens())
        self.search_engine_wildcard = AhoKorasickWildcard(self.enzymes_reader.get_sib_wildcard_patterns(),
                                                          self.enzymes_reader.get_neb_wildcard_patterns())
        # p1 = Pattern('GAA', ['name1', 'name11'])
        # p2 = Pattern('NCCT', ['name2'])
        # p3 = Pattern('TAAG', ['name3'])
        # p4 = Pattern('GTG', ['name4'])
        # pats = [p1, p2, p3, p4]
        self.build_primers_engine = CustomBitapSearch(self.enzymes_reader.get_all_sib_patterns(), 2)
        self.build_primers_engine_neb = CustomBitapSearch(self.enzymes_reader.get_all_neb_patterns(), 2)
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
        self.create_enzymes_list(tab_neb, self.enzymes_reader.get_neb_enzymes_data())
        self.create_enzymes_list(tab_sib, self.enzymes_reader.get_sib_enzymes_data())
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
        self.seq_line_edit.cursorPositionChanged.connect(self.cursor_position)
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

        cutAction = QAction(QtGui.QIcon(self.IMAGES_PATH + 'cut.png'), "Cut to clipboard", self)
        cutAction.setStatusTip("Delete and copy text to clipboard")
        cutAction.setShortcut("Ctrl+X")
        cutAction.triggered.connect(self.seq_line_edit.cut)

        copyAction = QAction(QtGui.QIcon(self.IMAGES_PATH + "copy.png"), "Copy to clipboard", self)
        copyAction.setStatusTip("Copy text to clipboard")
        copyAction.setShortcut("Ctrl+C")
        copyAction.triggered.connect(self.seq_line_edit.copy)

        pasteAction = QAction(QtGui.QIcon(self.IMAGES_PATH + "paste.png"), "Paste from clipboard", self)
        pasteAction.setStatusTip("Paste text from clipboard")
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.triggered.connect(self.seq_line_edit.paste)

        toolbar.addAction(cutAction)
        toolbar.addAction(copyAction)
        toolbar.addAction(pasteAction)
        toolbar.addSeparator()

        positionLabel = QLabel("Enter position: ", self)
        self.mutationPosition.setMinimum(0)
        self.mutationPosition.setMaximum(50000)
        self.mutationPosition.setValue(0)
        toolbar.addWidget(positionLabel)
        toolbar.addWidget(self.mutationPosition)

        search_action = QAction(QIcon(self.IMAGES_PATH + 'find.png'), "&Search for restriction sites", self)
        search_action.setStatusTip("Search for restriction sites")
        search_action.triggered.connect(self.on_search_btn_clicked)

        build_primers_action = QAction(QIcon(self.IMAGES_PATH + 'primers.png'), "&Build primers", self)
        build_primers_action.setStatusTip("Build primers")
        build_primers_action.triggered.connect(self.on_build_primers_btn_clicked)

        toolbar.addAction(search_action)
        toolbar.addAction(build_primers_action)
        #toolbar.addSeparator()

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
        self.statusBar().showMessage("Search for restriction sites")
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
        mpos_value = self.mutationPosition.value() - 1
        sequence_text = self.seq_line_edit.toPlainText().replace(" ", "").replace('\n', '')
        current_tab = self.tabs.currentIndex()
        if current_tab == 1:  # SibTab
            primers_results = self.build_primers_engine.bitap_search(sequence_text, mpos_value)
        # TODO: Neb tab
        if current_tab == 0:  # NebTab
            primers_results = self.build_primers_engine_neb.bitap_search(sequence_text, mpos_value)
        self.show_build_primers_results_table(primers_results)

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

    def show_build_primers_results_table(self, primers_results):
        header_labels = ['Site Names', 'Sequence', 'Site with mismatch', 'Site start position', 'Mismatch positions',
                         'Primer', 'Primer type']
        row_count = 0
        for site, mismatched_sites in primers_results.items():
            row_count += len(mismatched_sites)
        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(header_labels)
        index = -1
        for site, mismatched_sites in primers_results.items():
            # index = pr_results.index(site_item)
            row_count += len(mismatched_sites)
            for found_mismatched_site in mismatched_sites:
                index += 1
                self.table_widget.setItem(index, 0, QTableWidgetItem(str(site.get_names())))
                self.table_widget.setItem(index, 1, QTableWidgetItem(site.get_seq()))
                self.table_widget.setItem(index, 2, QTableWidgetItem(found_mismatched_site.get_enzyme_with_mismatch()))
                self.table_widget.setItem(index, 3, QTableWidgetItem(str(found_mismatched_site
                                                                         .get_start_pos() + 1)))
                self.table_widget.setItem(index, 4, QTableWidgetItem(str([pos + 1 for pos in found_mismatched_site
                                                                         .get_mismatch_positions()])))
                primer = found_mismatched_site.get_primer()
                self.table_widget.setItem(index, 5, QTableWidgetItem(primer.get_primer_sequence()))
                primer_type = ("Forward" if primer.get_is_forward() else "Reverse")
                self.table_widget.setItem(index, 6, QTableWidgetItem(primer_type))
        self.table_widget.resizeRowsToContents()
        self.table_widget.resizeColumnsToContents()
        horizontal_header = self.table_widget.horizontalHeader()
        horizontal_header.setStretchLastSection(True)

    def cursor_position(self):
        cursor_pos = self.seq_line_edit.textCursor().position()
        seq = self.seq_line_edit.toPlainText()
        seq_part = seq[:cursor_pos].replace(" ", "").replace('\n', '')
        pos = len(seq_part)
        # Mortals like 1-indexed things
        # line = cursor.blockNumber() + 1
        # col = cursor.columnNumber()
        self.statusBar().showMessage("Cursor position: {}".format(pos))


if __name__ == "__main__":
    import sys

app = QtWidgets.QApplication(sys.argv)
mw = MainWindow()
mw.showMaximized()  # show()
sys.exit(app.exec())
