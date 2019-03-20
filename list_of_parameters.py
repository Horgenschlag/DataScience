#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from coordinate import *
time = t
alpha = 0.5
coordinate = [-238.29967338741352,1000,-142.1992683043871]
def timeToHeight(height):
	coef = np.polyfit( hsumy,tsumy, 2)
	y = coef[0] * dfy.hsumy ** 2 + coef[1] * dfy.hsumy + coef[2]  # 套公式求 y 值 = ax^2 + bx + c
	curve = np.poly1d(coef) 
	return curve(height)
def distance(time):
	plt.scatter(tlist, xlist, s=3)             #dot to curve
	coef = np.polyfit(tlist, xlist, 3)
	y = coef[0] * 'tlist' ** 3 + coef[1] * 'tlist' **2 + 'tlist' * coef[2] + coef[3]
	curve = np.poly1d(coef)
	return curve(time)
def velocity(time):
	plt.scatter(tlist, vlist, s=3)             #dot to curve
	coef = np.polyfit(tlist, vlist, 3)
	y = coef[0] * 'tlist' ** 3 + coef[1] * 'tlist' **2 + 'tlist' * coef[2] + coef[3]
	curve = np.poly1d(coef)
	return curve(time)
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
	timeSum = timeToHeight(0)
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
	avgx = sumx / timeToHeight(0)
	avgz = sumz / timeToHeight(0)
	global df
	time = t
	f = forceToVelocity(v)
	vx = (v * np.cos(alpha) - avgx)
	vz = (v * np.sin(alpha) - avgz)
	xlist,zlist,vlist,tlist = [0],[0],[250],[0]
	x,z = 0,0 
	while time <= timeSum:
		a = (-f)/m
		vx += np.cos(alpha)* a * t
		vz += np.sin(alpha)* a * t
		x += vx * t
		z += vz * t
		f = forceToVelocity(np.sqrt(vx ** 2 + vz ** 2)) 
		time += t
		round(time,2)
		vsum = np.sqrt(vx ** 2 + vz ** 2)
		xlist.append(x)
		zlist.append(z)
		vlist.append(vsum)
		tlist.append(time)
	df = {'xlist':xlist,   'vlist':vlist,    'tlist':tlist}#list to dataframe
	df = pd.DataFrame(df)
	coordinate_x = [coordinate[0]+x for x in xlist]
	coordinate_z = [coordinate[2]+z for z in zlist]
	coordinate_y = [y for y in hsumy]
	tlist = tlist
	velocitylist = [np.sqrt(vsum**2 + vy**2) for vsum in vlist for vy in vsumy]
	with open('xzk.csv','w') as xzk:
		xzk.writelines('X,Y,Z,V,T\n')
	with open('xzk.csv','a') as xzk:
		for i in range(len(coordinate_x)):
			xzk.writelines(f'{coordinate_x[i]},{coordinate_y[i]},{coordinate_z[i]},{velocitylist[i]},{tlist[i]}\n')
if __name__ == '__main__':
	main()