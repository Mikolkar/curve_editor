from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMenu,
    QHBoxLayout,
)
from PyQt6.QtGui import QAction


class ArrowButtonsWidget(QWidget):
    def __init__(self, change_callback=None):
        super().__init__()
        self.change_callback = change_callback

        self.jump = 1
        self.k_index = 0
        self.tmp_x = []
        self.tmp_y = []
        self.tmp_u_num = 100

        self.all_splines = []
        self.spline_index = 0
        self.chosen_spline = 0
        self.spline_changed = True
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_frame = QFrame()

        self.grid = QGridLayout(main_frame)

        # Setting buttons
        self.setButtons()

        # Adding all widgets to grid
        self.addWidgets()

        main_layout.addWidget(main_frame)
        self.setLayout(main_layout)

    def removeSpline(self, index):
        spline = self.spline_menu.actions()[index]
        self.spline_menu.removeAction(spline)
        self.change_callback([index], 4)

    def addCurve(self):
        if self.spline_changed:
            self.spline_changed = False
            self.change_callback([], 3)

            spline_name = f"Krzywa {self.spline_index}"
            spline_action = QAction(spline_name, self)
            spline_num = self.spline_index
            self.spline_menu.addAction(spline_action)
            spline_action.triggered.connect(
                lambda: self.change_callback([spline_num], 5),
            )

            self.spline_index += 1

    def movePoint(self, direction):
        if self.tmp_x != [] and self.tmp_y != []:
            if direction == "UP":
                self.tmp_y[self.k_index] += self.jump
            elif direction == "DOWN":
                self.tmp_y[self.k_index] -= self.jump
            elif direction == "LEFT":
                self.tmp_x[self.k_index] -= self.jump
            elif direction == "RIGHT":
                self.tmp_x[self.k_index] += self.jump
            else:
                print("Wrong direction")

            # Setting to functions x y
            if self.change_callback:
                self.change_callback([self.tmp_x, self.tmp_y, self.tmp_u_num], 0)

    def changePoints(self):
        self.setPoint()
        self.jump = int(self.btnJump.text())

    def setPoint(self):
        try:
            number = int(self.line.text())
            if number >= 0 and number < len(self.tmp_x):
                self.k_index = number
            else:
                print("Wrong index")
        except:
            print("Inpust must be integer")

    def changeU(self, inp):
        if inp > 1:
            self.tmp_u_num = inp
        else:
            if abs(inp) == 1:
                self.tmp_u_num += inp
        self.u_line.setText(f"{self.tmp_u_num}")
        # Setting to function u
        if self.tmp_x != [] and self.tmp_y != []:
            if self.change_callback:
                self.change_callback([self.tmp_x, self.tmp_y, self.tmp_u_num], 0)

    def setButtons(self):
        def setMoveButtons():
            self.line = QLineEdit("0")
            self.btnJump = QLineEdit(f"{self.jump}")

            # UP, DOWN, LEFT, RIGHT
            self.btnUp = QPushButton("↥")
            self.btnDown = QPushButton("↧")
            self.btnLeft = QPushButton("↤")
            self.btnRight = QPushButton("↦")
            self.ok = QPushButton("OK")

            # Actions for buttons
            self.ok.clicked.connect(self.changePoints)
            self.btnUp.clicked.connect(lambda: self.movePoint("UP"))
            self.btnDown.clicked.connect(lambda: self.movePoint("DOWN"))
            self.btnLeft.clicked.connect(lambda: self.movePoint("LEFT"))
            self.btnRight.clicked.connect(lambda: self.movePoint("RIGHT"))

            self.btnUp.setAutoRepeat(True)
            self.btnDown.setAutoRepeat(True)
            self.btnLeft.setAutoRepeat(True)
            self.btnRight.setAutoRepeat(True)

        def set_U_Buttons():
            self.u_line = QLineEdit(f"{self.tmp_u_num}")
            self.add = QPushButton("+1")
            self.sub = QPushButton("-1")
            self.okay = QPushButton("OK")

            # Actions for buttons
            self.okay.clicked.connect(lambda: self.changeU(int(self.u_line.text())))
            self.add.clicked.connect(lambda: self.changeU(1))
            self.sub.clicked.connect(lambda: self.changeU(-1))

        def setOtherButtons():
            # save button
            self.save_points = QPushButton("Zapisz punkty")
            self.save_points.clicked.connect(lambda: self.change_callback([], 1))

            # choose file button
            self.choose_file = QPushButton("Wybierz plik")
            self.choose_file.clicked.connect(lambda: self.change_callback([], 2))

            # Spline buttons
            # new spline
            self.new_spline = QPushButton("Nowa krzywa")
            self.new_spline.clicked.connect(self.addCurve)

            # chose spline
            self.choose_spline = QPushButton("Wybierz krzywą")
            self.spline_menu = QMenu(self)
            self.choose_spline.setMenu(self.spline_menu)
            spline_name = f"Krzywa {self.spline_index}"
            spline_action = QAction(spline_name, self)
            spline_num = self.spline_index
            self.spline_menu.addAction(spline_action)
            spline_action.triggered.connect(
                lambda: self.change_callback([spline_num], 5),
            )

            self.spline_index += 1
            # self.addCurve()

            # remove spline
            self.rm_spline = QPushButton("Usuń krzywą")
            self.rm_spline.clicked.connect(lambda: self.change_callback([], 4))

        setMoveButtons()
        set_U_Buttons()
        setOtherButtons()

    # Fuctions for buttons
    def addWidgets(self):
        def setLabels():
            self.label_2 = QLabel("Rozmiar u")
            self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.label = QLabel("Przesuń punkt")
            self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ind = 1

        # Setting labels
        setLabels()

        # choose file button
        self.grid.addWidget(self.choose_file, ind - 1, 0, 1, 3)
        # u buttons and line
        self.grid.addWidget(self.label_2, ind, 0, 1, 3)
        self.grid.addWidget(self.u_line, ind + 1, 0, 1, 3)
        self.grid.addWidget(self.add, ind + 2, 2)
        self.grid.addWidget(self.okay, ind + 2, 1)
        self.grid.addWidget(self.sub, ind + 2, 0)

        # move buttons and line
        frame = QFrame()
        lay = QHBoxLayout(frame)
        lay.addWidget(self.line)
        lay.addWidget(self.btnJump)
        self.grid.addWidget(self.label, ind + 3, 0, 1, 3)
        # self.grid.addWidget(self.line, ind + 4, 0, 1, 1)
        # self.grid.addWidget(self.btnJump, ind + 4, 2, 1, 2)
        self.grid.addWidget(frame, ind + 4, 0, 1, 3)

        self.grid.addWidget(self.btnUp, ind + 5, 1)
        self.grid.addWidget(self.btnDown, ind + 7, 1)
        self.grid.addWidget(self.btnLeft, ind + 6, 0)
        self.grid.addWidget(self.btnRight, ind + 6, 2)
        self.grid.addWidget(self.ok, ind + 6, 1)

        # save points button
        self.grid.addWidget(self.new_spline, ind + 8, 0, 1, 3)
        self.grid.addWidget(self.choose_spline, ind + 9, 0, 1, 3)
        self.grid.addWidget(self.rm_spline, ind + 10, 0, 1, 3)
        self.grid.addWidget(self.save_points, ind + 11, 0, 1, 3)
        self.grid.setRowStretch(ind + 12, 1)
