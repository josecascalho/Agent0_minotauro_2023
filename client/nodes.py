class Node:
	"""The node has a name and keeps connection to parent 
	    which is a Node or None.
	    The _path_cost is the cost between parent and the node
	    The _total_cost is the some of all costs from previous connections
	    from the tree root (top) until the leave (down)    
	"""
	def __init__(self,state:tuple, parent, action: str, path_cost:int):
		self._state: tuple = state
		self._parent: Node = parent
		self._path_cost: int = path_cost
		self._action: str = action
		if parent != None:
			self._total_cost = self._path_cost + self._parent.get_total_cost()
		else:
			self._total_cost = path_cost
			
	def get_total_cost(self) -> int:
		return self._total_cost

	def get_path_cost(self) -> int:
		return self._path_cost

	def get_parent(self):
		return self._parent
	
	def get_state(self) -> tuple:
		return self._state

	def print(self):
		print(self._state,"(",self._path_cost,",",self._total_cost,")")

	



