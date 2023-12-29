from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt


class OneLineTextEdit(QTextEdit):
    def __init__(self, parent, ref):
        super().__init__(parent)
        self.ref = ref
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setMaximumHeight(30)
        self.setPlaceholderText("Enter new chapter name here...")
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAcceptRichText(False)        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            new_chapter = self.toPlainText()
            self.ref.create_new_chapter(new_chapter)
        else:
            super().keyPressEvent(event)