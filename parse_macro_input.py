# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:27:54 2024

@author: M67B363
"""
import pandas as pd
from Utils import convert_to_float

def parse_macro_input(filename):
    df = pd.read_excel(filename, sheet_name='2d', skiprows=1, header=None)  # Adjust based on your actual sheet
    df.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # Set column names
    return parse_input(df)

def parse_input(df):
    results = []
    
    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        year = row['A']  # Assuming 'A' is the column name for the 'year'
        
        # Check if year is valid
        if pd.isna(year) or year == "" or not isinstance(year, (int, float)):
            break
        
        result = {
            "year": year,
            "scenario": row['B'],  # Assuming 'B' is the column name for 'scenario'
            "one_year_inflation": convert_to_float(row['C']),  # Assuming 'C' is the column name for 'one_year_inflation'
            "cpi": convert_to_float(row['D']),  # Assuming 'D' is the column name for 'cpi'
            "ff": convert_to_float(row['E']),  # Assuming 'E' is the column name for 'ff'
            "payout_adjustment": convert_to_float(row['F']),  # Assuming 'F' is the column name for 'payout_adjustment'
            "sr_adjustment": convert_to_float(row['G']),  # Assuming 'G' is the column name for 'sr_adjustment'
            "contribution_rate": convert_to_float(row['H'])  # Assuming 'H' is the column name for 'contribution_rate'
        }
        results.append(result)
    
    return results


    
