import ConfigParser
import os
import sys
import logging

class Config(object):
    """
    Class for reading global configuration file

    methods:
    - Read      : Reading for configuration file
    - Getoption : Getting and setting options.
    
    """
    @classmethod
    def __init__(self, configFile):
        self.log = logging.getLogger(__name__)
        self.cfg = ConfigParser.RawConfigParser()
        try:
            self.log.info('Reading configuration file')
            if configFile and os.R_OK:
                self.Read(configFile)
        except IOError as io_err:
            self.log.error("Configuration file cannot be read: %s", io_err)
        
        # Example option for main with default value which isn't required 
        #self.main_first_arg = self.Getoption('main', 'option1', None, '', False)       
        
        # Example option for main with default value which is required 
        self.main_sec_opt = self.Getoption('main', 'option2', None, 'argument1', True)       

    @classmethod
    def Read(self, conf):
        """Open config file and try to parse"""
        if os.path.isfile(conf):
            try:
                self.cfg.readfp(open(conf))
            except self.cfg.ParsingError as parse_err:
                self.log.debug("Parsing error %s", parse_err, exc_info=True)
                return False
        else:
            self.log.debug("Cannot open file %s", conf, exc_info=True)
            return False
        return True
    
    @classmethod
    def Getoption(self, section, option, var, default, required):
        """ 
        Get from defined sections all the defined options 
        if option is not defined set default value. 
        """ 
        try:
            try:
                var = self.cfg.get(section, option)
                # If option is not set then the default setting will be replace the empty variable
                if not var and not default and not required:
                    self.log.warn('Skipping non required option [%s] in section [%s] defined without default', 
                                option, section)
                elif not var and default and required: 
                    var = self.cfg.set(section, option, default)
                    self.log.debug('Option [%s] in section [%s] to: %s (default)', option, section, default)
                elif not var and not default and required: 
                    self.log.error('Required option [%s] in section [%s] is undefined and missing defined default',
                                option, section)
                else:
                    self.log.debug('Setting option [%s] in section [%s] to: %s', option, section, var)
            #except ConfigParser.NoOptionError, opt_err:
            except ConfigParser.NoOptionError:
                self.log.error('Failed to find option [%s]', option, exc_info=True)
        except ConfigParser.NoSectionError:
            self.log.error('Failed to find section [%s]', section, exc_info=True)
        return var 
