import numpy as np
import pandas as pd
import re

pairs = ['AU', 'CG', 'GC', 'UA', 'GU', 'UG'] # GU is wobble

turner_map = pd.read_csv('turner_map.csv')
turner_map = pd.pivot_table(turner_map, index=["top"], columns=["bottom"], values="energy")

turner_loop_map = pd.read_csv('turner_loop_map.csv')

# print(turner_map)
# print(turner_loop_map)

def findall_bases_rna(line):
    return re.findall(r'[AUGC]', line)

def check_hairpin_loop(lines, lines_energy, i):
    """
    Docstring for check_hairpin_loop
    
    :param lines: lines of RNA in custom representation
    :param lines_energy: lines of energy
    :param i: current line index

    :modifies lines_energy: updates energy for ONLY one line - the hairpin loop line

    :returns i: the current line index (starting after the hairpin loop)
    :returns prev_pair: the complete line that is a pair  
    """
    prev_pair = None
    start_i = i
    bases_in_loop = len(findall_bases_rna(lines[start_i]))
    if bases_in_loop == 2:
        prev_pair = lines[start_i]
    
    i += 1
    while i < len(lines) and len(lines[i].strip()) != 2:
        bases_in_loop += len(findall_bases_rna(lines[i]))
        i += 1
    loop_energy = turner_loop_map[turner_loop_map['bases in loop'] == bases_in_loop]['hairpin loop'][0]
    lines_energy[start_i] = loop_energy
    
    return [i, prev_pair]

def structure_free_energy(structure) -> float:
    prev_pair = None # either none or a pair
    lines = structure.strip().split('\n')
    lines_energy = [0.0] * len(lines)  
    i = 0

    i, prev_pair = check_hairpin_loop(lines, lines_energy, i)

    while i < len(lines):
        line = lines[i] 
        if len(line) == 2:
            bases_in_pair = len(re.findall(r'[AUGC]', line))
            if bases_in_pair == 2:
                if prev_pair is not None:
                    bases_in_prev_pair = len(re.findall(r'[AUGC]', prev_pair))
                    pair_energy = turner_map.loc[bases_in_pair, bases_in_prev_pair]
                    lines_energy[lines.index(prev_pair)] = pair_energy
                    total_energy += pair_energy
                prev_pair = line
                i += 1
            else:

            
        else:
            check_internal_loop(lines, lines_energy, i, prev_pair)


    total_energy = sum(lines_energy)
    return total_energy


def graph_representation() -> dict:
    # todo
    return {}

def runTests():
    structureA = """
 C
A  A
 GU
 A|
 G|
 UG
U  G
U  U
C  A
 GC 
 GC
 U|
 UG
 CG
 AU
 GC
 A|
 GC
"""
    assert structure_free_energy(structureA) == 14.2 
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
 AA 
G  A
G  G
 GC 
C  C
G  A
C  U
 AU 
 GC
 UA
 GU
 G|
 U|
 AU
 A|
 A|
 UA
 UG
"""
    assert structure_free_energy(structureC) == 7.9

    structureD = """
 G
G  G
U  G
U  C
 AU
 UG
 A|
 U|
 CG
 UG
 GU
A  A
G  G
C  C
 AU
 G|
 C|
 UA
"""
    assert structure_free_energy(structureD) == 11.0