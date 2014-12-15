def vectorDiff(a, b):
	return (a[0] - b[0], a[1] - b[1])

def vectorSum(a, b):
	return (a[0] + b[0], a[1] + b[1])

def overrides(interface_class):
	def overrider(method):
		assert(method.__name__ in dir(interface_class))
		return method
	return overrider