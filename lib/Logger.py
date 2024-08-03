# Logger.py
# Simple logger class for application logging.

# System packages.
import os
import time
import logging

##############################################################################
# Globals.
##############################################################################

# Global Logger object for use by an application.
logger = None

##############################################################################
# Functions.
##############################################################################

##############################################################################
# Logger class.
##############################################################################
# ----------------------------------------------------------------------
class Logger(object):
    """
    Simple logger class for application logging.
    """
    # ------------------------------------------------------------------
    def __init__(self, logfile, default_level=logging.INFO):
        """
        Class constructor.
        Parameters:
            logfile (str) : The log file name.
            default_level (int) : The default logging level, defaults to INFO.
        """
        logger_name = os.path.basename(os.path.splitext(logfile)[0])
        logging.basicConfig(filename=logfile, level=default_level)
        self.logfile = logfile
        self.logger = logging.getLogger(logger_name)

    # ------------------------------------------------------------------
    def __del__(self):
        """
        Class destructor.
        """
        self.close()
    
    # ----------------------------------------------------------------------
    def log_msg(self, msg, level=logging.INFO):
        """
        Log a timestamped message to the log file.
        Parameters:
            msg : (str) The message to print and log.
            level : (int) The logging level, defaults to INFO.
        Returns:
            None
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S ', time.gmtime())
        logmsg = timestamp + str(msg)
        self.logger.log(level, logmsg)
        
    # ----------------------------------------------------------------------
    def print_and_log(self, msg, level=logging.INFO):
        """
        Print a timestamped message and also log it to the log file.
        Parameters:
            msg : (str) The message to print and log.
            level : (int) The logging level, defaults to INFO.
        Returns:
            None
        """
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S ', time.gmtime())
        logmsg = timestamp + str(msg)
        print(logmsg)
        self.logger.log(level, logmsg)

    # ----------------------------------------------------------------------
    def close(self):
        """
        Shut down the logger.
        """
        logging.shutdown()

