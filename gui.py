import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSlot, Qt, QRegExp
from PyQt5.QtGui import QColor, QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from evaluator import evaluate_in_range
from expr_parser.parser import Parser


class Canvas(FigureCanvas):
    def __init__(self, parent, x_values, y_values):
        fig, self.ax = plt.subplots(dpi=120)
        super().__init__(fig)
        self.setParent(parent)
        self.x_values = x_values
        self.y_values = y_values
        self.setGeometry(180, 50, 640, 500)
        self.show_plot()
        self.set_plot_border_black()

    def set_plot_border_black(self):
        self.ax.spines['bottom'].set_color('0.0')
        self.ax.spines['top'].set_color('0.0')
        self.ax.spines['right'].set_color('0.0')
        self.ax.spines['left'].set_color('0.0')

    def show_plot(self):
        self.ax.cla()
        self.ax.plot(self.x_values, self.y_values)
        self.ax.grid()
        self.figure.canvas.draw_idle()


class PlotterWidget(QWidget):
    def __init__(self, x_values, y_values):
        super().__init__()
        self.reset_button = QPushButton('Reset view', self)
        self.zoom_button = QPushButton('Zoom', self)
        self.pan_button = QPushButton('Pan', self)
        self.save_button = QPushButton('Save', self)
        self.min_label = QLabel(self)
        self.max_label = QLabel(self)
        self.min_box = QLineEdit(self)
        self.max_box = QLineEdit(self)
        self.f_of_x_label = QLabel(self)
        self.error_label = QLabel(self)
        self.expr_text_box = QLineEdit(self)
        self.plot_button = QPushButton('Plot', self)
        self.setFixedSize(1000, 750)
        self.canvas = Canvas(self, x_values, y_values)
        self.toolbar = NavigationToolbar(self.canvas, None, True)

        self.setWindowTitle('Plotter')
        self.init_ui()

    def init_pan_button(self):
        f = self.pan_button.font()
        f.setPointSize(12)
        self.pan_button.setFont(f)
        self.pan_button.setGeometry(830, 290, 85, 30)
        self.pan_button.clicked.connect(self.toolbar.pan)

    def init_save_button(self):
        f = self.save_button.font()
        f.setPointSize(12)
        self.save_button.setFont(f)
        self.save_button.setGeometry(830, 330, 85, 30)
        self.save_button.clicked.connect(self.toolbar.save_figure)

    def init_reset_button(self):
        f = self.reset_button.font()
        f.setPointSize(11)
        self.reset_button.setFont(f)
        self.reset_button.setGeometry(830, 250, 85, 30)
        self.reset_button.clicked.connect(self.toolbar.home)

    def init_zoom_button(self):
        f = self.zoom_button.font()
        f.setPointSize(12)
        self.zoom_button.setFont(f)
        self.zoom_button.setGeometry(830, 210, 85, 30)
        self.zoom_button.clicked.connect(self.toolbar.zoom)

    def init_ui(self):
        self.init_text_box()
        self.init_plot_button()
        self.init_error_label()
        self.init_f_of_x_label()
        self.init_background_color()
        self.init_min_box()
        self.init_max_box()
        self.init_reset_button()
        self.init_zoom_button()
        self.init_pan_button()
        self.init_save_button()

    def init_background_color(self):
        p = self.palette()
        color = QColor("#F5F5F5")
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def init_min_box(self):
        self.min_label.setText('min')
        self.min_label.setGeometry(200, 650, 100, 30)
        self.min_box.setGeometry(250, 650, 100, 30)
        self.min_box.setText('-1.0')
        f = self.min_label.font()
        f.setPointSize(12)
        self.min_label.setFont(f)
        self.min_box.setFont(f)
        self.min_box.setValidator(QRegExpValidator(QRegExp('^-?[1-9][0-9]*\\.?[0-9]*$')))

    def init_max_box(self):
        self.max_label.setText('max')
        self.max_box.setGeometry(450, 650, 100, 30)
        self.max_label.setGeometry(400, 650, 100, 30)
        self.max_box.setText('1.0')
        f = self.max_label.font()
        f.setPointSize(12)
        self.max_label.setFont(f)
        self.max_box.setFont(f)
        self.max_box.setValidator(QRegExpValidator(QRegExp('^-?[1-9][0-9]*\\.?[0-9]*$')))

    def init_f_of_x_label(self):
        self.f_of_x_label.setText('f(x) = ')
        self.f_of_x_label.setGeometry(200, 600, 300, 30)
        f = self.f_of_x_label.font()
        f.setPointSize(12)
        self.f_of_x_label.setFont(f)

    def init_text_box(self):
        self.expr_text_box.setGeometry(250, 600, 300, 30)
        f = self.expr_text_box.font()
        f.setPointSize(12)
        self.expr_text_box.setFont(f)

    def init_plot_button(self):
        self.plot_button.setGeometry(640, 600, 100, 30)
        self.plot_button.clicked.connect(self.on_plot_click)
        f = self.plot_button.font()
        f.setPointSize(12)
        self.plot_button.setFont(f)

    def init_error_label(self):
        self.error_label.setGeometry(0, 685, 1000, 50)
        self.error_label.setStyleSheet('QLabel { color: red }')
        label_font = self.error_label.font()
        label_font.setPointSize(14)
        label_font.setFamily('Consolas')
        self.error_label.setFont(label_font)
        self.error_label.setAlignment(Qt.AlignCenter)

    @pyqtSlot()
    def on_plot_click(self):
        textbox_value = self.expr_text_box.text()

        if textbox_value == '':
            return

        parser = Parser(textbox_value)
        ast = parser.parse()
        errors = ast.errors

        if len(errors) > 0:
            self.error_label.setText(errors[0])
            return

        if self.min_box.text() == '':
            self.error_label.setText('Error: Minimum x value(min) must be entered.')
            return

        if self.max_box.text() == '':
            self.error_label.setText('Error: Maximum x value(max) must be entered.')
            return

        x_min = float(self.min_box.text())
        x_max = float(self.max_box.text())

        try:
            x1, y1 = evaluate_in_range(ast, x_min, x_max)
            self.canvas.x_values = x1
            self.canvas.y_values = y1
            self.canvas.show_plot()
            self.error_label.setText('')
        except Exception as e:
            error_text = str(e)
            self.error_label.setText(error_text)
