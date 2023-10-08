import client
import ast
import random
import nodes_heuristic
import queue_heuristic

class Agent:
    def __init__(self):
        self.c = client.Client('127.0.0.1', 50000)
        self.res = self.c.connect()
        random.seed()  # To become true random, a different seed is used! (clock time)
        self.visited_nodes = []
        self.frontier_nodes = queue_heuristic.Queue()
        self.weight_map =[]
        self.weight_dict = {}
        self.goal_pos =(0,0)
        self.state = (0,0)
        self.max_coord = (0,0)
        self.obstacles = []



    def get_goal_position(self):
        msg = self.c.execute("info", "goal")
        goal = ast.literal_eval(msg)
        # test
        # print('Goal is located at:', goal)
        return goal

    def get_self_position(self):
        msg = self.c.execute("info", "position")
        pos = ast.literal_eval(msg)
        # test
        # print('Received agent\'s position:', pos)
        return pos

    def get_weight_map(self):
        msg = self.c.execute("info", "map")
        w_map = ast.literal_eval(msg)
        # test
        # print('Received map of weights:', w_map)
        return w_map

    def get_weight_dict(self):
        """Transform the weights into a dictionary"""
        msg = self.c.execute("info", "map")
        w_map = ast.literal_eval(msg)

        w_dict = {}
        for elem in w_map:
            w_dict[elem[0]]=elem[1]
        # print(w_dict)
        return w_dict

    def get_max_coord(self):
        msg = self.c.execute("info","maxcoord")
        max_coord =ast.literal_eval(msg)
        # test
        # print('Received maxcoord', max_coord)
        return max_coord

    def get_obstacles(self):
        msg = self.c.execute("info","obstacles")
        obst =ast.literal_eval(msg)
        # test
        # print('Received map of obstacles:', obst)
        return obst

    def step(self,pos,action):
        """Add new position after an action, using north, east, west or south"""
        if action == "east":
            if pos[0] + 1 < self.max_coord[0]:
                new_pos = (pos[0] + 1, pos[1])
            else:
                new_pos =(0,pos[1])

        if action == "west":
            if pos[0] - 1 >= 0:
                new_pos = (pos[0] - 1, pos[1])
            else:
                new_pos = (self.max_coord[0] - 1, pos[1])

        if action == "south":
            if pos[1] + 1 < self.max_coord[1]:
                new_pos = (pos[0], pos[1] + 1 )
            else:
                new_pos = (pos[0], 0)

        if action == "north":
            if pos[1] - 1 >= 0:
                new_pos = (pos[0], pos[1] - 1)
            else:
                new_pos = (pos[0], self.max_coord[1] - 1 )

        return new_pos

    def mark(self, pos:tuple, colour:str):
        mark_ground = str(pos[0])+","+str(pos[1])+"_"+colour
        msg = self.c.execute("mark",mark_ground)
        obst =ast.literal_eval(msg)

    def unmark(self,pos:tuple):
        unmark_ground = str(pos[0])+","+str(pos[1])
        msg = self.c.execute("unmark",unmark_ground)
        obst =ast.literal_eval(msg)


    def create_node(self,parent_node,action):
        """Create a new node based on action and on parent_node"""
        # return a new position after the actions
        state = self.step(parent_node.get_state(),action)
        h = self.get_heuristic(state)
        return nodes_heuristic.Node(state, parent_node, action, self.weight_dict[state],h)

    def print_nodes(self,description,nds: list):
        print(description)
        print("Name(Parent):g   h  f")
        for nd in nds:
            if nd.get_parent() != None:
                print(nd.get_state(),"(",nd.get_parent().get_state(),"):",nd.get_g(),nd.get_h(),nd.get_f())
            else:
                print(nd.get_state(),"(---):",nd.get_g(),nd.get_h(),nd.get_f())
        print("---------------------------")

    def in_visited_nodes(self, nd:nodes_heuristic.Node):
        visited = False
        for vn in self.visited_nodes:
            if vn.get_state() == nd.get_state():
                visited = True
                break
        # Test
        #print("Node ",nd.get_state()," is in a visited state? ", visited)
        return visited

    def state_has_obstacle(self, nd:nodes_heuristic.Node):
        obstacle = False
        for obst in self.obstacles:
            if nd.get_state() == obst:
                obstacle = True
                break
        # Test
        #print("Node ",nd.get_state()," is in an obstacle? ", obstacle)
        return obstacle

    def remove_nodes_visited(self):
        new_frontier = queue_heuristic.Queue()
        for elem in self.frontier_nodes.get_list():
            if not self.in_visited_nodes(elem):
                new_frontier.add(elem)
        return new_frontier


    def get_heuristic(self, state: tuple) -> int:
        '''This heuristic uses the Manhattan distance.
        calculating the differences between x and y coordinates
        input: state (tuple)
        output: Manhattan distance (int)
        '''
        diff_in_x = self.goal_pos[0] - state[0];
        if diff_in_x < 0:
            diff_in_x = (-1) * diff_in_x
        diff_in_y = self.goal_pos[1] - state[1]
        if diff_in_y < 0:
            diff_in_y = (-1) * diff_in_y

        return diff_in_x + diff_in_y


    def print_path(self, node):
        n = node
        n_list = []
        while n.get_path_cost() != 0:
            n_list.insert(0,[n.get_state(), n.get_path_cost()])
            n = n.get_parent()
        # Test
        print("Final Path", n_list)

    def expand(self,type) -> nodes_heuristic.Node:
        if type == "greedy":
            ne = self.frontier_nodes.get_h_sorted()
        elif type == "a_star":
            ne = self.frontier_nodes.get_f_sorted()
        return ne


    def run(self):
        # Get the position of the Goal
        self.goal_pos = self.get_goal_position()
        print("Goal node:",self.goal_pos)
        # Get information of the weights for each step in the world ...
        self.weight_dict = self.get_weight_dict()
        # Test
        print("weights dict:",self.weight_dict)
        self.obstacles = self.get_obstacles()
        # Test
        print("obstacles:", self.obstacles)
        # Get max coordinates
        self.max_coord = self.get_max_coord()
        # Get the initial position of the agent
        self.state = self.get_self_position()
        # Start thinking
        end = False
        found = None
        #Add first node (root)
        root = nodes_heuristic.Node(self.state,None,"",0,self.get_heuristic(self.state))
        self.visited_nodes.append(root)
        # Get the first four nodes. They are not in the same position of the root node.
        for act in ["north","east","south","west"]:
            elem = self.create_node(root,act)
            if not self.in_visited_nodes(elem) and not self.state_has_obstacle(elem):
                self.frontier_nodes.add(elem)
                self.mark(elem.get_state(),"red")
        # Test
        self.print_nodes("Nodes in frontier", self.frontier_nodes.get_list())
        self.print_nodes("Nodes visitied", self.visited_nodes)
        input()
        # Cycle expanding nodes following the sequence in frontier nodes.
        while end == False:
            # Expanding strategy
            node_to_expand = self.expand("greedy")
            self.unmark(node_to_expand.get_state())
            self.state = node_to_expand.get_state()
            # Test
            print("Expanding node position:", self.state)
            self.visited_nodes.append(node_to_expand)
            self.mark(node_to_expand.get_state(),"blue")
            for act in ["north","east","west","south"]:
                new_node = self.create_node(node_to_expand,act)
                if not self.in_visited_nodes(new_node) and not self.state_has_obstacle(new_node):
                    self.frontier_nodes.add(new_node)
                    self.mark(new_node.get_state(),"red")
            # remove all nodes visited from frontier nodes
            self.frontier_nodes = self.remove_nodes_visited()
            # Test
            self.print_nodes("Frontier", self.frontier_nodes.get_list())
            self.print_nodes("Visitied", self.visited_nodes)
            for node in self.visited_nodes:
                if node.get_state() == self.goal_pos:
                    print("Node state:",node.get_state())
                    print("GoalNodePos",self.goal_pos)
                    found = node
                    self.print_path(found)
                    end = True
                    break
            input()
        input("Waiting for return!")


# Starting the program...
def main():
    agent = Agent()
    agent.run()

main()