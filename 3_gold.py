import pandas as pd

# A utility class to store daily information
class Node():
	def __init__(self,buy,sell,price):
		self.buy = buy
		self.sell = sell
		self.price = price

	def add(self,buy,sell):
		self.buy += buy
		self.sell += sell

	def __repr__(self):
		return 'Node(%d, %d, %d)'%(self.buy,self.sell,self.price)


# calculates daily information (day code, daily buy - daily sell, daily price)
# and writes it to a file
def preprocess_train_data(df):
	m = {}
	for index,row in df.iterrows():
		key = (row['day'],row['month'],row['year'])
		key = key[0]+key[1]*31+key[2]*(12*31)
		try:
			i = int(row['price'])
			i = int(row['buy'])
			i = int(row['sell'])
		except ValueError:
			continue
		if key not in m:
			m[key] = Node(row['buy'],row['sell'],row['price'])
		else:
			m[key].add(row['buy'],row['sell'])

	with open('3_data.txt','w') as f:
		keys = m.keys()
		keys.sort()
		for key in keys:
			print >> f, key,m[key].buy-m[key].sell,m[key].price


# calculates daily information for query days (day code, daily buy - daily sell)
# and writes it to a file
def preprocess_queries(df):
	queries = [(13,4,2013),(13,7,2013),(14,7,2013),(7,11,2013),(15,12,2013),(9,2,2014),(17,2,2014)]
	idx = 0
	m = {}

	# compare two tuples (day,month,year)
	def comp(a,b):
		if a[2]==b[2]:
			if a[1]==b[1]:
				return a[0]<b[0]
			return a[1]<b[1]
		return a[2]<b[2]

	for index,row in df.iterrows():
		if idx>=len(queries):
			break
		q = queries[idx]
		key = (row['day'],row['month'],row['year'])
		if key==q:
			code = key[0]+key[1]*31+key[2]*(12*31)
			if code not in m:
				m[code] = Node(row['buy'],row['sell'],row['price'])
			else:
				m[code].add(row['buy'],row['sell'])
		elif comp(q,key):
			while comp(q,key):
				idx+=1
				if idx>=len(queries):
					break
				q = queries[idx]

	with open('3_data_q.txt','w') as f:
		keys = m.keys()
		keys.sort()
		for key in keys:
			print >> f, key,m[key].buy-m[key].sell


def main():
	df = pd.read_excel('_1.xlsx')
	preprocess_train_data(df)
	preprocess_queries(df)


if __name__ == "__main__":
	main()

