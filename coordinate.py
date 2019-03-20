#!/usr/bin/env python3
# coding: utf-8
# Author: 
 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
H0 = 1000
V0 = 250
m = 100
g = 9.81

t = 0.01
h = H0
G = m * g
vy = 0
v = V0

def main():
	timeSum = t
	listData = []
	height,velocity = h,vy
	while height > 0:
		listOstream = []
		Fa = forceToVelocity(velocity)
		a = (G-Fa)/m
		distance = t * velocity + 0.5 * a * t**2
		velocity += t * a
		height -= distance
		listTemp = [velocity,height,timeSum]
		listOstream.extend(listTemp)
		listData.append(listOstream)
		timeSum += t
		timeSum = round(timeSum,2)
	global vsumy, hsumy, tsumy, dfy
	vsumy=[]
	hsumy=[]
	tsumy=[]
	for i in listData:
		vsumy.append(i[0])
		hsumy.append(i[1])
		tsumy.append(i[2])
	dfy = {'tsumy':tsumy,'vsumy':vsumy,'hsumy':hsumy}
	dfy = pd.DataFrame(dfy)

	wind = pd.read_csv('Wind.csv')
	h1,h2 = 50,150
	sumx = (timeToHeight(0) - timeToHeight(h)) * wind['Wx,м/с,'][0]
	sumz = (timeToHeight(0) - timeToHeight(h)) * wind['Wz,м/с'][0]
	while h >= h1:
		if h >= h2:
			x = (timeToHeight(h1) - timeToHeight(h2)) * wind['Wx,м/с,'][(h1+50)//100]
			z = (timeToHeight(h1) - timeToHeight(h2)) * wind['Wz,м/с'][(h1+50)//100]
		else:
			x = (timeToHeight(h1)- timeToHeight(h)) * wind['Wx,м/с,'][(h1+50)//100]
			z = (timeToHeight(h1)- timeToHeight(h)) * wind['Wz,м/с'][(h1+50)//100]
		sumx += x
		sumz += z
		h1,h2 = h2, h2+100
	global avgx, avgz
	avgx = sumx / timeToHeight(0)
	avgz = sumz / timeToHeight(0)

	global alpha
	alpha = 0
	with open('coordinate.txt','w') as result_1:
		result_1.writelines('[X,Y,Z],Alpha\n')
	while alpha <= np.pi*2:
		cauculateResult()
		alpha += 0.1
		alpha = round(alpha,1)
	result_1.close()
def forceToVelocity(v):
	df1 = pd.read_csv('F.csv')
	plt.scatter(df1['V, м/с'],df1['Fa, Н'])
	coef = np.polyfit(df1['V, м/с'],df1['Fa, Н'],2)
	y = coef[0] * df1['V, м/с'] ** 2 + coef[1] * df1['V, м/с'] + coef[2]
	curve = np.poly1d(coef)
	plt.scatter(df1['V, м/с'],df1['Fa, Н'], s=0.5)
	plt.plot(df1['V, м/с'], curve(df1['V, м/с']) , c='r')
	return curve(v)
def timeToHeight(height):
	coef = np.polyfit( hsumy,tsumy, 2)
	y = coef[0] * dfy.hsumy ** 2 + coef[1] * dfy.hsumy + coef[2]  # 套公式求 y 值 = ax^2 + bx + c
	curve = np.poly1d(coef) 
	return curve(height)
def velocityToTime(time):
	coef = np.polyfit( tsumy,vsumy, 3)
	y =coef[0]* dfy.tsumy**3 + coef[1] * dfy.tsumy ** 2 + coef[2] * dfy.tsumy + coef[3]  # 套公式求 y 值 = ax^2 + bx + c
	curve = np.poly1d(coef)  # np.poly1d() 方便地生成曲线函数
	return curve(time)
def heightToTime(time):
	coef = np.polyfit( tsum,hsum, 2)
	y = coef[0] * dfy.tsumy ** 2 + coef[1] * dfy.tsumy + coef[2]  # 套公式求 y 值 = ax^2 + bx + c
	curve = np.poly1d(coef) 
	return curve(time)
def cauculateResult():
	f = forceToVelocity(v)
	vx = (v * np.cos(alpha) - avgx)
	vz = (v * np.sin(alpha) - avgz)
	time = t
	x,z = 0,0
	while time <= timeToHeight(h):
		a = (-f)/m
		vx += np.cos(alpha)* a * t
		vz += np.sin(alpha)* a * t
		x += vx * t
		z += vz *t
		f = forceToVelocity(np.sqrt(vx ** 2 + vz ** 2)) 
		time += t
	with open('coordinate.txt','a') as result_1:
		result_1.writelines(f'[{-x},{h},{-z}],{alpha}\n')
if __name__ == '__main__':
	main()