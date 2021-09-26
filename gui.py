import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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

    def show_plot(self):
        self.ax.cla()
        self.ax.plot(self.x_values, self.y_values)
        self.ax.grid()
        self.figure.canvas.draw_idle()


class PlotterWidget(QWidget):
    def __init__(self, x_values, y_values):
        super().__init__()
        self.setFixedSize(1000, 750)
        self.chart = Canvas(self, x_values, y_values)
        self.text_box = QLineEdit(self)
        self.text_box.setGeometry(250, 600, 300, 30)
        self.plot_button = QPushButton('Plot', self)
        self.plot_button.setGeometry(640, 600, 100, 30)

        self.plot_button.clicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        textbox_value = self.text_box.text()
        parser = Parser(textbox_value)
        x1, y1 = evaluate_in_range(parser.parse(), -1, 1)
        self.chart.x_values = x1
        self.chart.y_values = y1

        self.chart.show_plot()
