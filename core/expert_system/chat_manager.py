import json
from PyQt6.QtWidgets import QPushButton
from widgets.my_widget_answer_button import MyWidget_AnswerButton


class ChatManager:

    def __init__(
        self,
        message_title,
        description_title,
        question_title,
        recommendation_title,
        answers_layout,
        result_title,
        report_title,
        button_end_session,
        history_manager,
    ):
        self.knowledge_base = self.load_knowledge_base()
        self.current_chat_id = "START"
        self.message_title = message_title
        self.description_title = description_title
        self.question_title = question_title
        self.recommendation_title = recommendation_title
        self.answers_layout = answers_layout
        self.result_title = result_title
        self.report_title = report_title
        self.button_end_session = button_end_session
        self.history_manager = history_manager

    def load_knowledge_base(self):
        with open("knowledge_base/knowledge_base.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def get_chat_data(self, chat_id):
        return self.knowledge_base.get(chat_id)

    # Generate Chat Content

    def generate_chat_content(self, next_chat):

        # self.empty_message()
        # self.empty_description()
        self.empty_question()
        self.empty_recommendation()
        self.clear_answers()
        self.empty_result()

        chat_data = self.get_chat_data(self.current_chat_id)

        # Start Test
        if not chat_data:
            print(f"Немає даних для: {self.current_chat_id}")
            return

        print(f"Чат: {self.current_chat_id}\nТип чату: {chat_data['type']}\n")
        # End Test

        if chat_data["type"] == "user":
            self.handle_user(chat_data, next_chat)
        elif chat_data["type"] == "system":
            self.handle_system(chat_data, next_chat)
        elif chat_data["type"] == "report":
            self.handle_user(chat_data, next_chat)
            self.handle_report(chat_data)

    # Handle Chat

    def handle_chat(self, next_chat_id, next_chat):
        self.current_chat_id = next_chat_id
        self.generate_chat_content(next_chat)

        if self.history_manager is not None:
            self.history_manager.last_chat_id = self.current_chat_id

    # Handle User

    def add_question_to_chat(self, question_information):
        self.question_title.setText(f"{question_information}")
        if self.question_title.text().strip() != "":
            self.question_title.setVisible(True)
        else:
            self.question_title.setVisible(False)

    def add_recommendation_to_chat(self, recommendation_information):
        self.recommendation_title.setText(f"{recommendation_information}")
        if self.recommendation_title.text().strip() != "":
            self.recommendation_title.setVisible(True)
        else:
            self.recommendation_title.setVisible(False)

    def create_answer_buttons(self, answers_information, next_chat):
        for answer_text, next_chat_id in answers_information.items():
            button_answer = MyWidget_AnswerButton(answer_text)
            button_answer.setObjectName("button_answer")

            def on_click(checked=False, chat_id=next_chat_id, answer=answer_text):
                if self.history_manager is not None:
                    self.history_manager.add_step(
                        chat_id=self.current_chat_id,
                        question=self.question_title.text(),
                        answer=answer,
                        recommendation=self.recommendation_title.text(),
                        result=self.result_title.text(),
                    )
                next_chat(chat_id)

            button_answer.clicked.connect(on_click)
            self.answers_layout.addWidget(button_answer)

    def add_result_to_chat(self, result_information):
        self.result_title.setText(f"{result_information}")
        if self.result_title.text().strip() != "":
            self.result_title.setVisible(True)
        else:
            self.result_title.setVisible(False)

    def handle_user(self, chat_data, next_chat):
        self.add_question_to_chat(chat_data.get("question", ""))
        self.add_recommendation_to_chat(
            "\n".join(chat_data.get("recommendation") or [])
        )
        answers = chat_data.get("answers") or {}
        if answers:
            self.create_answer_buttons(answers, next_chat)
            self.answers_layout.parentWidget().setVisible(True)
        else:
            self.answers_layout.parentWidget().setVisible(False)
        self.add_result_to_chat("\n".join(chat_data.get("result") or []))

    # Handle System

    def add_message_to_chat(self, message_information):
        self.message_title.setText(f"{message_information}")
        if self.message_title.text().strip() != "":
            self.message_title.setVisible(True)
        else:
            self.message_title.setVisible(False)

    def add_description_to_chat(self, description_information):
        self.description_title.setText(f"{description_information}")
        if self.description_title.text().strip() != "":
            self.description_title.setVisible(True)
        else:
            self.description_title.setVisible(False)

    def execute_action(self, action, next_chat):

        try:

            from core.expert_system import test_network

            function = getattr(test_network, action)
            result = function()

            # for object and dictionary
            if hasattr(result, "description") and hasattr(result, "next_chat_id"):
                self.add_description_to_chat(result.description)
                print(f"function result - object\n")
                next_chat(result.next_chat_id)
            elif (
                isinstance(result, dict)
                and "description" in result
                and "next_chat_id" in result
            ):
                self.add_description_to_chat(result["description"])
                print(f"function result - dictionary\n")
                next_chat(result["next_chat_id"])

        except AttributeError:
            print(f"Функція {action} не знайдена в network_test.py")
        except Exception as e:
            print(f"Помилка виконання {action}: {e}")

    def handle_system(self, chat_data, next_chat):
        self.add_message_to_chat(chat_data["message"])
        self.execute_action(chat_data["action"], next_chat)

    # Handle Report

    def add_report_to_chat(self, report_information):
        self.report_title.setText(f"{report_information}")
        self.report_title.setVisible(True)

    def handle_report(self, chat_data):
        self.add_report_to_chat("\n".join(chat_data.get("report") or []))
        self.button_end_session.setVisible(True)

        if self.history_manager is not None:
            self.history_manager.set_report(
                "\n".join(chat_data.get("report") or []),
                last_chat_id=self.current_chat_id,
            )

    # Clear Chat

    def empty_message(self):
        self.action_title.setText(f"")

    def empty_description(self):
        self.description_title.setText(f"")

    def empty_question(self):
        self.question_title.setText(f"")

    def empty_recommendation(self):
        self.recommendation_title.setText(f"")

    def clear_answers(self):
        if self.answers_layout is None:
            return

        while self.answers_layout.count():
            child = self.answers_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def empty_result(self):
        self.result_title.setText(f"")
