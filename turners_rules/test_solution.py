from .solution import calculate_free_energy 

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


def test_structure_a():
    assert calculate_free_energy(structureA) == 14.2

def test_structure_b():
    assert calculate_free_energy(structureB) == 15.5

def test_structure_c():
    assert calculate_free_energy(structureC) == 7.9

def test_structure_d():
    assert calculate_free_energy(structureD) == 11.0