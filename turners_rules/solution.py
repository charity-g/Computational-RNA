import pandas as pd
import re

pairs = ['AU', 'CG', 'GC', 'UA', 'GU', 'UG'] # GU is wobble

turner_map = pd.read_csv('turner_map.csv')
turner_map_for_printing = pd.pivot_table(turner_map, index=["top"], columns=["bottom"], values="energy")
turner_loop_map = pd.read_csv('turner_loop_map.csv')

print(turner_map_for_printing)
print(turner_loop_map)

def findall_rna_bases(line):
    return re.findall(r'[AUGC]', line)

def get_prev_pair_index(lines, curr_i, prev_pair):
    for j in range(curr_i-1, -1, -1):
        if lines[j] == prev_pair:
            return j
    raise ValueError(f"Previous pair {prev_pair} not found in lines")

# ==================

def calculate_hairpin_loop(lines, lines_energy, i):
    """
    Docstring for calculate_hairpin_loop
    
    :param lines: lines of RNA in custom representation
    :param lines_energy: lines of energy
    :param i: current line index

    :modifies lines_energy: updates energy for ONLY one line - the hairpin loop line

    :returns i: the current line index (starting after the hairpin loop)
    :returns prev_pair: the complete line that is a pair  
    """
    prev_pair = None
    start_i = i
    bases_in_loop = len(findall_rna_bases(lines[start_i]))
    if bases_in_loop == 2:
        prev_pair = lines[start_i]
    
    i += 1
    while i < len(lines) and len(lines[i].strip()) != 2:
        bases_in_loop += len(findall_rna_bases(lines[i]))
        i += 1
    loop_energy = turner_loop_map[turner_loop_map['bases in loop'] == bases_in_loop]['hairpin loop'][0]
    lines_energy[start_i] = loop_energy
    
    return [i, prev_pair]

def calculate_neighbor_pair(lines, lines_energy, i, prev_pair):
    """
    Docstring for calculate_neighbor_pair
    
    :param lines: lines of RNA in custom representation
    :param lines_energy: lines of energy
    :param i: current line index
    :param prev_pair: the previous pair line

    :modifies lines_energy: updates energy for ONLY one line - the neighbor pair line

    :returns i: the current line index (starting after the neighbor pair)
    :returns prev_pair: the complete line that is a pair  
    """
    line = lines[i]
    if prev_pair is not None:
        curr_pair_bases = findall_rna_bases(line)
        prev_pair_bases = findall_rna_bases(prev_pair)
        pair_energy = turner_map[(turner_map['top'] == prev_pair_bases) & (turner_map['bottom'] == curr_pair_bases)]['energy'][0] # ROWS is previous pair, COLUMNS is current pair
        lines_energy[get_prev_pair_index(lines, i, prev_pair)] = pair_energy
        
    return [i+1, line] 

def calculate_bulge_loop(lines, lines_energy, i):
    """
    Docstring for calculate_bulge_loop
    
    :param lines: lines of RNA in custom representation
    :param lines_energy: lines of energy
    :param i: current line index
    :param prev_pair: the previous pair line

    :modifies lines_energy: updates energy for ONLY one line - the neighbor pair line

    :returns i: the current line index (starting after the neighbor pair)
    """
    start_i = i
    bases_in_bulge = 0
    while i < len(lines) and len(findall_rna_bases(lines[i])) <= 2:
        bases_in_bulge += 1
        i += 1
    bulge_energy = turner_loop_map[turner_loop_map['bases in loop'] == bases_in_bulge]['bulge loop'][0]
    lines_energy[start_i] = bulge_energy

    return i


def calculate_internal_loop(lines, lines_energy, i):
    """
    Docstring for calculate_internal_loop
    
    :param lines: lines of RNA in custom representation
    :param lines_energy: lines of energy
    :param i: current line index
    :param prev_pair: the previous pair line

    :modifies lines_energy: updates energy for ONLY one line - the neighbor pair line

    :returns i: the current line index (starting at the neighbor pair)
    """
    bases_in_loop = 0
    start_i = i
    while i < len(lines) and len(lines[i].strip()) > 2:
        bases_in_loop += len(findall_rna_bases(lines[i]))
        i += 1
    
    internal_loop_energy = turner_loop_map[turner_loop_map['bases in loop'] == bases_in_loop]['internal loop'][0]
    lines_energy[start_i] = internal_loop_energy

    return i

def calculate_free_energy(structure) -> float:
    prev_pair = None # either none or a pair
    lines = structure.strip().split('\n')
    lines_energy = [0.0] * len(lines)  
    i = 0

    i, prev_pair = calculate_hairpin_loop(lines, lines_energy, i)

    while i < len(lines):
        line = lines[i] 
        if len(line) == 2: # is not an internal loop
            bases_in_pair = len(findall_rna_bases(line))
            if bases_in_pair == 2:
                i, prev_pair = calculate_neighbor_pair(lines, lines_energy, i, prev_pair)
            else:
                i = calculate_bulge_loop(lines, lines_energy, i)
        else:
            i = calculate_internal_loop(lines, lines_energy, i)


    total_energy = sum(lines_energy)
    return total_energy

