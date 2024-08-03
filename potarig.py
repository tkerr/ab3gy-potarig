###############################################################################
# potarig.py
# Author: Tom Kerr AB3GY
#
# Create a local web page to get POTA spots and control a transceiver using flrig.
# Helps facilitate POTA hunting from a home station.
# POTA = Parks on the Air
# POTA references:
#     https://parksontheair.com/
#     https://pota.app/
# FLRIG references:
#    http://www.w1hkj.com/
#    http://www.w1hkj.com/flrig-help/
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
import os
import sys

# Environment setup.
sys.path.insert(1, os.path.abspath('./lib'))
sys.path.insert(3, os.path.abspath('./src'))

# Local packages.
import lib.ConfigFile as ConfigFile
import lib.Logger as log
import src.app as app
import src.flrig_api as flrig
import src.log_adif_api as log_adif


##############################################################################
# Globals.
##############################################################################
scriptname = os.path.basename(sys.argv[0])
log_base = os.path.splitext(scriptname)[0]
logfile = os.path.join(os.path.abspath('.'), log_base + '.log')


##############################################################################
# Functions.
##############################################################################


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    
    # Start the logger.
    log.logger = log.Logger(logfile)
    log.logger.log_msg('{} started.'.format(scriptname))
    
    # Read the config file.
    config = ConfigFile.ConfigFile()
    (status, err_msg) = config.read(create=False)
    if not status:
        print('Error reading configuration file: {}'.format(err_msg))
    
    # Set up the ADIF log file.
    adif_filename = config.get('ADIF', 'FILENAME')
    log_adif.init_api(adif_filename)

    # Set up the flrig api.
    server_url = ''
    if status: 
        server_url = config.get('FLRIG', 'URL')
    if (len(server_url) == 0):
        server_url = flrig.DEFAULT_SERVER_URL
    log.logger.print_and_log('Flrig server url: {}'.format(server_url))
    flrig.client_init(server_url)
    if status:
        modes = config.get_section('MODES')
        if (len(modes) > 0):
            flrig.set_modes(modes)
        else:
            print('Flrig modes map not found in config file.')
    
    # Run the Flask simple builtin server.
    flask_host = config.get('FLASK', 'HOST')
    if (len(flask_host) == 0): flask_host = 'localhost'
    flask_port = config.get('FLASK', 'PORT')
    if (len(flask_port) == 0): flask_port = '8080'
    app.run_flask_server(flask_host, flask_port)
    
    log.logger.log_msg('{} exiting.\n'.format(scriptname))
    log.logger.close()
   