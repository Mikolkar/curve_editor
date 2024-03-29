import sys
import os
import matplotlib.image as mpimg
import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)

from app.controlPanel import ArrowButtonsWidget
from app.curves.de_casteljau import de_casteljau


class MatplotlibWidget(QWidget):
    def __init__(self, xlimit=800, ylimit=800):
        super().__init__()
        self.x_points, self.y_points = [], []

        self.xlimit = xlimit
        self.ylimit = ylimit

        self.current_spline = 0
        self.dots = []

        self.line = []
        self.lst_points = {}
        self.max_spline = 0

        # Points
        self.right_bar = ArrowButtonsWidget(self.manageCallbacks)
        self.u_num = self.right_bar.tmp_u_num

        self.setFixedHeight(600)
        self.initUI()

    def initUI(self):
        # Matplotlib varibles
        self.ctrl_pressed = False
        self.added = False
        self.drawing = False
        self.alt_pressed = False

        # Layouts
        self.main = QHBoxLayout(self)
        self.layout = QVBoxLayout()
        self.main.addLayout(self.layout)

        # Creating canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.ax = self.figure.add_subplot()
        self.ax.set_xlim(0, self.xlimit)
        self.ax.set_ylim(0, self.ylimit)

        # Toolbar
        self.toolbar = NavigationToolbar(self.canvas)
        self.layout.addWidget(self.toolbar)

        # Setting Canvas
        self.canvas.mpl_connect("button_press_event", self.onclick)
        self.addWidgets()

    def rm_lines_and_dots(self, arg=0):
        if len(self.x_points) > 1 and self.drawing:
            if arg == 0:
                if self.line:
                    for l in self.line:
                        l.remove()
                    self.line.clear()

            if arg == 0 or arg == 1:
                for l in self.dots:
                    l.remove()
                self.dots.clear()
            self.drawing = False

    def changePlot(self, x, y, u_num):
        self.x_points = x
        self.y_points = y
        self.u_num = u_num
        self.drawing = True
        self.plot(self.u_num)

    def plot(self, u):
        self.rm_lines_and_dots()

        for key in self.lst_points:
            x_points = self.lst_points[key][0]
            y_points = self.lst_points[key][1]
            u_num = self.u_num
            points = self.return_bezier_spline(x_points, y_points, u_num)

            # Drawing new line
            new_line = self.ax.plot(*points, "b-")

            # Adding new line to list
            self.line.extend(new_line)
        points = self.return_bezier_spline(self.x_points, self.y_points, self.u_num)
        # Drawing new line
        new_line = self.ax.plot(*points, "b-")

        # Adding new line to list
        self.line.extend(new_line)

        dot = self.ax.plot(self.x_points, self.y_points, "ro")
        self.dots.extend(dot)

        self.canvas.draw()

    def addWidgets(self):
        # Adding canvas to layout
        self.layout.addWidget(self.canvas)

        self.button = QPushButton("Wypisz punkty")
        self.button.clicked.connect(self.printVectors)

        self.main.addWidget(self.right_bar)

    def printVectors(self):
        u = np.linspace(0, 1, self.u_num + 1)

        arr_u = [k for k in u]

        print(f"x: {self.x_points}")
        print(f"y: {self.y_points}")

        print(f"u: {arr_u}")

    # Matplotlib events
    def onclick(self, event):
        # Adding points after clicking on canvas
        self.drawing = True
        if self.ctrl_pressed:
            if len(self.lst_points) == 0 or self.current_spline == self.max_spline:
                self.added = False

                self.x_points.append(event.xdata)
                self.y_points.append(event.ydata)

                self.right_bar.tmp_x = self.x_points
                self.right_bar.tmp_y = self.y_points

                self.right_bar.spline_changed = True
                self.canvas.draw()
                try:
                    self.plot(self.u_num)
                except:
                    self.x_points.pop()
                    self.y_points.pop()

        if self.alt_pressed:
            self.x_points.pop()
            self.y_points.pop()
            if len(self.x_points) > 1:
                self.plot(self.u_num)
            else:
                for l in self.line:
                    l.remove()
                self.line.clear()

                l = self.dots.pop()
                l.remove()
                self.canvas.draw()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = True

        if event.key() == Qt.Key.Key_Alt:
            self.alt_pressed = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_Control:
            self.ctrl_pressed = False

        if event.key() == Qt.Key.Key_Alt:
            self.alt_pressed = False

    def manageCallbacks(self, lst_args, callback):
        def addPoints():
            self.lst_points[len(self.lst_points)] = [
                self.x_points,
                self.y_points,
                self.u_num,
            ]

        def saveCurve(filename="splines/curve_data2.txt"):
            # Reading and printing file content
            index = 0
            self.lst_points[len(self.lst_points)] = [
                self.x_points,
                self.y_points,
                self.u_num,
            ]
            t = np.linspace(0, 1, self.u_num)

            arr_t = [k for k in t]

            for key in self.lst_points:
                try:
                    with open(filename, "r") as file:
                        for line in file:
                            if line.startswith("#"):
                                index = int(line[1:])
                        index += 1
                except FileNotFoundError:
                    print("Plik nie istnieje, zostanie utworzony.")

                # Appending to file
                with open(filename, "a") as file:
                    file.write(f"#{index}\n")
                    file.write(f"x: {self.lst_points[key][0]}\n")
                    file.write(f"y: {self.lst_points[key][1]}\n")
                    file.write(f"t: {arr_t}\n")
                    print("Zapisano 'numerki' do pliku")

        def openFileDialog():
            fileName, _ = QFileDialog.getOpenFileName(
                self,
                "Wybierz plik obrazu",
                "",
                "Pliki obrazów (*.jpg *.jpeg *.png *.bmp *.gif)",
            )
            if fileName:
                print(f"Wybrano plik: {fileName}")

                path = self.absPath(fileName)
                img = mpimg.imread(path)
                img_width, img_height = img.shape[1], img.shape[0]
                c_x = (self.xlimit - img_width) / 2
                c_y = (self.ylimit - img_height) / 2
                self.ax.imshow(
                    img, extent=[c_x, c_x + img_width, c_y, c_y + img_height]
                )
                self.canvas.draw()

        def clearLastSpline():
            if len(self.lst_points) == 0:
                return

            if not self.added:
                addPoints()
                self.added = True

            last_key = max(self.lst_points.keys())

            if len(self.lst_points) > 1:
                tmp_x = self.lst_points[last_key - 1][0]
                tmp_y = self.lst_points[last_key - 1][1]

                self.x_points, self.y_points = [tmp_x], [tmp_y]
            else:
                self.x_points, self.y_points = [], []

            self.right_bar.tmp_x = self.x_points
            self.right_bar.tmp_y = self.y_points

            if last_key in self.lst_points:
                self.lst_points.pop(last_key)

            # Remove last line from plot
            if self.line:
                last_line = self.line[-1]
                last_line.remove()
                self.line.pop()

            if self.dots:
                last_dot = self.dots[-1]
                last_dot.remove()
                self.dots.pop()

            last = self.right_bar.spline_menu.actions()[-1]  # Get the last action
            self.right_bar.spline_menu.removeAction(last)

            if self.current_spline == self.max_spline:
                self.current_spline -= 1
            self.max_spline -= 1
            self.right_bar.spline_index -= 1
            self.right_bar.spline_changed = True

            self.canvas.draw()

        def addSpline():
            if not self.added:
                addPoints()
                tmp_x = self.x_points[-1]
                tmp_y = self.y_points[-1]

                self.x_points = [tmp_x]
                self.y_points = [tmp_y]

                self.current_spline += 1

                self.drawing = True
                self.plot(self.u_num)
                self.canvas.draw()

                self.added = True
                self.max_spline += 1

        def chooseSpline():
            if (
                len(self.x_points) > 1
                and len(self.y_points) > 1
                and len(self.lst_points) >= 1
            ):
                if self.current_spline == self.max_spline:
                    self.lst_points[len(self.lst_points)] = [
                        self.x_points,
                        self.y_points,
                        self.u_num,
                    ]
                self.current_spline = lst_args[0]

            self.x_points = self.lst_points[self.current_spline][0]
            self.y_points = self.lst_points[self.current_spline][1]
            self.u_num = self.lst_points[self.current_spline][2]

            self.right_bar.tmp_x = self.x_points
            self.right_bar.tmp_y = self.y_points

            self.drawing = True
            self.rm_lines_and_dots(1)
            self.plot(self.u_num)

        if callback == 0:
            self.drawing = True
            self.u_num = lst_args[2]
            self.changePlot(lst_args[0], lst_args[1], lst_args[2])

        elif callback == 1:
            saveCurve()

        elif callback == 2:
            openFileDialog()

        elif callback == 3:
            addSpline()

        elif callback == 4:
            clearLastSpline()

        elif callback == 5:
            chooseSpline()

    def return_bezier_spline(self, x, y, u_len):
        t_values = np.linspace(0, 1, num=u_len)
        w = [1 for _ in range(len(x))]
        bezier_points = [de_casteljau(x, y, w, t) for t in t_values]

        x_values = [point[0] for point in bezier_points]
        y_values = [point[1] for point in bezier_points]

        return x_values, y_values

    def absPath(self, file_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ab_path = os.path.join(dir_path, file_name)
        return ab_path


class MainWindow(QMainWindow):
    def __init__(self, width=1200, height=800):
        super().__init__()
        screen_width = self.screen().geometry().width()
        screen_height = self.screen().geometry().height()

        # Setting central widget on MatplotlibWidget
        central = MatplotlibWidget(800, 800)
        self.setCentralWidget(central)
        self.setWindowTitle("Matplotlib z PyQt6")

        # Setting window size and position
        self.setGeometry(
            screen_width // 2 - width // 2,
            screen_height // 2 - height // 2,
            width,
            height,
        )
        central.setFixedHeight(height)


def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    # Executing app
    main()
