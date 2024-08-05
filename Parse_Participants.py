# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:21:39 2024

@author: M67B363
"""

import pandas as pd

def parse_participants(filename):
    results = []
    df = pd.read_excel(filename, sheet_name='Parameters', skiprows=0)
    df.columns = [
        "urm state", "savings start", "savings start honorary", "benefit start", "pensionbase",
        "birthdate", "startdate prognosis", "calculationdate", "enddate prognosis",
        "default retirement date", "age fraction", "year fraction retirement year",
        "amount of scenarios", "pp ratio", "start year", "person id"
    ]
    chunk_size = 10000
    for start_row in range(0, len(df), chunk_size):
        end_row = min(start_row + chunk_size, len(df))
        df_chunk = df.iloc[start_row:end_row]
        chunk_results = parse_parameter_chunk(df_chunk)
        results.extend(chunk_results)
    
    return results


def parse_parameter_chunk(df_chunk):
    # Filter out rows where 'urm state' is not a string
    df_chunk = df_chunk[(df_chunk["urm state"].notna()) & (df_chunk["urm state"].apply(lambda x: isinstance(x, str)))]
    
    # Define date columns
    date_columns = [ "birthdate", 
                    "startdate prognosis", "calculationdate", "enddate prognosis", "default retirement date"]
    
    # Handle non-date columns separately for type conversion
    non_date_columns = {
        "urm state": "string", 
        "savings start": "int",
        "savings start honorary": "int",
        "benefit start": "int",
        "pensionbase": "int", 
        "age fraction": "float",
        "year fraction retirement year": "float", 
        "amount of scenarios": "int",
        "pp ratio": "float", 
        "start year": "int",
        "person id": "string"
    }
    
    # Convert integer date values to actual date values if they are not already datetime
    for col in date_columns:
        if not pd.api.types.is_datetime64_any_dtype(df_chunk[col]):
            df_chunk[col] = pd.to_datetime(df_chunk[col], origin='1899-12-30', unit='D').dt.date

    # Convert other columns to appropriate data types
    df_chunk = df_chunk.astype(non_date_columns)
    
    # Convert the DataFrame to a dictionary of records
    results = df_chunk.to_dict("records")
    
    return results


