import configparser
import os

class ConsoleConfigManager:

    """
     config  manager class to handle the configuration file.
    
    """
    def __init__(self, log, config_file='console-config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.log = log
        if not self.config.read(self.config_file):
            self._create_default_config()

    def _create_default_config(self):
        """
         create a default configuration file with necessary information.
         
        return: None

        """

        self.log.info('Pick driver type .')
        self.log.info('1) firefox .')
        self.log.info('2) chrome .')
        self.log.info('choose "1" for FireFox and "2" for Chrome.')
        while  True:
            driver_type = input('chose the driver type : ')
            if driver_type == '1':
                driver_type = 'firefox'
            elif driver_type == '2':
                driver_type = 'chrome'
            else :
                self.log.error('[-] ERROR - invalid  choice ! \n please chose again .\n')
            break
        headless_mode = input('Enable headless mode? (yes/no): ')
        headless_mode = 'True' if headless_mode.lower() in ['yes', 'y'] else 'False'
        
        self.config['Setting'] = {'Drivertype': driver_type, 'HeadlessMode': headless_mode}
        self.config['Paths'] = {'GeckoPath': input('Enter path of Gecko driver (eq:path/to/geckodriver.exe): '), 'DBPath': input('Enter path to database (eq:path/to/database.db) :')}
        self.log.info('--------------------------------- CONFIG COMPLATED ---------------------------------------')
        self.log.info(f"you have  chosen {driver_type}, Headless Mode is set as {headless_mode}")
        self.log.info(f"also set database path in {self.config['Paths']['DBPath']}")
        self.log.info(f"also set Gecko driver path in {self.config['Paths']['GeckoPath']}")
        self.log.info(f"you can reconfig crawler at any time you want from meun .")
        self.log.info('------------------------------------------------------------------------')

        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

            
    def get_headless_mode(self):
        """
        Get headless mode setting from the configuration file.
        
        :return: bool - True if headless mode is enabled, False otherwise.
        """
        return self.config.getboolean('Setting', 'HeadlessMode', fallback=False)

    def set_headless_mode(self, mode):
        """
        Set headless mode in the configuration file.
        
        :param mode: bool - True to enable headless mode, False to disable it.
        """
        self.config.set('Setting', 'HeadlessMode', str(mode).lower())
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_driver_type(self):
        """
        get  the driver type from the configuration file.
        
        """
        return self.config.get('Setting', 'Drivertype')
    
    def set_driver_type(self):
        """
        set the  driver type to the configuration file.
        
        """
        self.config.set('Setting', 'Drivertype')
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_gecko_path(self):
        """
         Get geckodriver path from the configuration file.
        
        """
        return self.config.get('Paths', 'GeckoPath')

    def get_db_path(self):
        """
         Get database file path from the configuration file.
        
        """
        return self.config.get('Paths', 'DBPath')

    def set_gecko_path(self, path):
        """
         Set geckodriver path in the configuration file.
        
        :param path: str - The path of Geckodriver.
        
        """
        self.config.set('Paths', 'GeckoPath', path)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def set_db_path(self, path):
        """
         Set database file path in the configuration file.
        
        :param path: str - The path to save the SQLite3 database file.
        
        """
        self.config.set('Paths', 'DBPath', path)
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)



class WebConfigManager:
    def __init__(self, log, config_file='web_config.ini'):
        self.log = log
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        """Load configuration from file, create with defaults if not exist."""
        if not os.path.exists(self.config_file):
            self.log.info('[+] Config not found, ready to create...')
            self._create_default_config()
            self.log.info('[+] Config created successfully.')
        else:
            self.config.read(self.config_file)
            self.log.info('[+] Config loaded successfully.')

    def _create_default_config(self):
        """Create a default configuration file with initial settings."""
        self.config['Setting'] = {
            'Drivertype': '',  
            'HeadlessMode': 'False'  
        }
        self.config['Paths'] = {
            'GeckoPath': '',  # Empty by default
            'DBPath': 'archive/dataBase/digikala_database.db'  # Example path
        }
        self.save_config()
        self.log.info('[+] Config saved successfully.')

    def get_setting(self, section, setting):
        """Retrieve a specific setting from config."""
        try:
            return self.config.get(section, setting)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            self.log.error(f"Error retrieving setting: {e}")
            return None

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
        self.log.info('[+] Config saved.')

    def get_driver_type(self):
        return self.get_setting('Setting', 'Drivertype')
    
    def set_driver_type(self, driver_type):
        self.set_setting('Setting', 'Drivertype', driver_type)
    
    def get_db_path(self):
        return self.get_setting('Paths', 'DBPath')
    
    def get_headless_mode(self):
        return self.config.getboolean('Setting', 'HeadlessMode')
    
    def set_headless_mode(self, headless):
        self.set_setting('Setting', 'HeadlessMode', str(headless).lower())

    def get_gecko_path(self):
        return self.get_setting('Paths', 'GeckoPath')
    
    def set_gecko_path(self, path):
        self.set_setting('Paths', 'GeckoPath', path)
