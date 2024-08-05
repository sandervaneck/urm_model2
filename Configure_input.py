# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:34:05 2024

@author: M67B363
"""

def configure_input(participants, macro_input, alm_input):
    deelnemerresults = []
    deelnemer_mediaan_results = []
    pensioenleeftijd = 67
    eerste_berekeningsjaar = 2024
    premie_percentage = 0.224
    end_prognose_year = eerste_berekeningsjaar + 49
    scenario_aantal = max_scenario(macro_input, alm_input)
    deelnemers_aantal = len(participants)
    
    alm_data = {scenario: filter_scenario_data(alm_input, macro_input, scenario)[0] for scenario in range(1, scenario_aantal)}
    macro_data = {scenario: filter_scenario_data(alm_input, macro_input, scenario)[1] for scenario in range(1, scenario_aantal)}
    
    return (end_prognose_year, eerste_berekeningsjaar, deelnemerresults, deelnemer_mediaan_results, pensioenleeftijd, scenario_aantal, deelnemers_aantal, premie_percentage, alm_data, macro_data)
    
    
def max_scenario(macro_input, alm_input):
    scenarios_alm = [entry['scenario'] for entry in alm_input]
    scenarios_macro = [entry['scenario'] for entry in macro_input]
    return max(scenarios_alm + scenarios_macro)

def filter_scenario_data(macro_input, alm_input, scenario):
    alm_filtered = [entry for entry in alm_input if entry["scenario"] == scenario]
    macro_filtered = [entry for entry in macro_input if entry["scenario"] == scenario]
    return alm_filtered, macro_filtered