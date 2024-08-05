# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:42:40 2024

@author: M67B363
"""
from collections import defaultdict
from Utils import pensioenjaar_calculator, bereken_percentielen
from Process_scenario import process_scenario
import logging

def stap_1(nummer, eerste_berekeningsjaar, scenario_aantal, participants, alm_input, macro_input, endprognoseyear, pensioenleeftijd):
    try:
        # Log the current participant number and length of parameters        
        # Check if index is in range
        if nummer < 0 or nummer >= len(participants):
            logging.error(f"Participant index {nummer} out of range for parameters list of length {len(participants)}")
            return None
        
        
        participant_parameters = participants[nummer]

        results = []
        for scenario in range(1, scenario_aantal + 1):
            pensioenjaar = pensioenjaar_calculator(participant_parameters, pensioenleeftijd)
            berekeningsjaar = participant_parameters['calculationdate'].year
            try:
                result = process_scenario(
                    eerste_berekeningsjaar,
                    scenario, 
                    nummer, 
                    participant_parameters, 
                    alm_input, 
                    macro_input, 
                    endprognoseyear, 
                    pensioenleeftijd, 
                    pensioenjaar, 
                    berekeningsjaar
                )
                results.append(result)
            except Exception as e:
                logging.error(f"Error processing scenario {scenario} for participant {nummer}: {e}")
                raise e
        restructured_results = defaultdict(lambda: defaultdict(dict))

        for result in results:
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

        print(f"Participant {nummer} done")
        return {
            "deelnemer": nummer + 1,
            "results": final_result
        }
    except IndexError as e:
        logging.error(f"IndexError for participant {nummer}: {e}")
        return None

  
    
