import json

class Setup:
    def __init__(self):
        self.settings_file = "settings.json"
        self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, "r") as f:
                settings_data = json.load(f)
                self.show_live_gen = settings_data.get("show_live_gen", False)
        except FileNotFoundError:
            self.show_live_gen = False

    def save_settings(self):
        settings_data = {
            "show_live_gen": self.show_live_gen
        }
        with open(self.settings_file, "w") as f:
            json.dump(settings_data, f)

    def is_live_gen_enabled(self):
        return self.show_live_gen

    def set_live_gen_enabled(self, value):
        self.show_live_gen = value
        self.save_settings()
