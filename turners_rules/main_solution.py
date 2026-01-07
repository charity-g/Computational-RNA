import numpy as np
import pandas as pd

pairs = ['AU', 'CG', 'GC', 'UA', 'GU', 'UG'] # GU is wobble

turner_map = pd.read_csv('turner_map.csv')
turner_map = pd.pivot_table(turner_map, index=["top"], columns=["bottom"], values="energy")

turner_loop_map = pd.read_csv('turner_loop_map.csv')

print(turner_map)
print(turner_loop_map)