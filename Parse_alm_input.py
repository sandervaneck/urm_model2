# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:26:34 2024

@author: M67B363
"""


import pandas as pd
from multiprocessing import Pool, cpu_count

def parse_alm_input(filename):
    sheetnames = ["18-27", "28-37", "38-47", "48-57", "58-67", "68-77", "78-87", "88-97", "98-107", "108-117", "118-127"]
    with Pool(cpu_count()) as pool:
        all_results = pool.map(alm_input_reader, [(filename, sheetname) for sheetname in sheetnames])
    
    # Flatten the list of lists into a single list
    flat_results = [item for sublist in all_results for item in sublist]
    
    return flat_results

def parse_alm_input_chunk(df_chunk):
    df_chunk = df_chunk[(df_chunk["year"].notna()) & (df_chunk["year"].apply(lambda x: isinstance(x, (int, float))))]
    df_chunk = df_chunk.astype({"year": "int", "scenario": "int", "cohort": "int", "cwf_op": "float", "cwf_pp": "float", "total_return": "float", "total_return_hon": "float"})
    
    results = df_chunk.to_dict("records")
    return results

def alm_input_reader(args):
    filename, sheetname = args
    results = []
    
    # Read the entire sheet into memory
    df = pd.read_excel(filename, sheet_name=sheetname, skiprows=0)
    df.columns = ["year",
    "scenario",
    "cohort",
    "cwf_op",
    "cwf_pp",
    "total_return",
    "total_return_hon"]
    #["A", "B", "C", "D", "E", "F", "G"]
    
    # Process the DataFrame in chunks manually
    chunk_size = 10000
    for start_row in range(0, len(df), chunk_size):
        end_row = min(start_row + chunk_size, len(df))
        df_chunk = df.iloc[start_row:end_row]
        chunk_results = parse_alm_input_chunk(df_chunk)
        results.extend(chunk_results)
    
    return results

