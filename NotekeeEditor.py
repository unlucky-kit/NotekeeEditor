import sys
from PyQt5.QtWidgets import QApplication
from katex import NotekeeEditor

# Run the application if this file is executed directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    playground = NotekeeEditor()
    playground.show()
    sys.exit(app.exec_())
