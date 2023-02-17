#input 
def checkio(data) :
	for index in range(len(data) - 1, - 1, - 1) :
		if data.count(data [index]) == 1 :
			del data [index]
	return data



#====================
#gpt output=============
#Type 3
def checkio(data):
	i = len(data) - 1
	while i >= 0:
		if data.count(data[i]) == 1:
			del data[i]
		i -= 1
	return data

#Type 4
def checkio(data):
	items_seen = set()
	for item in reversed(data):
		if item in items_seen:
			data.remove(item)
		else:
			items_seen.add(item)
	return data

# Type 3 Code Clone Variants
def checkio_three(data) :
	for index in range(len(data) - 1, - 1, - 1) :
		if data.index(data [index]) == data.count(data [index]) - 1 :
			del data [index]
	return data


# Type 4 Code Clone Variants
def checkio_four(data) :
	for index in range(len(data) - 1, - 1, - 1) :
		if data.count(data [index]) == 1 and data.index(data [index]) == len(data) - data.count(data [index]) - 1 :
			del data [index]
	return data

