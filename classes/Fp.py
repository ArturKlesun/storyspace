def vectorDiff(a, b):
	return (a[0] - b[0], a[1] - b[1])

def vectorSum(a, b):
	return (a[0] + b[0], a[1] + b[1])

def isPointInRect(p, r):
	return p[0] > r[0] and p[1] > r[1] and p[0] < r[0] + r[2] and p[1] < r[1] + r[3]

def distanceBetween(point1, point2):
	dif = vectorDiff(point1, point2)
	return (dif[0]**2 + dif[1]**2)**(0.5)

def split(someList, pos):
	return (someList[:pos], someList[pos:])


def overrides(interface_class):
	def overrider(method):
		assert(method.__name__ in dir(interface_class))
		return method
	return overrider