import json
from advanced import AdvancedSettings
from start import start_application

class Scheduler:
    def __init__(self, settings_file='settings.json'):
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_settings(self):
        with open(self.settings_file, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def run(self):
        advanced_settings = AdvancedSettings(self.settings)
        advanced_settings.display_settings()
        start_application(self)

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()