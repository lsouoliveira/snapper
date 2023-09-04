from PyQt5 import QtWidgets
from .app import App
import sys

def excepthook(exc_type, exc_value, exc_tb):
    QtWidgets.QApplication.quit()

def main():
    sys.excepthook = excepthook

    app = App()
    app.exec_()


if __name__ == "__main__":
    main()
