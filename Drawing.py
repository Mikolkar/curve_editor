import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MatplotlibWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = FigureCanvas(
            Figure(figsize=(8, 8))
        )  # Rozmiar wykresu 80x80 jednostek
        self.ax = self.canvas.figure.subplots()
        self.ax.set_xlim(0, 80)
        self.ax.set_ylim(0, 80)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        # Początek od górnego lewego rogu
        self.current_pos = [0, 80]

    def draw_letter_a(self):
        # Koordynaty dla litery 'a'
        # Skalowanie litery
        x = np.array([1, 2, 2, 1, 1]) * 3
        # Skalowanie litery
        y = np.array([1, 1, 2, 2, 1]) * 3

        self.ax.plot(
            x + self.current_pos[0], self.current_pos[1] - y, "b-"
        )  # Rysowanie z uwzględnieniem obecnej pozycji
        self.canvas.draw()

        # Aktualizacja pozycji
        # Przesuwanie o szerokość litery 'a'
        self.current_pos[0] += 6
        if self.current_pos[0] > 80:
            self.new_line()

    def new_line(self):
        # Przejście do nowej linii
        self.current_pos[1] -= 10
        self.current_pos[0] = 0


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = MatplotlibWidget()
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Rysowanie Liter")
        self.resize(800, 800)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_A:
            self.central_widget.draw_letter_a()
        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.central_widget.new_line()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
