import json
from PyQt6.QtWidgets import QPushButton


class ChatManager:

    def __init__(self):
        self.knowledge_base = self.load_knowledge_base()
        self.current_question_id = "START"

    def load_knowledge_base(self):
        with open("core/knowledge_base.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def get_question_data(self, question_id):
        return self.knowledge_base.get(question_id)

    def generate_chat_content(self, question_title, answers_layout, next_question):
        self.clear_answers(answers_layout)
        question_data = self.get_question_data(self.current_question_id)
        self.add_question_to_chat(question_data["question"], question_title)
        self.create_answer_buttons(
            question_data["answers"], answers_layout, next_question
        )

    def add_question_to_chat(self, question_information, question_title):
        question_title.setText(f"{question_information}")

    def create_answer_buttons(self, answers_information, answers_layout, next_question):
        for answer_text, next_id in answers_information.items():
            button_answer = QPushButton(answer_text)
            button_answer.setObjectName("button_answer")
            button_answer.clicked.connect(lambda checked, id=next_id: next_question(id))
            answers_layout.addWidget(button_answer)

    def clear_answers(self, layout):
        if layout is None:
            return

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def handle_answer(self, next_id, question_title, answers_layout, next_level):
        self.current_question_id = next_id
        self.generate_chat_content(question_title, answers_layout, next_level)
