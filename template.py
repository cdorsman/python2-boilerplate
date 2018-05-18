#!/usr/bin/env python
"""
Progname is a tool for ...
"""

import sys
import platform
import os
import os.path
import getopt

import logging
import logging.config
import logging.handlers

from config import *

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

def main():
    """
    After CLI arguments the following steps will be done
    - Configfile PROGNAME.conf will be parsed.
    """
    
    cf = Config(op.configfile)
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
