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

PROGNAME = os.path.basename(__file__)
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
        self.verbose = False
        """ 
        Parsing cli options
    
        The following arguments will be accepted:
            - '-C' or '--conf='         : Location of configuration file.
            - '--help'                  : Print usage 
            - '--version'               : Print version 

        Mandatory: env and datasource(s) or workbook(s)
        """ 
        self.configfile = PROGNAME + ".conf"

        try:
            opts, args = getopt.getopt(args, ':C:vV',
                                       ('conf=', 'help', 'version', 'verbose'))
        except getopt.error as go_err:
            print go_err
            sys.exit(1)

        for opt, arg in opts:
            if opt in ('-C', '--config'):
                self.configfile = os.path.abspath(arg)
            elif opt == '--help':
                self.Usage()
                sys.exit(0)
            elif opt in ('-v', '--verbose'):
                self.verbose = True
            elif opt in ('-V', '--version'):
                self.Version()
                sys.exit(0)

        if not self.env:
            self.Usage()
            sys.exit(1)

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
        self.env = op.env
        self.proj_customer = ""

        try:
            if op.configfile and os.R_OK:
                self.Read(op.configfile)
        except IOError as io_err:
            log.error("Configuration file cannot be read: %s", io_err)
            sys.exit(1)
        
        # Customer definition
        self.main_arg = self.Getoption('main', 'argument', None, '')       
        self.env_arg = self.Getoption(self.env, 'dbuser', None, '')

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
    def Getoption(self, section, option, var, default):
        """
        Get all options from defined sections 
        if option is not defined set default value. 
        """
        try:
            var = self.cfg.get(section, option)
            # If option is not set then the default setting will be replace the empty variable
            if not var:
                var = self.cfg.set(section, option, default)
                log.debug('Option %s in section [%s] to: %s (default)', option, section, default)
            else:
                log.debug('Setting option %s in section [%s] to: %s', option, section, var)
        except ConfigParser.NoSectionError, sect_err:
            log.error('Failed to find section [%s]', section)
            raise LookupError(sect_err)
        return var
    
def main():
    """
    After parsing CLI arguments the following steps will be done
    - Configuration file progname.conf will be parsed and arguments will be loaded
    """
    
    log.info('Reading configuration file')
    cf = Config()

if __name__ == '__main__':
    """
    - The commandline arguments are passed to the Options class
    - Initialization of the logger
    - Printing first line with the following:
        - Progname 
        - Version 
        - Hardware platform 
        - Python version 
        
    Example of print: progname.py-0.1 running on Python version: 2.7.10-x86_64 on Linux
    """
    op = Options(sys.argv[1:])
    # Location of logging.ini
    logging.config.fileConfig("logging.ini")
    log = logging.getLogger(PROGNAME)
    log.debug('Initializing logger')
    log.info('%s Version %s running on Python version: %s-%s on %s',
              PROGNAME, VERSION, platform.python_version(), platform.machine(), platform.system())
    main()
