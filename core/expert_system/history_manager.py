import os
import json
from datetime import datetime

from PyQt6.QtWidgets import QListWidget, QListWidgetItem


class HistoryManager:

    def __init__(self, history_list: QListWidget, sessions_dir: str = "sessions"):

        self.history_list = history_list
        self.sessions_dir = sessions_dir

        self.session_id: str | None = None
        self.steps: list[dict] = []
        self.report: str = ""
        self.last_chat_id: str | None = None

        os.makedirs(self.sessions_dir, exist_ok=True)

    def start_session(
        self, session_id: str | None = None, start_chat_id: str = "START"
    ):

        if session_id is None:
            # unique token id
            session_id = f'token {datetime.now().strftime("%d.%m.%Y %H-%M-%S")}'

        self.session_id = session_id
        # new variable
        self.created_at = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
        self.steps.clear()
        self.report = ""
        self.last_chat_id = start_chat_id

        self.history_list.clear()

    def add_step(
        self,
        chat_id: str,
        question: str,
        answer: str,
        recommendation: str = "",
        result: str = "",
    ):

        if self.steps:
            last = self.steps[-1]
            if last.get("chat_id") == chat_id:
                return

        index = len(self.steps) + 1

        step = {
            "index": index,
            "chat_id": chat_id,
            "question": question.strip(),
            "answer": answer.strip(),
            "recommendation": recommendation.strip(),
            "result": result.strip(),
        }

        self.steps.append(step)

        display_text = [
            f"Крок {index} (вузол: {chat_id})",
            f"Q: {step['question'] or '-'}",
            f"A: {step['answer'] or '-'}",
        ]
        if step["recommendation"]:
            display_text.append(f"Рекомендація:\n{step['recommendation']}")
        if step["result"]:
            display_text.append(f"Результат:\n{step['result']}")

        item = QListWidgetItem("\n".join(display_text))
        self.history_list.addItem(item)

        self.history_list.scrollToBottom()

    def set_report(self, report_text: str, last_chat_id: str | None = None):

        if self.report:
            if self.last_chat_id == last_chat_id:
                return

        if last_chat_id is not None:
            self.last_chat_id = last_chat_id

        self.report = report_text.strip()

        if self.report:
            item = QListWidgetItem("=== ЗВІТ ===\n" + self.report)
            self.history_list.addItem(item)
            self.history_list.scrollToBottom()

    def to_dict(self) -> dict:
        return {
            "version": 1,
            "session_id": self.session_id,
            "created_at": self.created_at,
            # new variable
            "updated_at": datetime.now().strftime("%d.%m.%Y %H-%M-%S"),
            "last_chat_id": self.last_chat_id,
            "steps": self.steps,
            "report": self.report,
        }

    def save_to_file(self, path: str | None = None) -> str:

        if self.session_id is None:
            self.start_session()

        if path is None:
            filename = f'{self.session_id.replace("token ", "")} session.es.json'
            path = os.path.join(self.sessions_dir, filename)

        data = self.to_dict()
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(f"Сесію збережено у файл: {path}\n")
        return path

    def load_session(self, path: str) -> str | None:

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.session_id = data.get("session_id")
        self.created_at = data.get("created_at")
        self.steps = data.get("steps", [])
        self.report = data.get("report", "")
        self.last_chat_id = data.get("last_chat_id")

        self.history_list.clear()

        for step in self.steps:
            display_text = [
                f"Крок {step.get('index')} (вузол: {step.get('chat_id')})",
                f"Q: {step.get('question') or '-'}",
                f"A: {step.get('answer') or '-'}",
            ]
            if step.get("recommendation"):
                display_text.append(f"Рекомендація:\n{step['recommendation']}")
            if step.get("result"):
                display_text.append(f"Результат:\n{step['result']}")

            item = QListWidgetItem("\n".join(display_text))
            self.history_list.addItem(item)

        if self.report:
            item = QListWidgetItem("=== ЗВІТ ===\n" + self.report)
            self.history_list.addItem(item)

        self.history_list.scrollToBottom()

        return self.last_chat_id
