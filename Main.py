# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 10:50:32 2024

@author: M67B363
"""
from Read_input import read_input
from Configure_input import configure_input
from stap_1 import stap_1
from stap_2 import stap_2
from schrijf_stap_1 import write_step_1
from schrijf_stap_2 import write_step_2
import openpyxl
from datetime import datetime
import multiprocessing as mp
from functools import partial

if __name__ == "__main__":
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start time: {time}")
    filename = 'input - 128 deelnemers - 2000 scenarios.xlsx'
    result_file_name = "results.xlsx"
    
    (participants, macro_input, alm_input) = read_input(filename)
    (end_prognose_year, eerste_berekeningsjaar, deelnemerresults, deelnemer_mediaan_results, pensioenleeftijd, scenario_aantal, deelnemers_aantal, premie_percentage, alm_data, macro_data) = configure_input(participants, macro_input, alm_input)
    deelnemerresults = []
    #Option 1:
    partial_stap1 = partial(
        stap_1,
        eerste_berekeningsjaar=eerste_berekeningsjaar,
        scenario_aantal=scenario_aantal,
        participants=participants,
        alm_input=alm_input,
        macro_input=macro_input,
        end_prognose_year=end_prognose_year,
        pensioenleeftijd=pensioenleeftijd
        )
    
    chunksize = max(1, deelnemers_aantal // (mp.cpu_count() * 4))
    
    #Check what chunksize is best
    print(f"chunksize: {chunksize}")
    #Try 500
    chunksize = 500
    with mp.Pool(mp.cpu_count()) as pool:
        deelnemerresults = pool.imap_unordered(partial_stap1, range(0, deelnemers_aantal), chunksize=chunksize)
      
    #Option 2
    #for nummer in range(0,deelnemers_aantal):
    #    deelnemerresults.append(stap_1(nummer, eerste_berekeningsjaar, scenario_aantal, participants, alm_input, macro_input, end_prognose_year, pensioenleeftijd))
        
    deelnemerresults = [result for result in deelnemerresults if result is not None]
    wb = openpyxl.Workbook()
    write_step_1(deelnemerresults, participants, pensioenleeftijd, result_file_name, wb)
    
    partial_stap_2 = partial(
        stap_2,
        eerste_berekeningsjaar=eerste_berekeningsjaar,
        scenario_aantal=scenario_aantal,
        fourd=participants,
        twod=alm_input,
        macro_input=macro_input,
        endprognoseyear=end_prognose_year,
        pensioenleeftijd=pensioenleeftijd,
        result = deelnemerresults
        )
    
    stap_2_results = []
    with mp.Pool(mp.cpu_count()) as pool:
        stap_2_results = pool.imap_unordered(partial_stap_2, range(0, deelnemers_aantal), chunksize=chunksize)
      
    #Option 2
    #for idx, deelnemerresult in enumerate(deelnemerresults):
    #    stap_2_results.append(stap_2(idx, eerste_berekeningsjaar, scenario_aantal, participants, alm_input, macro_input, end_prognose_year, pensioenleeftijd, deelnemerresults))
    
    stap_2_results = [result for result in stap_2_results if result is not None]   
    write_step_2(stap_2_results, participants, pensioenleeftijd, end_prognose_year, result_file_name, wb)
    
    wb.save(result_file_name)
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"end time: {time}")
    
    
    
    