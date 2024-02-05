class ConfigManager:
    # TODO add more setting 
    # TODO add config
    # TODO optimize code 
    """
     config  manager class to handle the configuration file.
    
    """
    def __init__(self, log, config_file='config.ini'):
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
        while  True:
            driver_type = input('chose the driver type : ')
            if driver_type == '1':
                driver_type = 'firefox'
            elif driver_type == '2':
                driver_type = 'chrome'
            else :
                self.log.error('[-] ERROR - invalid  choice ! \n please chose again .\n')
            break
        self.config['Setting'] = {'DriverTpye' : driver_type}
        self.config['Paths'] = {'GeckoPath': input('Enter path of Gecko driver (eq:path/to/geckodriver.exe): '), 'DBPath': input('Enter path to database (eq:path/to/database.db) :')}
        
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)


    def get_driver_type(self):
        """
        get  the driver type from the configuration file.
        
        """
        return self.config.get('Setting', 'DriverTpye')
    
    def set_driver_type(self):
        """
        set the  driver type to the configuration file.
        
        """
        self.config.set('Setting', 'DriverTpye')
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

