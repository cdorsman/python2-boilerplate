#!/usr/bin/env python
"""
Progname is a tool for ...
"""

import sys
import platform
import os
import os.path
import getopt

import ConfigParser
import logging
import logging.config
import logging.handlers

# The PROGNAME global is how you want to name your script. 
# Once PROGNAME is set, the script will look for configfile called PROGNAME.conf
# If you want to name the program as the filename but without the '.py' extension.
PROGNAME = os.path.basename(__file__).rstrip('.py')
# If you want to set a custom name:
#PROGNAME = "progname"

LOGGERNAME = PROGNAME.title()
VERSION = "0.1"

class Options(object):
    """
    Class for parsing and handling CLI options
    
    Methods:
    - Usage     : Print the usage message
    - Version   : Print version 
    """

    @classmethod
    def __init__(self, args):
        """ 
        Parsing cli options
    
        The following arguments will be accepted:
            - '-C' or '--conf='         : Location of configuration file.
            - '--help'                  : Print usage 
            - '--version'               : Print version 
        """ 
        self.configfile = PROGNAME + ".conf"
        self.logconffile = "./logging.ini"

        try:
            opts, args = getopt.getopt(args, ':C:vV',
                                       ('config=', 'help', 'version', 'verbose'))
        except getopt.error as go_err:
            print go_err
            sys.exit(1)

        for opt, arg in opts:
            if opt in ('-C', '--config'):
                self.configfile = os.path.abspath(arg)
            elif opt == '--help':
                self.Usage()
                sys.exit(0)
            elif opt ==  '--version':
                self.Version()
                sys.exit(0)

    @classmethod
    def Version(self):
        """Print version"""
        print "Version: %s" % VERSION

    @classmethod
    def Usage(self):
        """Print usage"""
        print "Usage: %s" % PROGNAME
        print "    %s -h: Help" % PROGNAME

class Config(object):
    """
    Class for reading global configuration file

    methods:
    - Read      : Reading for configuration file
    - Getoption : Getting and setting options.
    
    """
    @classmethod
    def __init__(self):
        self.cfg = ConfigParser.RawConfigParser()

        try:
            log.info('Reading configuration file')
            if op.configfile and os.R_OK:
                self.Read(op.configfile)
        except IOError as io_err:
            log.error("Configuration file cannot be read: %s", io_err)
            sys.exit(1)
        
        # Example option for main with default value which isn't required 
        #self.main_first_arg = self.Getoption('main', 'option1', None, '', False)       
        
        # Example option for main with default value which is required 
        self.main_sec_opt = self.Getoption('main', 'option2', None, 'argument1', True)       

    @classmethod
    def Read(self, configfile):
        """Open config file and try to parse"""
        if os.path.isfile(configfile):
            try:
                self.cfg.readfp(open(configfile))
            except self.cfg.ParsingError as parse_err:
                log.debug("Parsing error %s", parse_err)
                sys.exit(1)
        else:
            log.debug("Cannot open file %s", configfile)
            sys.exit(1)
    
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
                    log.warn('Skipping non required option [%s] in section [%s] defined without default', 
                                option, section)
                elif not var and default and required: 
                    var = self.cfg.set(section, option, default)
                    log.debug('Option [%s] in section [%s] to: %s (default)', option, section, default)
                elif not var and not default and required: 
                    log.error('Required option [%s] in section [%s] is undefined and missing defined default',
                                option, section)
                    sys.exit(1)
                else:
                    log.debug('Setting option [%s] in section [%s] to: %s', option, section, var)
            except ConfigParser.NoOptionError, opt_err:
                log.error('Failed to find option [%s]', option)
                raise LookupError(opt_err)
        except ConfigParser.NoSectionError, sect_err:
            log.error('Failed to find section [%s]', section)
            raise LookupError(sect_err)
        return var 
    
def main():
    """
    After CLI arguments the following steps will be done
    - Configfile PROGNAME.conf will be parsed.
    """
    
    cf = Config()
    print "Main"

if __name__ == '__main__':
    """
    - CLI arguments are parsed in Options class
    - Printing first line with script info with the following:
        - Progname 
        - Version 
        - Hardware platform 
        - Python version 
    """

    op = Options(sys.argv[1:])
    # Location of logging.ini
    logging.config.fileConfig(op.logconffile)
    log = logging.getLogger(LOGGERNAME)
    log.debug('%s-%s running on Python version: %s-%s on %s',
              LOGGERNAME, VERSION, platform.python_version(), 
              platform.machine(), platform.system())
    main()
