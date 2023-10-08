class Node:
    """The heuristic node has a name and keeps connection to parent
        which is a Node or None.
        The _path_cost is the cost between parent and the node
        The _g is the some of all costs from previous connections
        from the tree root (top) until the leave (down)
        The _h value, which is the value added to each state
        The _f value which is the sum of _h and _g
    """
    def __init__(self,state:tuple, parent, action: str, path_cost:int, heur_value:int):
        self._state: tuple = state
        self._parent: Node = parent
        self._path_cost: int = path_cost
        self._action: str = action
        self._h: int = heur_value
        if parent != None:
            self._g = self._path_cost + self._parent.get_g()
        else:
            self._g = path_cost


    def get_g(self) -> int:
        return self._g

    def get_h(self) -> int:
        return self._h

    def get_f(self) -> int:
        return self._g + self._h

    def get_path_cost(self) -> int:
        return self._path_cost

    def get_parent(self):
        return self._parent

    def get_state(self) -> tuple:
        return self._state

    def print(self):
        print(self._state,"(",self._path_cost,",",self._g,",",self._h,")")





