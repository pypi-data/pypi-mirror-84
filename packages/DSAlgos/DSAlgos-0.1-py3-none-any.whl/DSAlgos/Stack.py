class Stack:
	def __init__(self):
		self.val = []
        
    # appends a value at the end of the list
	def push(self, item):
		self.val.append(item)
	
    # pops the value from the list
	def pop(self):
		if self.val==[]:
			print("Stack is empty")
			return None
		return self.val.pop()
	
    # this function tells the topmost element in the stack
	def peek(self):
		if self.val==[]:
			print("Stack is empty")
			return None
		return self.val[len(self.val)-1]
		
    # this function tells if the stack is empty or not
	def is_empty(self):
		return self.val == []
