# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 14:00:48 2024

@author: M67B363
"""

from Utils import get_first_year
from ontwikkel_scenario import ontwikkel_scenario

def process_scenario(eerste_berekeningsjaar, scenario, nummer, parameters, fourd, twod, endprognoseyear, pensioenleeftijd, pensioenjaar, berekeningsjaar):
    prognosejaar = get_first_year(fourd, twod)
    return ontwikkel_scenario(
        eerste_berekeningsjaar=eerste_berekeningsjaar,
        endprognoseyear=endprognoseyear,
        scenario=scenario,
        parameters=parameters,
        fourd=fourd,
        twod=twod,
        pensioenleeftijd=pensioenleeftijd,
        prognosejaar=prognosejaar,
        pensioenjaar=pensioenjaar,
        eerste_jaar=berekeningsjaar,
        berekeningsjaar=berekeningsjaar
    )  