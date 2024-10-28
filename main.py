import sys
from PyQt5.QtWidgets import QApplication
from src.app import CodeforcesApp

def main():
    app = QApplication(sys.argv)
    ex = CodeforcesApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()