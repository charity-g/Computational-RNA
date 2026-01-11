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
    total_energy, lines = calculate_free_energy(structureA, debug=True)
    assert lines == [7.4, 0.0, 0.6, 5.2, 0.0, 1.9, 2.5, 0.0, 0.0, -2.1, 3.3, -1.5, -1.8, -1.7, -2.9, 3.3]
    assert total_energy == 14.2

def test_structure_b():
    total_energy, lines = calculate_free_energy(structureB, debug=True)
    assert lines == [5.9, 0.0, -1.7, 1.7, 0.0, -0.9, 5.2, 0.0, -0.7, -0.9, 5.2, 0.0, -1.1, 3.3, -1.7, -2.1, 3.3]
    assert total_energy == 15.5

def test_structure_c():
    total_energy, lines = calculate_free_energy(structureC, debug=True)
    assert lines == [4.3, 0.0, 0.0, -2.3, 2.5, 0.0, 0.0, -1.7, -2.1, -0.9, -0.5, 5.2, 0.0, -0.9, 0.0]
    assert total_energy == 7.9

def test_structure_d():
    total_energy, lines = calculate_free_energy(structureD, debug=True)
    assert lines == [4.1, 0.0, 0.0, 0.0, -0.5, -1.5, 5.2, 0.0, -1.7, -0.5, -0.5, 2.5, 0.0, 0.0, -0.9, 5.2, 0.0, 0.0]
    assert total_energy == 11.0