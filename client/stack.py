import nodes

class Stack():
	"""
	A class stack utiliza uma lista mas acede à lista utilizando o push e o pop.
	É uma pilha com tamanho ilimitado. Ainda tem funções para retornar o número de elementos,
	a pilha como lista, testar se a pilha está vazia, e a impressão de elemento a elemento
	da pilha do topo à base, assumindo que o elemento tem uma função "print" própria.
	"""
	def __init__(self):
		self._stack = []

	def get_size(self):
		return len(self._stack)

	def get_list(self):
		return self._stack

	def push(self,elem:nodes.Node):
		self._stack.append(elem)
	
	def pop(self) -> nodes.Node:
		elem = self._stack.pop()		
		return elem

	def empty(self) -> bool:
		if not self._stack:
			return True
		else:
			return False


	def print_stack(self,desc:str):
		print(desc,":")
		print("+top+")
		for i in range(1,len(self._stack) + 1):
			self._stack[(-1)*i].print()
		print("+bottom+")
    
