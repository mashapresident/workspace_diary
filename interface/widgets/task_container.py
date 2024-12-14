from PySide6.QtWidgets import QVBoxLayout, QWidget, QScrollArea
from PySide6.QtCore import Qt
from interface.widgets.task import task_view
from interface.widgets.text import text
class task_container(QWidget):
    def __init__(self, label: str, tasks_list: list, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.setFixedWidth(250)
        
        # Основний макет для контейнера
        self.main_layout = QVBoxLayout(self)

        # Заголовок
        self.title = text(label, 16, "white")
        self.title.setStyleSheet("font-size: 16px; color: white;")
        self.main_layout.addWidget(self.title)

        # Прокручуваний контейнер
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")

        # Віджет для прокручуваного контенту
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        # Установимо напрямок для вертикального лейаута так, щоб завдання з'являлись зверху
        self.scroll_layout.setAlignment(Qt.AlignTop)  # Ensure tasks align to the top

        # Додавання завдань до прокручуваного контейнера
        self.update_tasks(tasks_list)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

    def update_tasks(self, tasks_list: list):
        """Оновлює список завдань в контейнері."""
        # Очистити поточний список завдань
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Додавання нових завдань
        for t in tasks_list:
            task_widget = task_view(t)  
            self.scroll_layout.addWidget(task_widget)

        # Оновлюємо вид, щоб завдання відображались з самого верху
        self.scroll_area.ensureVisible(0, 0)
