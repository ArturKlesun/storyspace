def vectorDiff(a, b):
	return a[0] - b[0], a[1] - b[1]

def vectorSum(a, b):
	return a[0] + b[0], a[1] + b[1]

def vectorMult(a, koef):
	return a[0] * koef, a[1] * koef

def vectorReverse(vector):
	return vectorDiff([0,0], vector)

def isPointInRect(p, r):
	return p[0] > r[0] and p[1] > r[1] and p[0] < r[0] + r[2] and p[1] < r[1] + r[3]

def isRectInRect(r1, r2):
	return not (r1[0] + r1[2] < r2[0] or r1[1] + r1[3] < r2[1] or r1[0] > r2[0] + r2[2] or r1[1] > r2[1] + r2[3])

def distanceBetween(point1, point2):
	dif = vectorDiff(point1, point2)
	return (dif[0]**2 + dif[1]**2)**(0.5)

def split(someList, pos):
	return someList[:pos], someList[pos:]

def getVectorFromRectToPoint(rect, point):
	vector = [0,0]
	if point[0] < rect[0]:
		vector[0] -= rect[0] - point[0]
	if point[1] < rect[1]:
		vector[1] -= rect[1] - point[1]
	if point[0] > rect[0] + rect[2]:
		
		vector[0] += point[0] - rect[0] - rect[2]
	if point[1] > rect[1] + rect[3]:
		vector[1] += point[1] - rect[1] - rect[3]
	return vector
	

def overrides(interface_class):
	def overrider(method):
		assert(method.__name__ in dir(interface_class))
		return method
	return overrider