import ConfigParser

class Config():
    """ Read and write a Config file
    
    """
    
    def __init__(self, filename = 'Settings.ini'):
        """ Pick config file
        
        filename (str): complete file path to config file
        
        """
        self.cfg = ConfigParser.ConfigParser() #Wichtig!
        #self.cfg.read(str(filename))
        self.filename = filename

        #cfg.add_section('FlameParameters')
        #cfg.set('FlameParameters', 'Flammenhoehe', '200')
        #cfg.set('FlameParameters', 'Nullpunkt', '100')
        #cfgfile = open('Settings.txt', 'w')
        #cfg.write(cfgfile)
        #cfgfile.close()
        

    def getConfigOptions(self, section):
        """ Get selected section from config file
        
        section (str): Name of config section
        
        Returns:
            section dictionary (dict)
            
        """
        cfgdict = {}
        self.cfg.read(self.filename)
        options = self.cfg.options(section)
        for option in options:
            try:
                cfgdict[option] = self.cfg.get(section, option)
            except:
                print("exception on %s!" % option)
        self.cfgdict = cfgdict


    def writeConfigOptions(self, section, cfgdict):
        """ Write given dictionary as given section to config file
        
        section (str): Name of section
        cfgdict (dict): Dictionary
        
        """
        cfgfile = open(self.filename, 'w')
        for key, value in cfgdict.items():
            self.cfg.set(section, key, value) 
        self.cfg.write(cfgfile)
        cfgfile.close()
"""
config = Config('Settings.txt')
config.getConfigOptions('FlameParameters')
cfgdict =  getattr(config, 'cfgdict')
print cfgdict
config.writeConfigOptions('FlameParameters', cfgdict)

cfg = Config('Settings.txt')
cfg.getConfigOptions('FlameParameters')
settings = getattr(cfg, 'cfgdict')
print settings
"""
