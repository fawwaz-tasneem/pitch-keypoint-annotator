import sys
from PyQt6 import QtWidgets
from gui.annotation_tool import AnnotationTool

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AnnotationTool()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
