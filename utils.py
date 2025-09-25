def lerp(start, end, strength):
	return (1 - strength) * start + strength * end

def clamp(value, minimum, maximum):
	return min(max(value, minimum), maximum)

def wrap(value, minimum, maximum):
	while value > maximum:
		value -= (maximum - minimum)
	while value < minimum:
		value += (maximum - minimum)
	return value