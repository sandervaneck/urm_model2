# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:32:43 2024

@author: M67B363
"""
from Parse_Participants import parse_participants
from Parse_alm_input import parse_alm_input
from parse_macro_input import parse_macro_input

def read_input(filename):
    participants = parse_participants(filename)
    macro_input = parse_macro_input(filename)
    alm_input = parse_alm_input(filename)
    return (participants, macro_input, alm_input)