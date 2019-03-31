import numpy as np
import json
import socket
import json
strMap = ''
index = 1
x,y = 100,100

HOST = 'besthack19.sytes.net'
PORT = 4242
data = '{"team":"inmy4restle88dr", "task":%d}'%index
size_data = len(data).to_bytes(4, 'little')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST,PORT))
	s.send(size_data)
	s.send(bytearray(data.encode()))
	buffer = []
	sizeRecv = s.recv(4)
	sizeRecv = int.from_bytes(sizeRecv,'little')
	while len(strMap) <sizeRecv:
		b = s.recv(sizeRecv)
		buffer.append(b)
		strMap = b''.join(buffer)
	with open(f'task{index}.txt','w') as f:
		f.writelines(str(strMap))
	with open(f'task{index}.txt', 'r') as l:
		dict1 = {}
		list0 = []
		list1=l.read()
		list2=list1[list1.rfind('{'):list1.rfind('}')]
		list2 = list2[1:-1].split(',')
		for i in list2:
			list0 = i.split(':')
			dict1[list0[0][1:-1]] =int(list0[1])
		list1=list1.split(':',1)[1].split('}',1)[0]
		list1 = list1[1:-1].split(',')
		list1 = [int(i) for i in list1 ]
		dict1 = {"data":dict1}
	def map(l):
		width = len(l) ** (1/2)
		dictMap = {}
		x,y,i= 0,0,0
		while  y < width:
			dictMap[(x,y)]=l[i]
			x += 1
			i += 1
			if x == width:
				y += 1
				x = 0
		return dictMap
	dictMap = map(list1)
	dictData = dict1
	n = 0
	listx,listy,listh = [],[],[]
	xsum,ysum = 0,0
	while n <= 10:
		n += 1
		print(dictData)
		psi = dictData['data']['psi']
		speed = dictData['data']['speed']
		height = dictData['data']['height']
		listh.append(height)
		alpha = 3.1415926 * psi / 180  #psi转换成弧度制
		xsum += np.sin(alpha)*speed*1.25
		ysum += np.sin(alpha)*speed*1.25
		listx.append(xsum)
		listy.append(ysum)
		coordinate = '{"ready":1, "x":%d, "y":%d}'%(x,y)
		size_coordinate = len(coordinate).to_bytes(4, 'little')
		s.sendall(size_coordinate)
		s.sendall(bytearray(coordinate.encode()))
		dataSize = s.recv(4)
		dataSize = int.from_bytes(dataSize,'little')
		jsonData = s.recv(dataSize)
		dictData = json.loads(jsonData)
	listx,listy = [round(x) for x in listx],[round(y) for y in listy]
	dictxy = {listx[i]:listy[i] for i in range(len(listx))}
	for i in dictMap:
		listm = []
		if x != 100:
			break
		for h,j in dictxy.items():
			if h*j<=0:
				continue
			listm.append(dictMap[ (int(i[0] + h) , int(i[1] + j ))] )
		for k in range(len(listm)-1):
			if (listm[k]+listh[k] - (listm[k+1]+listh[k+1]))**2 >900:
				break
			elif k+1<len(listm):
				continue
			elif (listm[k]+listh[k] - (listm[0] + listh[0]))**2 >900:
				break
			else:	
				x,y = i[0]+xsum,i[1]+ysum
	while True:
		print(dictData)
		psi = dictData['data']['psi']
		alpha = 3.1415926 * psi / 180
		speed = dictData['data']['speed']
		if speed == 0:
			speed = speed0
		speed0 = speed
		x = x + np.sin(alpha)*speed*1.25
		y = y + np.cos(alpha)*speed*1.25
		coordinate = '{"ready":1, "x":%d, "y":%d}'%(x,y)
		size_coordinate = len(coordinate).to_bytes(4, 'little')
		height = dictData['data']['height']
		# h = dictMap[(x,y)]   #海拔
		# Hsum = height + h 
		s.send(size_coordinate)
		s.send(bytearray(coordinate.encode()))
		dataSize = s.recv(4)
		dataSize = int.from_bytes(dataSize,'little')
		jsonData = s.recv(dataSize)
		dictData = json.loads(jsonData)