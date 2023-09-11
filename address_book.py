import sys
import os
import json
import datetime
import math
import time
import webbrowser  # Added for website opening
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QScrollArea, QMessageBox, QDialog, QComboBox, QListWidget, QListWidgetItem, QTextBrowser, QDesktopWidget, \
    QInputDialog
from PyQt5.QtCore import Qt, pyqtSignal, QObject  # Import QObject here
from AddressBookViewer import AddressBookViewer  # Import the AddressBookViewer class



def ts_to_gen(ts):
    gen = math.pow(1.0002, (ts - 1675084800) / 3300)
    return gen

class Contact:
    def __init__(self, name, phone_numbers, emails, groups, tags, notes, website, custom_social):  # Added custom_social parameter
        self.name = name
        self.phone_numbers = phone_numbers
        self.emails = emails
        self.groups = groups
        self.tags = tags
        self.notes = notes
        self.website = website
        self.custom_social = custom_social  # Added custom_social attribute
        self.timestamp = int(time.time())  # Current timestamp
        self.gen = ts_to_gen(self.timestamp)
        self.custom_fields = {}  # Dictionary for custom fields

    def to_json(self):
        return {
            "name": self.name,
            "phone_numbers": self.phone_numbers,
            "emails": self.emails,
            "groups": self.groups,
            "tags": self.tags,
            "notes": self.notes,
            "website": self.website,
            "custom_social": self.custom_social,  # Include custom_social in JSON
            "timestamp": self.timestamp,
            "gen": self.gen,
            "custom_fields": self.custom_fields  # Include custom fields in JSON
        }

    def save_as_json(self):
        contact_filename = os.path.join("contacts", f"{self.name}.json")
        with open(contact_filename, "w") as f:
            json.dump(self.to_json(), f, indent=4)

    def delete(self):
        contact_filename = os.path.join("contacts", f"{self.name}.json")
        trash_filename = os.path.join("contacts_trash", f"{self.name}.json")
        if os.path.exists(contact_filename):
            os.rename(contact_filename, trash_filename)


# Create a custom signal class to emit contact clicked signal
class ContactSignal(QObject):
    contact_clicked = pyqtSignal(dict)



class AddressBook(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Address Book")
        self.setGeometry(100, 100, 800, 600)

        # Create necessary directories if they don't exist
        self.create_directories(["contacts", "contacts_trash", "utils"])  # Added "utils" directory

        self.contact_list = QListWidget(self)
        self.init_ui()
        self.load_custom_socials()
        self.load_groups()  # Load group names

        # Create and connect the custom signal
        self.contact_signal = ContactSignal()
        self.contact_list.itemClicked.connect(self.emit_contact_clicked_signal)

    def emit_contact_clicked_signal(self, item):
        contact_data = item.data(Qt.UserRole)
        self.contact_signal.contact_clicked.emit(contact_data)

    def create_directories(self, directories):
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)


    def add_contact_item(self, contact_data):
        contact_item = QListWidgetItem(contact_data["name"])
        contact_item.setData(Qt.UserRole, contact_data)
        self.contact_list.addItem(contact_item)

    def view_address_book(self):
        dialog = AddressBookViewer(self)

        # Get the selected contact's data
        selected_item = self.contact_list.currentItem()
        if selected_item is not None:
            contact_data = selected_item.data(Qt.UserRole)
            dialog.set_contact_details(contact_data)

        dialog.exec_()

    def get_custom_fields(self):
        custom_fields = {}
        for field_title, field_info in zip(self.custom_fields_input, self.custom_fields_value_input):
            custom_fields[field_title.text()] = field_info.text()
        return custom_fields

    def init_ui(self):
        layout = QVBoxLayout()

        # Display the "Name" label without a box
        name_label = QLabel("Name:")
        layout.addWidget(name_label)

        self.contact_name_input = QLineEdit(self)
        layout.addWidget(self.contact_name_input)

        layout.addWidget(QLabel("Phone Numbers (separated by comma):"))
        self.contact_phone_input = QLineEdit(self)
        layout.addWidget(self.contact_phone_input)

        layout.addWidget(QLabel("Emails (separated by comma):"))
        self.contact_email_input = QLineEdit(self)
        layout.addWidget(self.contact_email_input)

        layout.addWidget(QLabel("Groups:"))
        self.contact_group_input = QComboBox(self)
        self.contact_group_input.addItem("No Group")  # Option for no group
        self.load_existing_groups()  # Load existing groups
        layout.addWidget(self.contact_group_input)

        self.add_group_button = QPushButton("Add New Group", self)
        self.add_group_button.clicked.connect(self.add_new_group)
        layout.addWidget(self.add_group_button)

        layout.addWidget(QLabel("Tags (separated by comma):"))
        self.contact_tags_input = QLineEdit(self)
        layout.addWidget(self.contact_tags_input)

        layout.addWidget(QLabel("Notes:"))
        self.contact_notes_input = QTextEdit(self)
        layout.addWidget(self.contact_notes_input)

        layout.addWidget(QLabel("Website:"))  # Added website field
        self.contact_website_input = QLineEdit(self)
        layout.addWidget(self.contact_website_input)

        layout.addWidget(QLabel("Custom Socials:"))  # Added label for custom socials
        self.contact_custom_social_input = QComboBox(self)
        self.load_existing_custom_socials()  # Load existing custom socials
        layout.addWidget(self.contact_custom_social_input)

        self.add_custom_social_button = QPushButton("Add Custom Social", self)
        layout.addWidget(self.add_custom_social_button)
        self.add_custom_social_button.clicked.connect(self.add_custom_social)

        # custom field
        self.custom_fields_input = []
        self.custom_fields_value_input = []
        self.custom_fields_button = QPushButton("Add Custom Field", self)
        layout.addWidget(self.custom_fields_button)

        # Connect the button to the function
        self.custom_fields_button.clicked.connect(self.add_custom_field)

        self.add_contact_button = QPushButton("Add Contact", self)
        layout.addWidget(self.add_contact_button)

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(self.scroll_area)

        self.view_contacts_button = QPushButton("View Address Book", self)
        layout.addWidget(self.view_contacts_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.add_contact_button.clicked.connect(self.add_contact)
        self.view_contacts_button.clicked.connect(self.view_address_book)

    def add_contact(self):
        name = self.contact_name_input.text()
        phone_numbers = [num.strip() for num in self.contact_phone_input.text().split(",")]
        emails = [email.strip() for email in self.contact_email_input.text().split(",")]
        group = self.contact_group_input.currentText()
        tags = [tag.strip() for tag in self.contact_tags_input.text().split(",")]
        notes = self.contact_notes_input.toPlainText()
        website = self.contact_website_input.text()  # Added website input
        custom_social = self.contact_custom_social_input.currentText()  # Added custom_social input

        # Clear the "Name" input field after extracting the value
        self.contact_name_input.clear()

        if name:
            contact = Contact(name, phone_numbers, emails, group, tags, notes, website, custom_social)
            custom_fields = self.get_custom_fields()
            contact.custom_fields.update(custom_fields)

            contact.save_as_json()
            self.add_contact_item(contact.to_json())

            QMessageBox.information(self, "Contact Added", "Contact has been added successfully.")

    def add_custom_social(self):
        custom_social, ok = QInputDialog.getText(self, "Add Custom Social", "Enter the name of the custom social:")
        if ok and custom_social:
            # Save the custom social for future use
            custom_socials_dir = "utils"
            if not os.path.exists(custom_socials_dir):
                os.makedirs(custom_socials_dir)

            custom_socials_file = os.path.join(custom_socials_dir, "custom_socials.json")
            if os.path.exists(custom_socials_file):
                with open(custom_socials_file, "r") as f:
                    custom_socials = json.load(f)
            else:
                custom_socials = []

            if custom_social not in custom_socials:
                custom_socials.append(custom_social)

                with open(custom_socials_file, "w") as f:
                    json.dump(custom_socials, f, indent=4)

                # Clear and repopulate the combo box to prevent duplicates
                self.contact_custom_social_input.clear()
                self.load_existing_custom_socials()

    def load_existing_groups(self):
        for filename in os.listdir("contacts"):
            if filename.endswith(".json"):
                contact_path = os.path.join("contacts", filename)
                with open(contact_path, "r") as f:
                    contact_data = json.load(f)
                    groups = contact_data["groups"]
                    for group in groups:
                        if group not in self.contact_group_input.currentText():
                            self.contact_group_input.addItem(group)

    def add_new_group(self):
        new_group, ok = QInputDialog.getText(self, "Add New Group", "Enter the name of the new group:")
        if ok and new_group:
            self.contact_group_input.addItem(new_group)
            self.save_group(new_group)  # Save the new group to JSON

    def load_groups(self):
        groups_file = os.path.join("utils", "groups.json")
        if os.path.exists(groups_file):
            with open(groups_file, "r") as f:
                groups = json.load(f)
                for group in groups:
                    self.contact_group_input.addItem(group)

    def save_group(self, group_name):
        groups_file = os.path.join("utils", "groups.json")
        if os.path.exists(groups_file):
            with open(groups_file, "r") as f:
                groups = json.load(f)
        else:
            groups = []

        if group_name not in groups:
            groups.append(group_name)

        with open(groups_file, "w") as f:
            json.dump(groups, f, indent=4)

    def load_existing_custom_socials(self):
        custom_socials_dir = "utils"
        if not os.path.exists(custom_socials_dir):
            os.makedirs(custom_socials_dir)

        custom_socials_file = os.path.join(custom_socials_dir, "custom_socials.json")
        if os.path.exists(custom_socials_file):
            with open(custom_socials_file, "r") as f:
                custom_socials = json.load(f)
                for social in custom_socials:
                    self.contact_custom_social_input.addItem(social)

    def load_custom_socials(self):
        custom_socials_dir = "utils"
        if not os.path.exists(custom_socials_dir):
            os.makedirs(custom_socials_dir)

        custom_socials_file = os.path.join(custom_socials_dir, "custom_socials.json")
        if os.path.exists(custom_socials_file):
            with open(custom_socials_file, "r") as f:
                custom_socials = json.load(f)
                for social in custom_socials:
                    self.contact_custom_social_input.addItem(social)


# custom field
    def add_custom_field(self):
        field_title, ok = QInputDialog.getText(self, "Add Custom Field", "Enter the title of the custom field:")
        if ok and field_title:
            # Prompt the user for additional information if needed
            field_info, ok = QInputDialog.getText(self, "Add Custom Field", f"Enter additional information for '{field_title}':")
            if ok:
                # Create a dictionary to store custom field definition
                custom_field = {"title": field_title, "info": field_info}

                # Save the custom field definition as a JSON file in the "utils" directory
                custom_fields_dir = "utils"
                if not os.path.exists(custom_fields_dir):
                    os.makedirs(custom_fields_dir)

                custom_field_file = os.path.join(custom_fields_dir, f"{field_title}.json")
                with open(custom_field_file, "w") as f:
                    json.dump(custom_field, f, indent=4)

                # Display a message to inform the user
                QMessageBox.information(self, "Custom Field Added", "Custom field has been added successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddressBook()
    window.show()
    sys.exit(app.exec_())
