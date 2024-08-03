##############################################################################
# app.py
#
# A Flask web interface for the AB3GY POTA spot application.
##############################################################################

import os
import time
from flask import Flask, redirect, render_template, request, make_response
from flask import session

# Local packages.
import lib.Logger as log
import src.flrig_api as flrig
import src.log_adif_api as log_adif
import src.potaspots as potaspots

##############################################################################
# Globals.
############################################################################## 
app = Flask(__name__)

# Global POTA display filters.
g_filters = {
    'band'        : 'ALL',
    'mode'        : 'ALL',
    'program'     : 'ALL',
    'sortby'      : 'activator',
    'exclude_qrt' : False,
}


##############################################################################
# Functions.
############################################################################## 

#-----------------------------------------------------------------------------
def run_flask_server(host='localhost', port=8080, debug=False):
    """
    Run the Flask simple builtin web server application.
    """
    global app

    # Start the server.
    msg = 'Starting Flask server on {}:{}, debug={}\n'.format(host, port, debug)
    msg += 'Press CTRL-C to quit'
    if log.logger is not None:
        log.logger.print_and_log(msg)
    else:
        print(msg)
    app.run(host=host, port=port, debug=debug)

#-----------------------------------------------------------------------------
def shutdown_server():
    """
    Programmatically shut down the Flask server.
    NOTE: This does not work - not running with the Werkzeug Server
    See https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        print('Werkzeug Server shutdown not found')
    else:
        func()

#-----------------------------------------------------------------------------
def get_referrer():
    """
    Return the referring page route.
    """
    ref = ''
    url = request.referrer
    if url is not None:
        url_parts = url.split('/')
        if (len(url_parts) > 0):
            ref = '/' + url_parts[-1]
    return ref

#-----------------------------------------------------------------------------
def update_filters(filters):
    """
    Update the spot filters based on the supplied dictionary.
    """
    global g_filters
    filter_keys = list(filters.keys())
    #print(filters)
    
    if 'band' in filter_keys:
        g_filters['band'] = filters['band'].upper()
    if 'mode' in filter_keys:
        g_filters['mode'] = filters['mode'].upper()
    if 'program' in filter_keys:
        g_filters['program'] = filters['program'].upper()
    if 'sortby' in filter_keys:
        g_filters['sortby'] = filters['sortby']
    if 'exqrt' in filter_keys:
        g_filters['exclude_qrt'] = True
    else:
        g_filters['exclude_qrt'] = False
    #print(g_filters)


##############################################################################
# Routes.
# In Flask, URLs are bound to functions that execute when the web page is 
# requested.
############################################################################## 

#-----------------------------------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def route_app_main():
    global g_filters
    #print('A')
    spots_list = potaspots.get_latest_spots()
    #print(spots_list)
    now = int(time.time())
    create_time = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    
    #print('B')
    band_list, mode_list, program_list = potaspots.parse_spots(spots_list)
    
    if (request.method == 'POST'):
        #print('C')
        filters = request.form.to_dict()
        update_filters(filters)
    
    #print('D')
    filtered_spots = potaspots.filter_spots(spots_list, g_filters)
    
    #print('E')
    for spot in filtered_spots:
        spot['timeSince'] = int(now - spot['spotTime'])
    
    #print('F')
    html = render_template('app_main.html',
        create_time=create_time,
        spots_list=filtered_spots,
        band_list=band_list,
        mode_list=mode_list,
        program_list=program_list,
        filters=g_filters)
    resp = make_response(html)
    return resp

#-----------------------------------------------------------------------------
@app.route('/flrig', methods=['GET'])
def route_app_flrig():
    if (request.method == 'GET'):
        mode = request.args.get('mode')
        freq = request.args.get('freq')
        flrig.set_xcvr(mode, freq)
    return ('', 204) # 204 No Content

#-----------------------------------------------------------------------------
@app.route('/logdata', methods=['GET'])
def route_app_logdata():
    if (request.method == 'GET'):
        call = request.args.get('call')
        freq = request.args.get('freq')
        mode = request.args.get('mode')
        ref = request.args.get('ref')
        name = request.args.get('name')
        log_adif.log_data(call, freq, mode, ref, name)
    return ('', 204) # 204 No Content


##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    import os
    import sys
    print('{} main program called'.format(os.path.basename(sys.argv[0])))
    
    