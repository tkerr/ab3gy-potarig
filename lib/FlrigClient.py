###############################################################################
# FlrigClient.py
# Author: Tom Kerr AB3GY
#
# FlrigClient class.
# Implements an xmlrpc client to communicate with a flrig server.
# flrig is a rig control program that cooperates with fldigi, wsjt-x, and
# other amateur radio applications.
#
# W1HKJ software main page: http://www.w1hkj.com/
# FLRig Users Manual: http://www.w1hkj.com/flrig-help/index.html
# Supported commands: http://www.w1hkj.com/flrig-help/xmlrpc_commands.html
#
# Designed for personal use by the author, but available to anyone under the
# license terms below.
###############################################################################

###############################################################################
# License
# Copyright (c) 2024 Tom Kerr AB3GY (ab3gy@arrl.net).
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,   
# this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,  
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
###############################################################################

# System level packages.
import time
import xmlrpc.client

# Local packages.


##############################################################################
# Globals.
##############################################################################


##############################################################################
# Functions.
##############################################################################

    
##############################################################################
# FlrigClient class.
##############################################################################
class FlrigClient(object):
    """
    FlrigClient class.
    Implements an xmlrpc client to communicate with a flrig server.
    """
    # ------------------------------------------------------------------------
    def __init__(self, server_url=''):
        """
        Class constructor.
        
        Parameters
        ----------
        server_url : str
            The flrig server url.
            
        Returns
        -------
        None.
        """
        self.server_url = server_url
        self.server = None
        self.errmsg = ''
        if (len(server_url) > 0):
            self.create_server_proxy(server_url)
    
    # ------------------------------------------------------------------------
    def _string_cmd(self, func, val=None):
        """
        Execute an FLRig command and return a string response.
        
        Parameters
        ----------
        func : function
            A FLRig xmlrpc command to execute, format = self.server.xxx
        val : function argument
            An optional FLRig command argument; type must match expected type for the command
        
        Returns
        -------
        resp : str
            A string command execution response
        self.errmsg is empty if successful, or contains an error message if failed.
        """
        resp = ''
        if self.server is not None:
            try:
                if val is None:
                    resp = str(func())
                else:
                    resp = str(func(val))
                self.errmsg = ''
            except Exception as err:
                self.errmsg = str(err)
                print('flrig error: {}'.format(self.errmsg))
        else:
            self.errmsg = 'Server proxy is not defined'
            print('flrig error: {}'.format(self.errmsg))
        return resp
    
    # ------------------------------------------------------------------------
    def _list_cmd(self, func, val=None):
        """
        Execute an FLRig command and return a list response.
        
        Parameters
        ----------
        func : function
            A FLRig xmlrpc command to execute, format = self.server.xxx
        val : function argument
            An optional FLRig command argument; type must match expected type for the command
        
        Returns
        -------
        resp : list
            A list command execution response
        self.errmsg is empty if successful, or contains an error message if failed.
        """
        resp = ''
        if self.server is not None:
            try:
                if val is None:
                    resp = list(func())
                else:
                    resp = list(func(val))
                self.errmsg = ''
            except Exception as err:
                self.errmsg = str(err)
                print('flrig error: {}'.format(self.errmsg))
        else:
            self.errmsg = 'Server proxy is not defined'
            print('flrig error: {}'.format(self.errmsg))
        return resp

    # ------------------------------------------------------------------------
    def create_server_proxy(self, url):
        """
        Create an xmlrpc server proxy for FLRig.
        
        Parameters
        ----------
        url : str
            The FLRig server URL.
        
        Returns
        -------
        self.errmsg is empty if successful, or contains an error message if failed.
        """
        try:
            self.server = xmlrpc.client.ServerProxy(url)
            self.errmsg = ''
        except Exception as err:
            self.server = None
            self.errmsg = str(err)
            print('Error creating flrig server proxy {}: {}'.format(url, self.errmsg))

    # ------------------------------------------------------------------------
    def cat_string(self, val):
        """
        Send a CAT string to the transceiver and return the response.
        """
        return self._string_cmd(self.server.rig.cat_string, str(val))

    # ------------------------------------------------------------------------
    def get_AB(self):
        """
        Return the VFO in use (A/B)
        """
        return self._string_cmd(self.server.rig.get_AB)

    # ------------------------------------------------------------------------
    def get_bw(self):
        """
        Return the current VFO bandwidth.
        NOTE: Returns a list.
        """
        return self._list_cmd(self.server.rig.get_bw)
    
    # ------------------------------------------------------------------------
    def set_bw(self, val):
        """
        Set bandwidth to the nearest requested value.
        """
        return self._string_cmd(self.server.rig.set_bandwidth, int(val))
    
    # ------------------------------------------------------------------------
    def get_bwA(self):
        """
        Return bandwidth of VFO A.
        NOTE: Returns a list.
        """
        return self._list_cmd(self.server.rig.get_bwA)
    
    # ------------------------------------------------------------------------
    def get_bwB(self):
        """
        Return bandwidth of VFO B.
        NOTE: Returns a list.
        """
        return self._list_cmd(self.server.rig.get_bwB)
    
    # ------------------------------------------------------------------------
    def get_bws(self):
        """
        Return a list of VFO bandwidth values.
        """
        return self._list_cmd(self.server.rig.get_bws)
    
    # ------------------------------------------------------------------------
    def get_info(self):
        """
        Return the transceiver info string.
        """
        return self._string_cmd(self.server.rig.get_info)

    # ------------------------------------------------------------------------
    def get_mode(self):
        """
        Return the mode of the current VFO.
        """
        return self._string_cmd(self.server.rig.get_mode)
    
    # ------------------------------------------------------------------------
    def set_mode(self, val):
        """
        Set the mode of the current VFO in accordance with the mode table.
        """
        return self._string_cmd(self.server.rig.set_mode, str(val))
    
    # ------------------------------------------------------------------------
    def get_modeA(self):
        """
        Return the mode of VFO A.
        """
        return self._string_cmd(self.server.rig.get_modeA)
    
    # ------------------------------------------------------------------------
    def set_modeA(self, val):
        """
        Set the mode VFO A in accordance with the mode table.
        """
        return self._string_cmd(self.server.rig.set_modeA, str(val))
    
    # ------------------------------------------------------------------------
    def get_modeB(self):
        """
        Return the mode of VFO B.
        """
        return self._string_cmd(self.server.rig.get_modeB)
    
    # ------------------------------------------------------------------------
    def set_modeB(self, val):
        """
        Set the mode VFO B in accordance with the mode table.
        """
        return self._string_cmd(self.server.rig.set_modeB, str(val))

    # ------------------------------------------------------------------------
    def get_modes(self):
        """
        Return a list of MODE values.
        """
        return self._list_cmd(self.server.rig.get_modes)
    
    # ------------------------------------------------------------------------
    def get_power(self):
        """
        Return the power level.
        """
        return self._string_cmd(self.server.rig.get_power)
    
    # ------------------------------------------------------------------------
    def set_power(self, val):
        """
        Set the power level in watts.
        """
        return self._string_cmd(self.server.rig.set_power, int(val))
    
    # ------------------------------------------------------------------------
    def get_maxpower(self):
        """
        Return the maximum power level available.
        """
        return self._string_cmd(self.server.rig.get_maxpwr)
        
    # ------------------------------------------------------------------------
    def get_ptt(self):
        """
        Return the PTT state (1 = on, 0 = off).
        """
        return self._string_cmd(self.server.rig.get_ptt)
    
    # ------------------------------------------------------------------------
    def set_ptt(self, val):
        """
        Set the PTT state (1 = on, 0 = off).
        """
        return self._string_cmd(self.server.rig.set_ptt, int(val))
    
    # ------------------------------------------------------------------------
    def get_split(self):
        """
        Return the split state (1 = on, 0 = off).
        """
        return self._string_cmd(self.server.rig.get_split)
    
    # ------------------------------------------------------------------------
    def set_split(self, val):
        """
        Set the split state (1 = on, 0 = off).
        """
        return self._string_cmd(self.server.rig.set_split, int(val))

    # ------------------------------------------------------------------------
    def get_version(self):
        """
        Return the FLRig version string.
        """
        return self._string_cmd(self.server.main.get_version)
        
    # ------------------------------------------------------------------------
    def get_vfo(self):
        """
        Return the current VFO frequency in Hz.
        """
        return self._string_cmd(self.server.rig.get_vfo)
    
    # ------------------------------------------------------------------------
    def set_vfo(self, val):
        """
        Set the current VFO frequency in Hz.
        """
        return self._string_cmd(self.server.rig.set_vfo, float(val))
    
    # ------------------------------------------------------------------------
    def get_vfoA(self):
        """
        Return the VFO A frequency in Hz.
        """
        return self._string_cmd(self.server.rig.get_vfoA)
    
    # ------------------------------------------------------------------------
    def set_vfoA(self, val):
        """
        Set the VFO A frequency in Hz.
        """
        return self._string_cmd(self.server.rig.set_vfoA, float(val))
    
    # ------------------------------------------------------------------------
    def get_vfoB(self):
        """
        Return the VFO B frequency in Hz.
        """
        return self._string_cmd(self.server.rig.get_vfoB)
    
    # ------------------------------------------------------------------------
    def set_vfoB(self, val):
        """
        Set the VFO B frequency in Hz.
        """
        return self._string_cmd(self.server.rig.set_vfoB, float(val))
    
    # ------------------------------------------------------------------------
    def get_xcvr(self):
        """
        Return the transceiver name.
        """
        return self._string_cmd(self.server.rig.get_xcvr)
    
    # ------------------------------------------------------------------------
    def swap(self):
        """
        Execute VFO swap.
        """
        self._string_cmd(self.server.rig.swap)
        time.sleep(1.0) # Delay for transceiver CAT commands to execute
        return ''
    

##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    import sys
    
    url = ''
    vfo = 0
    
    # Arg 1 is the FLRig server URL.
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    # Arg 2 is the VFO frequency to set.
    if len(sys.argv) > 2:
        vfo = int(sys.argv[2])
        
    if (len(url) > 0):
        client = FlrigClient(url)
    else:
        client = FlrigClient()
    
    print(sorted(client.server.system.listMethods()))
    print('flrig server URL = {}'.format(client.server_url))
    print('version = {}'.format(client.get_version()))
    print('xcvr    = {}'.format(client.get_xcvr()))
    print('modes   = {}'.format(client.get_modes()))
    print('mode    = {}'.format(client.get_mode()))
    print('mode-A  = {}'.format(client.get_modeA()))
    print('mode-B  = {}'.format(client.get_modeB()))
    print('VFO A/B = {}'.format(client.get_AB()))
    print('VFO     = {}'.format(client.get_vfo()))
    print('VFO-A   = {}'.format(client.get_vfoA()))
    print('VFO-B   = {}'.format(client.get_vfoB()))
    print('split   = {}'.format(client.get_split()))
    print('BWs     = {}'.format(client.get_bws()))
    print('BW      = {}'.format(client.get_bw()))
    print('BW-A    = {}'.format(client.get_bwA()))
    print('BW-B    = {}'.format(client.get_bwB()))
    print('pwr     = {}'.format(client.get_power()))
    print('maxpwr  = {}'.format(client.get_maxpower()))
    if (vfo > 0):
        print('VFOset  = {}'.format(client.set_vfo(vfo)))
        print('VFO     = {}'.format(client.get_vfo()))
    print('info:\n{}'.format(client.get_info()))
    
   