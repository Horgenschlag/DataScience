# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  # 导入pandas

df = pd.read_csv('xzk.csv')
coef = np.polyfit(df['T'], df['X'], 2)
y = coef[0] * df['T'] ** 2 + coef[1] * df['T'] + coef[2]  # 套公式求 y 值 = ax^2 + bx + c
Kt_x0 = coef[0] 
Kt_x1 = coef[1]
Kt_x2 = coef[2]
coef = np.polyfit(df['T'], df['Y'], 2)
y = coef[0] * df['Y'] ** 2 + coef[1] * df['Y'] + coef[2]  # 套公式求 y 值 = ax^2 + bx + c
Kt_y0 = coef[0] 
Kt_y1 = coef[1]
Kt_y2 = coef[2]
coef = np.polyfit(df['T'], df['Z'], 2)
y = coef[0] * df['T'] ** 2 + coef[1] * df['T'] + coef[2]  # 套公式求 y 值 = ax^2 + bx + c
Kt_z0 = coef[0] 
Kt_z1 = coef[1]
Kt_z2 = coef[2]
coef = np.polyfit(df['T'], df['V'], 3)
y = coef[0] * df['T'] ** 3 + coef[1] * df['T'] ** 2 + coef[2] *df['T'] + coef[3]  # 套公式求 y 值 = ax^2 + bx + c
Kt_v0 = coef[0] 
Kt_v1 = coef[1]
Kt_v2 = coef[2]
Kt_v3 = coef[3]
x = f'{Kt_x0} * t **2 + {Kt_x1} * t + {Kt_x2}'
y = f'{Kt_y0} * t **2 + {Kt_y1} * t + {Kt_y2}'
z = f'{Kt_z0} * t **2 + {Kt_z1} * t + {Kt_z2}'
v = f'{Kt_v0} * t **3 + {Kt_v1} * t **2 + {Kt_v2} * t + {Kt_v3}'
with open('зависимость.txt','w') as f:
	f.writelines(f'x = {x}\n')
with open('зависимость.txt','a') as f:
	f.writelines(f'y = {y}\nz = {z}\nv = {v}')