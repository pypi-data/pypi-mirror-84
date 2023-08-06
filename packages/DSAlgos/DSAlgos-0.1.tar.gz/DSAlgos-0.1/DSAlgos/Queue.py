class Queue:
	def __init__(self):
		self.val = []
	
    # this function inserts the value in the list's 0th position
	def enqueue(self, item):
		self.val.insert(0,item)
	
    # this function pops the last element from the list
	def dequeue(self):
		return self.val.pop()
	
    # this function tells if the queue is empty or not
	def is_empty(self):
		return self.val == []