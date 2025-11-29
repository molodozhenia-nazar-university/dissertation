from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt


class MyWidget_HistoryInBubbleStyle(QWidget):

    def __init__(self, step: dict, parent=None):

        super().__init__(parent)

        layout = QVBoxLayout(self)

        # Header for step
        bubble_header_for_step_label = QLabel(
            f"Крок {step.get('index')} (вузол: {step.get('chat_id')})"
        )
        bubble_header_for_step_label.setObjectName("bubble_header_for_step_label")

        # Add to global layout
        layout.addWidget(bubble_header_for_step_label)

        # Bubble Question (Q)
        if step.get("question"):

            bubble_question_frame = QFrame()
            bubble_question_frame.setObjectName("bubble_question_frame")

            bubble_question_layout = QVBoxLayout(bubble_question_frame)
            # bubble_question_layout.setContentsMargins(0, 0, 0, 0)

            bubble_question_label = QLabel(step.get("question"))
            bubble_question_label.setWordWrap(True)

            # Add to local layout
            bubble_question_layout.addWidget(bubble_question_label)
            # Add to global layout
            layout.addWidget(bubble_question_frame)

        # Bubble Answer (A)
        if step.get("answer"):

            bubble_answer_frame = QFrame()
            bubble_answer_frame.setObjectName("bubble_answer_frame")

            bubble_answer_layout = QVBoxLayout(bubble_answer_frame)
            # bubble_answer_layout.setContentsMargins(0, 0, 0, 0)

            bubble_answer_label = QLabel(step.get("answer"))
            bubble_answer_label.setWordWrap(True)

            # Add to local layout
            bubble_answer_layout.addWidget(bubble_answer_label)
            # Add to global layout
            layout.addWidget(bubble_answer_frame)

        # Bubble Recommendation (R1)
        if step.get("recommendation"):

            bubble_recommendation_frame = QFrame()
            bubble_recommendation_frame.setObjectName("bubble_recommendation_frame")

            bubble_recommendation_layout = QVBoxLayout(bubble_recommendation_frame)
            # bubble_recommendation_layout.setContentsMargins(0, 0, 0, 0)

            bubble_recommendation_label = QLabel(step.get("recommendation"))
            bubble_recommendation_label.setWordWrap(True)

            # Add to local layout
            bubble_recommendation_layout.addWidget(bubble_recommendation_label)
            # Add to global layout
            layout.addWidget(bubble_recommendation_frame)

        # Bubble Result (R2)
        if step.get("result"):

            bubble_result_frame = QFrame()
            bubble_result_frame.setObjectName("bubble_result_frame")

            bubble_result_layout = QVBoxLayout(bubble_result_frame)
            # bubble_result_layout.setContentsMargins(0, 0, 0, 0)

            bubble_result_label = QLabel(step.get("result"))
            bubble_result_label.setWordWrap(True)

            # Add to local layout
            bubble_result_layout.addWidget(bubble_result_label)
            # Add to global layout
            layout.addWidget(bubble_result_frame)
