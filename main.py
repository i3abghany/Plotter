import os
import subprocess
import sys
from PyQt5.QtWidgets import QApplication

from gui import PlotterWidget


def main():
    app = QApplication(sys.argv)
    plotter_widget = PlotterWidget([], [])
    plotter_widget.show()
    sys.exit(app.exec_())


def run_tests():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.exit(subprocess.call([sys.executable,
                              '-m',
                              'unittest',
                              'discover',
                              '-t',
                              f'{project_dir}/test',
                              '-s',
                              f'{project_dir}/test']))


if __name__ == '__main__':
    if '--test' in sys.argv:
        run_tests()
    else:
        main()
