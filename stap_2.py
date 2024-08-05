# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:54:12 2024

@author: M67B363
"""
from Utils import get_largest_year, get_input_vanaf_prognosejaar, pensioenjaar_calculator, creeer_pensioenjaar_parameters, bereken_percentielen
from Process_scenario import process_scenario
from collections import defaultdict

def stap_2(nummer, eerste_berekeningsjaar, scenario_aantal, participant_parameters, fourd, twod, endprognoseyear, pensioenleeftijd, result):
    try:
        
        result = result[nummer]['results']
        #percentile_scenarios = get_percentile_scenarios(results)
        participant_parameters = participant_parameters[nummer]
        pensioenjaar = pensioenjaar_calculator(participant_parameters, pensioenleeftijd)
        berekeningsjaar = participant_parameters['calculationdate'].year
        if pensioenjaar < berekeningsjaar:
            pensioenjaar = berekeningsjaar
        if pensioenjaar >= berekeningsjaar:
            pensioenjaar = min(get_largest_year(result), pensioenjaar)
        
        mediaan_scenario = result[pensioenjaar]["50th"]
        porgnosejaar = pensioenjaar - participant_parameters['calculationdate'].year + 1
        twods, fourds = get_input_vanaf_prognosejaar(twod, fourd, porgnosejaar)
        pensioenjaar_parameters = creeer_pensioenjaar_parameters(mediaan_scenario['results'], participant_parameters)
        
        median_results = []
        for scenario in range(1, scenario_aantal + 1):
            try:
                median_results.append(process_scenario(
                    eerste_berekeningsjaar,
                    scenario, 
                    nummer, 
                    pensioenjaar_parameters, 
                    fourds, 
                    twods, 
                    endprognoseyear, 
                    pensioenleeftijd, 
                    pensioenjaar, 
                    pensioenjaar_parameters['calculationdate'].year
                ))
            except Exception as e:
                raise e
        
        restructured_results = defaultdict(lambda: defaultdict(dict))

        for result in median_results:
            scenario = result["scenario"]
            for entry in result["scenarioresults"]:
                year = entry["jaar"]
                nominal_benefit = entry["nominal_benefit"]
                nominal_benefit_sr = entry["nominal_benefit_sr"]
                real_benefit = entry["real_benefit"]
                total_capital = entry["total_capital"]
                savings_op = entry["savings_op"]
                savings_hon = entry["savings_hon"]
                leeftijd = entry["leeftijd"]
                restructured_results[year][scenario] = {
                    "nominal_benefit": nominal_benefit,
                    "nominal_benefit_sr": nominal_benefit_sr,
                    "real_benefit": real_benefit,
                    "total_capital": total_capital,
                    "savings_op": savings_op,
                    "savings_hon": savings_hon,
                    "leeftijd": leeftijd
                    }
        
        final_result = {}
        percentiles = [5, 50, 95]

        for year, year_data in restructured_results.items():
            final_result[year] = bereken_percentielen(year_data, percentiles)

        
        return {
            "deelnemer": nummer + 1,
            "results": final_result
        }
    except Exception as e:
        return None