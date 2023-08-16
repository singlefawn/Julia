# livegen.py


import os
from PyQt5 import QtWidgets, QtCore
import math
import time
from PyQt5.QtGui import QFontDatabase, QFont


class TransparentWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Construct the custom font path dynamically
        current_dir = os.path.dirname(os.path.abspath(__file__))
        custom_font_path = os.path.join(current_dir, "admin/assets/century-gothic/CenturyGothic.ttf")

        font_id = QFontDatabase.addApplicationFont(custom_font_path)
        font_families = QFontDatabase.applicationFontFamilies(font_id)

        if font_families:
            custom_font_family = font_families[0]
            custom_font = QFont(custom_font_family, 20)
        else:
            print("Failed to load custom font. Using default font instead.")
            custom_font = QFont("Arial", 20)

        self.label = QtWidgets.QLabel(f"Live Gen: 0", self)
        self.label.setFont(custom_font)
        self.label.setStyleSheet("color: white;")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Set up timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_gen)
        self.timer.start(1)  # Update every millisecond

    def ts_to_gen(self, ts):
        gen = math.pow(1.0002, (ts - 1675084800) / 3300)
        return gen

    def update_gen(self):
        ts = time.time()
        gen = self.ts_to_gen(ts)
        formatted_gen = "{:.15f}".format(gen)  # Format with 15 decimal places
        self.label.setText(f"Live Gen: {formatted_gen}")


app = QtWidgets.QApplication([])
window = TransparentWindow()
window.show()
app.exec_()
