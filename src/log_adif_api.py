##############################################################################
# log_adif_api.py
#
# API for logging data to an ADIF file.
# Designed for use by the AB3GY POTA spot application.
##############################################################################

# System packages.
from datetime import datetime, timezone
from pathlib import Path
import time

# Local packages.
import lib.adif as adif

##############################################################################
# Globals.
############################################################################## 
adif_filename = None


##############################################################################
# Functions.
############################################################################## 

#-----------------------------------------------------------------------------
def init_api(filename):
    """
    Initialize the ADIF logging api.
    """
    global adif_filename
    if (len(filename) > 0):
        adif_filename = Path(filename)
        if not adif_filename.exists():
            with open(adif_filename, 'a') as f:
                header='potarig log file <eoh>\n'
                try:
                    f.write(header)
                except Exception as err:
                    print('ADIF file create error: {}'.format(str(err)))
        

#-----------------------------------------------------------------------------
def log_data(call, freq, mode, ref, name):
    """
    Create an ADIF record and save it to the log file.
    """
    global adif_filename
    if adif_filename is not None:
        if (len(freq) > 0):
            freq_mhz = float(freq) * 0.001
            band = adif.freq2band(freq_mhz)
            freq_mhz = str(freq_mhz)
        else:
            freq_mhz = ''
            band = ''
        now = datetime.now(timezone.utc)
        comment = '{} {}'.format(ref, name)
        qso_date = now.strftime("%Y%m%d")
        qso_time = now.strftime("%H%M")
        my_adif = adif.adif()
        my_adif.set_field('CALL', call)
        my_adif.set_field('BAND', band)
        my_adif.set_field('FREQ', freq_mhz)
        my_adif.set_field('MODE', mode)
        my_adif.set_field('QSO_DATE', qso_date)
        my_adif.set_field('TIME_ON', qso_time)
        my_adif.set_field('COMMENT', comment)
        with open(adif_filename, 'a') as f:
            try:
                f.write('{}\n'.format(my_adif.get_adif(sort=False)))
            except Exception as err:
                print('ADIF file write error: {}'.format(str(err)))


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    import os
    import sys
    print('{} main program called'.format(os.path.basename(sys.argv[0])))
    
    