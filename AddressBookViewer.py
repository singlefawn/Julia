import os  # Add this line to import the os module
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt

class AddressBookViewer(QDialog):
    def __init__(self, parent=None):
        super(AddressBookViewer, self).__init__(parent)
        self.setWindowTitle("Address Book Viewer")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()
        self.contact_list = QListWidget(self)
        layout.addWidget(self.contact_list)
        self.text_browser = QTextBrowser(self)
        layout.addWidget(self.text_browser)
        self.setLayout(layout)

        # Connect the custom signal to the slot
        self.parent().contact_signal.contact_clicked.connect(self.set_contact_details)

        # Load and display contact names
        self.load_contact_names()

    @pyqtSlot(dict)
    def set_contact_details(self, contact_data):
        # Check if contact_data is not None
        if contact_data:
            details_text = f"Name: {contact_data['name']}\n"
            details_text += f"Phone Numbers: {', '.join(contact_data['phone_numbers'])}\n"
            details_text += f"Emails: {', '.join(contact_data['emails'])}\n"

            # Join the groups into a single string without extra commas
            details_text += f"Groups: {contact_data['groups']}\n"

            details_text += f"Tags: {', '.join(contact_data['tags'])}\n"
            details_text += f"Notes:\n{contact_data['notes']}\n"
            details_text += f"Website: {contact_data['website']}\n"
            details_text += f"Custom Social: {contact_data['custom_social']}\n"

            custom_fields = contact_data['custom_fields']
            if custom_fields:
                details_text += "Custom Fields:\n"
                for field_title, field_info in custom_fields.items():
                    details_text += f"{field_title}: {field_info}\n"

            self.text_browser.setPlainText(details_text)

    def load_contact_names(self):
        # Load contact names from the contacts directory and display them in the list
        contact_names = []
        for filename in os.listdir("contacts"):
            if filename.endswith(".json"):
                contact_names.append(filename[:-5])  # Remove the ".json" extension

        self.contact_list.clear()
        self.contact_list.addItems(contact_names)
        self.contact_list.itemClicked.connect(self.contact_clicked)

    def contact_clicked(self, item):
        # When a contact is clicked, emit the contact clicked signal with the contact's data
        contact_name = item.text()
        contact_data = self.load_contact_data(contact_name)
        self.parent().contact_signal.contact_clicked.emit(contact_data)

    def load_contact_data(self, contact_name):
        # Load contact data from the selected contact's JSON file
        contact_filename = os.path.join("contacts", f"{contact_name}.json")
        if os.path.exists(contact_filename):
            with open(contact_filename, "r") as f:
                return json.load(f)
        return None
