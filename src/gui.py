from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QLabel, QComboBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorting Visualization")
        self.setGeometry(100, 100, 800, 700)

        # Sorting array
        self.array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        self.n = len(self.array)
        self.i = 0
        self.j = 0
        self.sorted_index = self.n
        self.swap_indices = (-1, -1)
        self.is_swapping = False

        # Initialize Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.bubble_sort_step)

        # Current sorting algorithm (default to Bubble Sort)
        self.current_algorithm = "Bubble Sort"

        # Setup the dropdown for algorithm selection
        self.algorithm_dropdown = QComboBox(self)
        self.algorithm_dropdown.addItems(["Bubble Sort", "Insertion Sort", "Selection Sort"])

        # Increase font size for dropdown
        dropdown_font = QFont("Arial", 18)
        self.algorithm_dropdown.setFont(dropdown_font)

        # Setup buttons
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.restart_button = QPushButton("Restart", self)
        self.step_button = QPushButton("Step", self)

        button_font = QFont("Arial", 18)
        self.start_button.setFont(button_font)
        self.stop_button.setFont(button_font)
        self.restart_button.setFont(button_font)
        self.step_button.setFont(button_font)

        self.start_button.clicked.connect(self.start_sorting)
        self.stop_button.clicked.connect(self.stop_sorting)
        self.restart_button.clicked.connect(self.restart_sorting)
        self.step_button.clicked.connect(self.sort_step)

        # Setup button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.step_button)
        button_layout.addWidget(self.restart_button)

        # Setup color key layout
        key_layout = self.setup_color_key(button_font)

        # Setup main layout
        main_layout = QVBoxLayout()

        # Add the dropdown to the top
        main_layout.addWidget(self.algorithm_dropdown)

        # Add spacer to push buttons and key to the bottom
        main_layout.addStretch(1)

        # Add buttons and color key at the bottom
        main_layout.addLayout(button_layout)
        main_layout.addLayout(key_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_color_key(self, font):
        key_labels = [
            ("Default (Unsorted)", QColor(100, 200, 255)),
            ("Comparing", QColor(255, 255, 100)),
            ("Swapped", QColor(255, 100, 100)),
            ("Sorted", QColor(100, 255, 100)),
        ]
        layout = QHBoxLayout()
        for label_text, color in key_labels:
            label = QLabel(label_text)
            label.setFont(font)
            label.setStyleSheet(f"background-color: {color.name()}; padding: 10px;")
            label.setFixedHeight(50)  # Limit the height of the labels
            layout.addWidget(label)

        return layout

    def on_algorithm_change(self):
        self.current_algorithm = self.algorithm_dropdown.currentText()
        self.restart_sorting()

    def sort_step(self):
        if self.current_algorithm == "Bubble Sort":
            self.bubble_sort_step()
        elif self.current_algorithm == "Insertion Sort":
            self.insertion_sort_step()
        elif self.current_algorithm == "Selection Sort":
            self.selection_sort_step()
        self.update()

    def bubble_sort_step(self):
        if self.i < self.n - 1:
            if self.j < self.n - self.i - 1:
                if not self.is_swapping:
                    # Compare and decide whether to swap
                    if self.array[self.j] > self.array[self.j + 1]:
                        # Perform the swap immediately
                        self.array[self.j], self.array[self.j + 1] = (
                            self.array[self.j + 1],
                            self.array[self.j],
                        )
                        # Indicate the elements were swapped
                        self.is_swapping = True
                        self.swap_indices = (self.j, self.j + 1)
                    else:
                        self.j += 1  # Move to the next pair
                    self.update()
                else:
                    # Swap has been done, just move to the next pair
                    self.is_swapping = False
                    self.swap_indices = (-1, -1)
                    self.j += 1
                    self.update()
            else:
                # Move to the next round of sorting
                self.j = 0
                self.i += 1
                # Mark the sorted section
                self.sorted_index = self.n - self.i
                self.update()
        else:
            # Sorting is done, stop the timer
            self.sorted_index = 0
            self.timer.stop()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        bar_width = self.width() // len(self.array)
        max_height = self.height() - 240

        painter.setFont(QFont("Arial", 24, QFont.Bold))

        for i, value in enumerate(self.array):
            x = i * bar_width
            y = self.height() - (value / max(self.array)) * max_height - 120

            if i == self.swap_indices[0] or i == self.swap_indices[1]:
                color = QColor(255, 100, 100)  # Red for swapped
                painter.setPen(QPen(Qt.black, 4))
            elif i == self.j or i == self.j + 1:
                color = QColor(255, 255, 100)  # Yellow for comparison
                painter.setPen(QPen(Qt.black, 4))
            elif i >= self.sorted_index:
                color = QColor(100, 255, 100)  # Green for sorted section
                painter.setPen(Qt.NoPen)
            else:
                color = QColor(100, 200, 255)  # Default blue
                painter.setPen(Qt.NoPen)

            painter.setBrush(color)
            painter.drawRect(x, y, bar_width - 2, self.height() - y - 120)

            painter.setPen(Qt.black)
            painter.drawText(
                x, y, bar_width - 2, self.height() - y - 120, Qt.AlignCenter, str(value)
            )

            # Draw downward-facing arrows above the bars being compared, only if not fully sorted
            if self.sorted_index > 0 and (i == self.j or i == self.j + 1):
                arrow_y = y - 40
                painter.setPen(QPen(Qt.black, 4))
                painter.drawLine(
                    x + bar_width // 2, arrow_y, x + bar_width // 2, y - 10
                )
                painter.drawLine(
                    x + bar_width // 2, y - 10, x + bar_width // 2 - 10, y - 20
                )
                painter.drawLine(
                    x + bar_width // 2, y - 10, x + bar_width // 2 + 10, y - 20
                )

        if self.sorted_index == 0:
            # Final step: turn all elements green with thin outline
            for i in range(self.n):
                x = i * bar_width
                y = self.height() - (self.array[i] / max(self.array)) * max_height - 120
                painter.setPen(QPen(Qt.black, 2))  # Thin black outline for all bars
                painter.setBrush(QColor(100, 255, 100))  # Green color for all bars
                painter.drawRect(x, y, bar_width - 2, self.height() - y - 120)
                painter.setPen(Qt.black)
                painter.drawText(
                    x,
                    y,
                    bar_width - 2,
                    self.height() - y - 120,
                    Qt.AlignCenter,
                    str(self.array[i]),
                )

            self.sorted_index = -1  # Avoid re-triggering this section

    def start_sorting(self):
        self.timer.start(400)  # Slower to clearly see each step

    def stop_sorting(self):
        self.timer.stop()

    def restart_sorting(self):
        self.stop_sorting()
        self.i = 0
        self.j = 0
        self.sorted_index = self.n
        self.array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        self.swap_indices = (-1, -1)
        self.is_swapping = False
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
