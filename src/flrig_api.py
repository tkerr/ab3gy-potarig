##############################################################################
# flrig_api.py
#
# A flrig interface for the AB3GY POTA spot application.
# FLRIG references:
#    http://www.w1hkj.com/
#    http://www.w1hkj.com/flrig-help/
##############################################################################

# Local packages.
import lib.FlrigClient as FlrigClient
import lib.Logger as log

##############################################################################
# Globals.
############################################################################## 
DEFAULT_SERVER_URL = 'http://localhost:12345'
flrig_client = None
modes_map = {}


##############################################################################
# Functions.
############################################################################## 

#-----------------------------------------------------------------------------
def client_init(server_url=DEFAULT_SERVER_URL):
    """
    Initialize the FlrigClient object.
    """
    global flrig_client
    flrig_client = FlrigClient.FlrigClient(server_url)

#-----------------------------------------------------------------------------
def set_modes(modes_dict):
    """
    Initialize the FlrigClient object.
    """
    global modes_map
    for k,v in modes_dict.items():
        modes_map[k.upper()] = v.upper()

#-----------------------------------------------------------------------------
def set_xcvr(mode, freq):
    """
    Set transcriver mode and frequency.
    """
    global flrig_client
    global modes_map

    if (len(freq) > 0):
        freq_hz = float(freq) * 1000.0
    else:
        freq_hz = 0.0
    
    mode = mode.upper()
    if (mode == 'PHONE') or (mode == 'SSB'):
        if (freq_hz < 9000000):
            mode = 'LSB'
        else:
            mode = 'USB'
    if mode in modes_map.keys():
        xcvr_mode = modes_map[mode]
    else:
        xcvr_mode = mode
    
    if flrig_client is not None:
        # Set the frequency first in case this causes a band change.
        if (freq_hz > 0.0): flrig_client.set_vfo(freq_hz)
        if (len(xcvr_mode) > 0): flrig_client.set_mode(xcvr_mode)
        
        # Check frequency in case a mode change altered it.
        set_freq = flrig_client.get_vfo()
        if (len(set_freq) > 0) and (freq_hz > 0.0):
            f_set_freq = float(set_freq)
            if (f_set_freq != freq_hz):
                flrig_client.set_vfo(freq_hz)
    
        if log.logger is not None:
            msg =  'Mode: {} '.format(flrig_client.get_mode())
            msg += 'VFO: {}'.format(flrig_client.get_vfo())
            log.logger.print_and_log(msg)


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    import os
    import sys
    print('{} main program called'.format(os.path.basename(sys.argv[0])))
    
    