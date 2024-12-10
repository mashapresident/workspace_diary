from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QScrollArea

from interface.widgets.task import task
from interface.widgets.text import text

class task_container(QWidget):
    def __init__(self, label: str, tasks_list: list[task], parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        # Основний макет для контейнера
        main_layout = QVBoxLayout(self)

        # Заголовок
        self.title = text(label, 16, "white")
        self.title.setStyleSheet("font-size: 16px; color: white;")
        main_layout.addWidget(self.title)

        # Прокручуваний контейнер
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")

        # Віджет для прокручуваного контенту
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Додавання завдань до прокручуваного контейнера
        for t in tasks_list:
            task_widget = task(t)  
            scroll_layout.addWidget(task_widget)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
