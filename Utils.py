# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:46:29 2024

@author: M67B363
"""

import numpy as np

def creeer_pensioenjaar_parameters(mediaan_scenario, start_parameters):
    parameters = start_parameters
    parameters['benefit start'] = mediaan_scenario['nominal_benefit']
    parameters['savings start'] = mediaan_scenario['total_capital']
    if parameters['urm state'] != "retired" and parameters['urm state'] != "partnerPension" and parameters['urm state'] != "orphanPension":
       parameters['calculationdate'] = start_parameters['default retirement date']
    parameters['status'] = 'retired'
    return parameters

def get_largest_year(example_variable):
    # Get all keys from the dictionary
    all_keys = example_variable.keys()
    # Find and return the maximum key
    return max(all_keys)

def convert_to_float(value):
    if value is None or value == '' or str(value).isspace():
        return 0.0
    try:
        return float(value)
    except ValueError:
        return 0.0
    
def get_input_vanaf_prognosejaar(macro_input, alm_input, prognosejaar):
    macro = [entry for entry in macro_input if entry["year"] >= prognosejaar]
    alm = [entry for entry in alm_input if entry["year"] >= prognosejaar]
    return (macro, alm)

def get_first_year(fourd_filtered, twod_filtered):
    fourd_years = [int(entry['year']) for entry in fourd_filtered if 'year' in entry]
    twod_years = [int(entry['year']) for entry in twod_filtered if 'year' in entry]
    if fourd_years and twod_years:
        prognosejaar = min(min(fourd_years), min(twod_years))
    elif fourd_years:
        prognosejaar = min(fourd_years)
    elif twod_years:
        prognosejaar = min(twod_years)
    else:
        prognosejaar = 1  # Default value if no year found
        
    return prognosejaar

def pensioenjaar_calculator(parameters, pensioenleeftijd):
    result = 0
    if parameters['urm state'] == "retired" or parameters['urm state'] == "partnerPension" or parameters['urm state'] == "orphanPension":
        result = parameters["calculationdate"].year
    else:
        result = min(parameters["default retirement date"].year, parameters["birthdate"].year + pensioenleeftijd)
    return result

def bereken_percentielen(year_data, percentiles):
    sorted_data = sorted(year_data.items(), key=lambda x: (x[1]['nominal_benefit'] if x[1]['nominal_benefit'] > 0 else x[1]['total_capital']))
    result = {}
    for p in percentiles:
        index = int(np.percentile(range(len(sorted_data)), p))
        scenario, data = sorted_data[index]
        result[f"{p}th"] = {'scenario': scenario, 'results': data}
    return result