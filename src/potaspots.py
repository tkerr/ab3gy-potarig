###############################################################################
# potaspots.py
# Author: Tom Kerr AB3GY
#
# Get spots from the POTA api.
# POTA = Parks on the Air
# References:
#     https://parksontheair.com/
#     https://pota.app/
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
import json
import requests
from datetime import datetime

# Local packages.


##############################################################################
# Globals.
##############################################################################
POTA_URL = "https://api.pota.app/spot/"


##############################################################################
# Lists for frequency-to-band conversion.
##############################################################################

bandmap_freqs = [135.7, 137.8, 472.0, 479.0, 501.0, 504.0, 1800.0, 2000.0, 
    3500.0, 4000.0, 5060.0, 5450.0, 7000.0, 7300.0, 10100.0, 10150.0, 
    14000.0, 14350.0, 18068.0, 18168.0, 21000.0, 21450.0, 24890.0, 24990.0, 
    28000.0, 29700.0, 50000.0, 54000.0, 70000.0, 71000.0, 144000.0, 148000.0,
    222000.0, 225000.0, 420000.0, 450000.0, 902000.0, 928000.0, 1240000.0, 1300000.0, 
    2300000.0, 2450000.0, 3300000.0, 3500000.0, 5650000.0, 5925000.0, 10000000.0, 10500000.0, 
    24000000.0, 24250000.0, 47000000.0, 47200000.0, 75500000.0, 81000000.0, 
    119980000.0, 120020000.0, 142000000.0, 149000000.0, 241000000.0, 250000000.0]
    
bandmap_bands = ['2190M', '2190M', '630M', '630M', '560M', '560M', '160M', '160M',
    '80M', '80M', '60M', '60M', '40M', '40M', '30M', '30M', '20M', '20M', '17M', '17M',
    '15M', '15M', '12M', '12M', '10M', '10M', '6M', '6M', '4M', '4M', '2M', '2M',
    '1.25M', '1.25M', '70CM', '70CM', '33CM', '33CM', '23CM', '23CM', '13CM', '13CM',
    '9CM', '9CM', '6CM', '6CM', '3CM', '3CM', '1.25CM', '1.25CM', 
    '6MM', '6MM', '4MM', '4MM', '2.5MM', '2.5MM', '2MM', '2MM',
    '1MM', '1MM']


##############################################################################
# Functions.
##############################################################################

# ----------------------------------------------------------------------------
def freq2band(fkhz):
    """
    Convert frequency in KHz to its respective band.
    """
    max = len(bandmap_freqs) - 1
    if (fkhz < bandmap_freqs[0]): return ''
    if (fkhz > bandmap_freqs[max]): return ''
    for i in range(0, max, 2):
        if (fkhz >= bandmap_freqs[i]) and (fkhz <= bandmap_freqs[i+1]):
            return bandmap_bands[i]
    return ''

# ----------------------------------------------------------------------------
def get_all_spots(url=POTA_URL):
    """
    Get spot information from the POTA api and return the data as a list of
    dictionaries.  List can include multiple spots for the same activation
    (activator + reference).
    
    spotTime field is converted to integer seconds since the Unix epoch.
    
    Returns spots as a list of dictionaries sorted by activator.  Returns 
    an empty list if unsuccessful.
    """
    data_json = []
    resp = None
    try:
        resp = requests.get(url)
    except Exception as err:
        errmsg = str(err).split(':')
        l = len(errmsg)
        for i in range(l):
            print("{}{}".format('  '*i, errmsg[i]), end='')
            if (i < (l-1)): print(':', end='')
            print()
    if resp:
        if (resp.status_code == 200):
            # Deserialize the JSON data.
            data_str = resp.content.decode('utf-8', errors='strict').replace('\ufffd', '?')
            temp = json.loads(data_str)
            data_json = sorted(temp, key=lambda d: d['activator'])
        else:
            print('HTTP request error: {}'.format(resp.status_code))
    
    # Convert spot time to integer.
    # Create a 'spotTimeShort' field.
    for spot in data_json:
        spot['spotTimeShort'] = spot['spotTime'][11:16]
        utc_time = datetime.strptime(spot['spotTime'], '%Y-%m-%dT%H:%M:%S')
        epoch_time = int((utc_time - datetime(1970,1,1)).total_seconds())
        spot['spotTime'] = epoch_time
    return data_json

# ----------------------------------------------------------------------------
def get_latest_spots(url=POTA_URL):
    """
    Get spot information from the POTA api and return the data as a list of
    dictionaries.  List includes only the most recent spot for each activation
    (activator + reference).
    
    spotTime field is converted to integer seconds since the Unix epoch.
    
    Returns spots as a list of dictionaries sorted by activator.  Returns 
    an empty list if unsuccessful.
    """
    latest_spots = []
    all_spots = get_all_spots(url)
    if (len(all_spots) == 0): return []
    
    current_spot = all_spots[0]
    for i in range(1,len(all_spots)):
        new_spot = all_spots[i]
        if (new_spot['activator'] == current_spot['activator']) and \
           (new_spot['reference'] == current_spot['reference']):
               if (new_spot['spotTime'] > current_spot['spotTime']):
                   current_spot = new_spot
        else:
            latest_spots.append(current_spot)
            current_spot = new_spot
    return latest_spots

# ----------------------------------------------------------------------------
def filter_spots(spots_list, filter_dict):
    """
    Filter the spots in the supplied list according to parameters provided in
    the filter dictionary.
    """
    filtered_spots = []
    
    # Remove non-filter keys.
    filter_keys = list(filter_dict.keys())
    if ('band' in filter_keys) and (filter_dict['band'] == 'ALL'): 
        filter_keys.remove('band')
    if ('mode' in filter_keys) and (filter_dict['mode'] == 'ALL'): 
        filter_keys.remove('mode')
    if ('program' in filter_keys) and (filter_dict['program'] == 'ALL'): 
        filter_keys.remove('program')
    
    # Filter the spots.
    for spot in spots_list:
        if 'band' in filter_keys:
            spotBand = freq2band(float(spot['frequency']))
            if spotBand != filter_dict['band']: continue
        if 'mode' in filter_keys:
            if spot['mode'] != filter_dict['mode']: continue
        if 'program' in filter_keys:
            spotProgram = spot['reference'][0:2]
            if spotProgram != filter_dict['program']: continue
        if filter_dict['exclude_qrt'] and ('QRT' in spot['comments'].upper()): continue
        filtered_spots.append(spot)
    
    if 'sortby' in filter_keys:
        filtered_spots = sort_spots(filtered_spots, filter_dict['sortby'])

    return filtered_spots

# ----------------------------------------------------------------------------
def parse_spots(spots_list):
    """
    Parse the spots in the supplied list and return lists used to filter the spots.
    Sorted lists provided: band, mode, program
    """
    band_list = []
    mode_list = []
    program_list = []
    
    for spot in spots_list:
        band = freq2band(float(spot['frequency']))
        if (band != '') and (band not in band_list): band_list.append(band)
        mode = spot['mode']
        if (mode != '') and (mode not in mode_list): mode_list.append(mode)
        program = spot['reference'][0:2]
        if program not in program_list: program_list.append(program)
    return (sorted(band_list), sorted(mode_list), sorted(program_list))

# ----------------------------------------------------------------------------
def sort_spots(spots_list, field):
    """
    Sort the spots in the supplied list by the specified field.
    """
    if (field == 'frequency'):
        return sorted(spots_list, key=lambda d: float(d['frequency']))
    elif (field == 'location'):
        return sorted(spots_list, key=lambda d: d['locationDesc'])
    elif (field == 'time'):
        return sorted(spots_list, key=lambda d: d['spotTime'], reverse=True)
    else:
        return sorted(spots_list, key=lambda d: d[field])
    
    
##############################################################################
# Main program.
############################################################################## 
if __name__ == "__main__":
    import sys
    
    url = POTA_URL
    if len(sys.argv) > 1:
        url = sys.argv[1]
    spots = get_latest_spots(url, True)
    for spot in spots:
        print(spot)
    print(parse_spots(spots))
    print(len(spots))
   