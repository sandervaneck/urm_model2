# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:05:36 2024

@author: M67B363
"""
from stap_1 import pensioenjaar_calculator

def write_step_2(deelnemer_mediaan_results, participants, pensioenleeftijd, end_prognose_year, output_file_name, wb):
    ws = wb.create_sheet(title="10 jaar later")
    ws["A1"] = "Deelnemer"
    ws["B1"] = "Jaar"
    ws["C1"] = "Benefits 5pct"
    ws["D1"] = "Benefits 50pct"
    ws["E1"] = "Benefits 95pct"
    ws["F1"] = "Benefits Deflated 5pct"
    ws["G1"] = "Benefits Deflated 50pct"
    ws["H1"] = "Benefits Deflated 95pct"
    ws["I1"] = "Scenario 5pct"
    ws["J1"] = "Scenario 50pct"
    ws["K1"] = "Scenario 95pct"
    
    for deelnemer_nummer, result in enumerate(deelnemer_mediaan_results):
        pensioenjaar = min(end_prognose_year,10 + pensioenjaar_calculator(participants[deelnemer_nummer], pensioenleeftijd))
        if pensioenjaar < participants[deelnemer_nummer]['startdate prognosis'].year:
            pensioenjaar = participants[deelnemer_nummer]['startdate prognosis'].year + 10
        largest_year = end_prognose_year -1
        #result_entry['results'][0]['scenarioresults'][parameters[deelnemer_nummer]['amount of scenarios']]['jaar']
        #get_largest_year(
        pensioenjaar = min(largest_year, pensioenjaar)
        print(f"Deelnemer {deelnemer_nummer + 1} heeft pensioenjaar + 10 {pensioenjaar}")
        results = result['results']
        rownum = deelnemer_nummer + 2
        ws[f"A{rownum}"] = deelnemer_nummer + 1
        ws[f"B{rownum}"] = pensioenjaar
        ws[f"C{rownum}"] = results[pensioenjaar]['5th']['results']['nominal_benefit']
        ws[f"D{rownum}"] = results[pensioenjaar]['50th']['results']['nominal_benefit']
        ws[f"E{rownum}"] = results[pensioenjaar]['95th']['results']['nominal_benefit']
        ws[f"F{rownum}"] = results[pensioenjaar]['5th']['results']['real_benefit']
        ws[f"G{rownum}"] = results[pensioenjaar]['50th']['results']['real_benefit']
        ws[f"H{rownum}"] = results[pensioenjaar]['95th']['results']['real_benefit']
        ws[f"I{rownum}"] = results[pensioenjaar]['5th']['scenario']
        ws[f"J{rownum}"] = results[pensioenjaar]['50th']['scenario']
        ws[f"K{rownum}"] = results[pensioenjaar]['95th']['scenario']
        
    print("Gegevens weggeschreven in results.xlsx")
    wb.save(output_file_name) 
    