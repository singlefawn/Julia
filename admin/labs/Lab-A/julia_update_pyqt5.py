# refractor of julia to support PyQt5

import os
import random
from PIL import Image
from PyQt5 import QtWidgets, QtGui, QtCore

class CustomScrollBar(QtWidgets.QSlider):
    def __init__(self, parent=None):
        super().__init__(QtCore.Qt.Vertical, parent)
        self.setStyleSheet("""
            QSlider::groove:vertical {
                background: black;
                width: 15px;
            }
            QSlider::handle:vertical {
                image: url('path/to/scroll_orb.png');
                height: 43px;
            }
        """)

class JuliaBox(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Julia AI")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("background-color: black;")
        layout = QtWidgets.QVBoxLayout(self)

        # Logo
        self.logo = QtGui.QPixmap('path/to/logo.png')
        self.logo_label = QtWidgets.QLabel(self)
        self.logo_label.setPixmap(self.logo)
        layout.addWidget(self.logo_label)

        # Font Customization
        font = QtGui.QFont("Arial", 16)

        # Text Frame and Text Box
        text_frame = QtWidgets.QFrame(self)
        text_frame.setStyleSheet("background-color: black;")
        text_frame_layout = QtWidgets.QHBoxLayout(text_frame)
        self.text_box = QtWidgets.QTextEdit(text_frame)
        self.text_box.setFont(font)
        self.text_box.setStyleSheet("color: white; background-color: black;")
        text_frame_layout.addWidget(self.text_box)
        layout.addWidget(text_frame)

        # Custom Scrollbar
        self.scrollbar = CustomScrollBar(self)
        layout.addWidget(self.scrollbar)

        # "Live Gen" Counter
        self.gen_counter = 0
        self.gen_label = QtWidgets.QLabel(f"Live Gen: {self.gen_counter}", self)
        self.gen_label.setStyleSheet("color: white; font-size: 20px; background: transparent;")
        layout.addWidget(self.gen_label)

        # Send Button
        self.send_button_image = QtGui.QPixmap('path/to/send_button.png')
        self.submit_button = QtWidgets.QLabel(self)
        self.submit_button.setPixmap(self.send_button_image)
        self.submit_button.mousePressEvent = self.julia_box
        layout.addWidget(self.submit_button)

        # Floating Div (Custom Widget)
        self.floating_div = QtWidgets.QWidget(self)
        self.floating_div.setStyleSheet("background-color: white;")
        floating_layout = QtWidgets.QVBoxLayout(self.floating_div)
        # Add elements to floating_layout

        # Input Message
        self.input_message = QtWidgets.QLineEdit(self)
        self.input_message.setPlaceholderText("Enter your message here")
        layout.addWidget(self.input_message)

        # Custom Interactions
        # Additional code to handle other custom interactions

        self.setLayout(layout)


    def load_random_photo(self):
        photo_dir = "../../../theta"
        photo_filenames = [f for f in os.listdir(photo_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
        random.shuffle(photo_filenames)
        photo_path = os.path.join(photo_dir, photo_filenames[0])
        photo = Image.open(photo_path)
        width, height = photo.size
        aspect_ratio = width / height
        target_aspect_ratio = 800 / 500
        if aspect_ratio > target_aspect_ratio:
            new_width = 1100
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = 500
            new_width = int(new_height * aspect_ratio)
        photo = photo.resize((new_width, new_height))

        # Convert PIL Image to QImage
        qimage = QtGui.QImage(photo.tobytes('raw', 'RGB'), new_width, new_height, QtGui.QImage.Format_RGB888)
        self.photo = QtGui.QPixmap.fromImage(qimage)

        if hasattr(self, 'photo_label'):
            self.photo_label.setPixmap(self.photo)  # Update the existing label
        else:
            self.photo_label = QtWidgets.QLabel(self)
            self.photo_label.setPixmap(self.photo)
            self.photo_label.setContentsMargins(0, 0, 0, 15)  # Padding (0, 15) at the bottom
            self.layout().addWidget(self.photo_label)
    def julia_box(self, event):
        # Code for handling the submit button action
        pass

    def update_live_gen_counter(self, live_gen):
        self.gen_label.setText(f"Live Gen: {live_gen}")

    def on_custom_event(self, event):
        # Code to handle custom events or interactions
        pass

    # Additional methods for handling custom interactions, events, etc.

app = QtWidgets.QApplication([])
window = JuliaBox()
window.show()
app.exec_()
