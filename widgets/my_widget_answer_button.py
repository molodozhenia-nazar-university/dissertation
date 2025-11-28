from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt


class MyWidget_AnswerButton(QPushButton):

    def __init__(self, text: str = "", parent=None):

        super().__init__("", parent)

        self._label = QLabel(text, self)
        self._label.setWordWrap(True)
        self._label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        layout = QHBoxLayout(self)
        layout.addWidget(self._label)

        # size settings for MyWidget_AnswerButton
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def setText(self, text: str) -> None:
        self._label.setText(text)

    def text(self) -> str:
        return self._label.text()
