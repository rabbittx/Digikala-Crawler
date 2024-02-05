import configparser
import os

class ConfigManager:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Load configuration from file, create with defaults if not exist."""
        if not os.path.exists(self.config_file):
            self._create_default_config()
        else:
            self.config.read(self.config_file)

    def _create_default_config(self):
        """Create a default configuration file with initial settings."""
        self.config['Setting'] = {
            'DriverType': 'firefox',  # Default to firefox
            'HeadlessMode': 'false'  # Default to non-headless mode
        }
        self.config['Paths'] = {
            'GeckoPath': '',  # Empty by default
            'DBPath': ''  # Empty by default
        }
        self.save_config()

    def get_setting(self, section, setting):
        """Retrieve a specific setting from config."""
        return self.config.get(section, setting)

    def set_setting(self, section, setting, value):
        """Set a specific setting in config."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][setting] = value
        self.save_config()

    def save_config(self):
        """Write the current configuration to file."""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    # Example usage methods
    def get_driver_type(self):
        return self.get_setting('Setting', 'DriverType')
    
    def set_driver_type(self, driver_type):
        self.set_setting('Setting', 'DriverType', driver_type)
    
    def get_headless_mode(self):
        return self.config.getboolean('Setting', 'HeadlessMode')
    
    def set_headless_mode(self, headless):
        self.set_setting('Setting', 'HeadlessMode', str(headless).lower())
