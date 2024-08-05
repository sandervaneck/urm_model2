# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:50:45 2024

@author: M67B363
"""
from stap_1 import pensioenjaar_calculator
from Utils import get_largest_year

def write_step_1(deelnemerresults, participants, pensioenleeftijd, output_file, wb):
    
    default_sheet = wb.active
    wb.remove(default_sheet)
    ws = wb.create_sheet(title="Pensioendatum")
    ws["A1"] = "Deelnemer"
    ws["B1"] = "Pensioenjaar"
    ws["C1"] = "Savings 5pct"
    ws["D1"] = "Savings 50pct"
    ws["E1"] = "Savings 95pct"
    ws["F1"] = "Savings Honorary 5pct"
    ws["G1"] = "Savings Honorary 50pct"
    ws["H1"] = "Savings Honorary 95pct"
    ws["I1"] = "Benefits 5pct"
    ws["J1"] = "Benefits 50pct"
    ws["K1"] = "Benefits 95pct"
    ws["L1"] = "Benefits Deflated 5pct"
    ws["M1"] = "Benefits Deflated 50pct"
    ws["N1"] = "Benefits Deflated 95pct"
    ws["O1"] = "Scenario 5pct"
    ws["P1"] = "Scenario 50pct"
    ws["Q1"] = "Scenario 95pct"
    
    for deelnemer_nummer, result in enumerate(deelnemerresults):
        pensioenjaar = pensioenjaar_calculator(participants[deelnemer_nummer], pensioenleeftijd)
        
        result = result['results']
        if pensioenjaar < participants[deelnemer_nummer]['startdate prognosis'].year:
            pensioenjaar = participants[deelnemer_nummer]['startdate prognosis'].year
        pensioenjaar = min(get_largest_year(result), pensioenjaar)
         
        rownum = deelnemer_nummer + 2
        ws[f"A{rownum}"] = deelnemer_nummer + 1
        ws[f"B{rownum}"] = pensioenjaar
        ws[f"C{rownum}"] = result[pensioenjaar]['5th']['results']['savings_op']
        ws[f"D{rownum}"] = result[pensioenjaar]['50th']['results']['savings_op']
        ws[f"E{rownum}"] = result[pensioenjaar]['95th']['results']['savings_op']
        ws[f"F{rownum}"] = result[pensioenjaar]['5th']['results']['savings_hon']
        ws[f"G{rownum}"] = result[pensioenjaar]['50th']['results']['savings_hon']
        ws[f"H{rownum}"] = result[pensioenjaar]['95th']['results']['savings_hon']
        ws[f"I{rownum}"] = result[pensioenjaar]['5th']['results']['nominal_benefit']
        ws[f"J{rownum}"] = result[pensioenjaar]['5th']['results']['nominal_benefit']
        ws[f"K{rownum}"] = result[pensioenjaar]['5th']['results']['nominal_benefit']
        ws[f"L{rownum}"] = result[pensioenjaar]['5th']['results']['real_benefit']
        ws[f"M{rownum}"] = result[pensioenjaar]['5th']['results']['real_benefit']
        ws[f"N{rownum}"] = result[pensioenjaar]['5th']['results']['real_benefit']
        ws[f"O{rownum}"] = result[pensioenjaar]['5th']['scenario']
        ws[f"P{rownum}"] = result[pensioenjaar]['50th']['scenario']
        ws[f"Q{rownum}"] = result[pensioenjaar]['95th']['scenario']
        
    print("Gegevens weggeschreven in results.xlsx")
    wb.save(output_file) 