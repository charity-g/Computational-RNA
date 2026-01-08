import numpy as np
import pandas as pd

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
    # TODO
    return 0.0


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