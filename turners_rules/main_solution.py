import numpy as np
import pandas as pd
import re

pairs = ['AU', 'CG', 'GC', 'UA', 'GU', 'UG'] # GU is wobble

turner_map = pd.read_csv('turner_map.csv')
turner_map = pd.pivot_table(turner_map, index=["top"], columns=["bottom"], values="energy")

turner_loop_map = pd.read_csv('turner_loop_map.csv')

# print(turner_map)
# print(turner_loop_map)

structure = """
 C
U  U
U  A
 GC
 UA
 G|
 CG
 UA"""

def structure_free_energy(structure) -> float:
    prev_pair = None # either none or a pair
    lines = structure.strip().split('\n')
    lines_energy = []
    total_energy = 0.0
    i = 0
    while i < len(lines):
        line = lines[i] 
        if len(line) == 2:
            bases_in_pair = len(re.findall(r'[AUGC]', line))
            if bases_in_pair == 2:
                # TODO
            else:
                # TODO
            
        else:
            start_i = i
            bases_in_loop = len(re.findall(r'[AUGC]', line))
            if bases_in_loop == 2:
                prev_pair = line
            i += 1
            while i < len(lines) and len(lines[i]) != 2:
                bases_in_loop += len(re.findall(r'[AUGC]', lines[i]))
                i += 1
            loop_energy = turner_loop_map[turner_loop_map['bases in loop'] == bases_in_loop]['hairpin loop'][0]
            lines_energy.append(loop_energy)
            for j in range(start_i+1, i):
                lines_energy.append("")
            total_energy += loop_energy

    return total_energy


def graph_representation() -> dict:
    # todo
    return {}

def runTests():
    structureA = """
 AG 
U  C
G  A
 UG 
 G| 
 CG 
 AU 
"""
    assert structure_free_energy(structureA) == -3.4 # TODO
    structureB = """
 GU 
U  G
 CG 
C  C
A  C
 UA 
 C| 
 A| 
 UG 
 AU 
 G| 
 C| 
 UA 
 C| 
 AU 
 GC 
 U| 
 GU 
 UC
"""
    assert structure_free_energy(structureB) == 15.5

    structureC = """
"""
    assert structure_free_energy(structureC) == -3.2 #TODO

